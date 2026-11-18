from app.database import engine, Base
from app.models import User, Conversation, ChatMessage


def create_tables():

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully!")


if __name__ == "__main__":
    create_tables()