from settings import engine
from models import Base
import sys

def create_db():
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès")

def drop_db():
    Base.metadata.drop_all(bind=engine)
    print("Tables supprimées avec succès")

def makemigrations():
    drop_db()
    create_db()

def help_cmd():
    print("Utilisation : python manage.py [create_db|drop_db|makemigrations]")

COMMANDS = {
    "create_db": create_db,
    "drop_db": drop_db,
    "makemigrations": makemigrations,
}

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    command = sys.argv[1]
    if command in COMMANDS:
        COMMANDS[command]()
    else:
        help_cmd()