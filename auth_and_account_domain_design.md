# Auth and Account Domain Architecture Specification

This document outlines the refined, production-ready schema for the authentication, authorization (RBAC), session management, and credential reset domain. It builds upon your initial entity-relationship design by adding best-practice constraints, indexing, normalization corrections, and secure password reset mechanisms.

---

## 1. Complete ERD Schema (PostgreSQL)

```sql
-- 1. Accounts Table: Core user profile information
CREATE TABLE accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR(25) NOT NULL,
    last_name VARCHAR(25) NOT NULL,
    birth_date DATE,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 2. Credentials Table: Authentication details securely separated from profile data
CREATE TABLE credentials (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_credentials_email ON credentials(email);

-- 3. Sessions Table: Active user sessions / tokens tracking
CREATE TABLE sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    ip VARCHAR(45),
    user_agent TEXT,
    token_hash VARCHAR(64) NOT NULL, -- Stored as a cryptographic hash for security
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_account_id ON sessions(account_id);
CREATE INDEX idx_sessions_token_hash ON sessions(token_hash);

-- 4. Credential Resets Table: Secure management of password reset and magic link tokens
CREATE TABLE credential_resets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    credential_id UUID NOT NULL REFERENCES credentials(id) ON DELETE CASCADE,
    token_hash VARCHAR(64) NOT NULL, -- Hashed version of the reset token sent to the user
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    used_at TIMESTAMP WITH TIME ZONE DEFAULT NULL, -- Null until successfully consumed (one-time use)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_credential_resets_token_hash ON credential_resets(token_hash);

-- 5. Roles Table: RBAC role definitions
CREATE TABLE roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- 6. Account Roles Table: Many-to-many relationship mapping accounts to roles
CREATE TABLE account_roles (
    account_id UUID REFERENCES accounts(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (account_id, role_id)
);

-- 7. Permissions Table: Fine-grained permissions broken down by domain, resource, and action
CREATE TABLE permissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    domain VARCHAR(50) NOT NULL,
    resource VARCHAR(50) NOT NULL,
    action VARCHAR(50) NOT NULL,
    CONSTRAINT uq_permission_triplet UNIQUE (domain, resource, action)
);

-- 8. Role Permissions Table: Many-to-many relationship mapping roles to permissions
CREATE TABLE role_permissions (
    role_id UUID REFERENCES roles(id) ON DELETE CASCADE,
    permission_id UUID REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);
```

---

## 2. Design Improvements & Highlights

### Security Enhancements
* **Token Hashing (`sessions` & `credential_resets`):** Raw session tokens and password reset links are never stored in plaintext. Instead, a cryptographic hash (e.g., SHA-256) is persisted. If the database is read by an unauthorized actor, tokens cannot be directly exploited.
* **One-Time Use Enforcement:** The `credential_resets` table uses a `used_at` timestamp rather than immediate row deletion. This provides clean audit trails and prevents replay attacks.
* **Email Normalization & Indexing:** `credentials.email` features a unique constraint and index, and applications should ensure emails are always lowercased before insertion.

### Architectural Corrections from Original Design
* **Typo Correction:** Fixed `ressource` to `resource` in the `permissions` table.
* **Data Type Realignment:** Changed `birth_date` from `TimeStamp(25)` to a standard `DATE` type.
* **Composite Primary Keys:** Added explicit composite primary keys to junction tables (`account_roles` and `role_permissions`) to eliminate duplicate assignment bugs.
* **Temporal Tracking:** Replaced static boolean flags for expiration with precise `expires_at` timestamps to allow efficient querying and dynamic expiration checks (`WHERE expires_at > CURRENT_TIMESTAMP`).

---

## 3. Recommended Operational Workflows

### Password Reset Flow
1. **Request Initiation:** User submits their email. If the account exists, the backend generates a secure random token (e.g., 32 bytes).
2. **Persistence:** The token is hashed, given an expiration window (e.g., 15 minutes), and recorded in `credential_resets`.
3. **Dispatch:** The plaintext token is sent via email inside a secure link.
4. **Verification & Execution:** When clicked, the incoming token is hashed and checked against `credential_resets` (`token_hash = ?`, `expires_at > NOW()`, `used_at IS NULL`). Upon success, the password in `credentials` is updated, `used_at` is marked, and active sessions are revoked.
