"""Point d'entrée de l'application Learnio."""

from src.app.factory import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
