# Import SQLAlchemy and the SerializerMixin for serializing SQLAlchemy models
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

# Initialize the SQLAlchemy instance
#remove metadata since it is no longer needed
db = SQLAlchemy()

# Define the Message model
class Message(db.Model, SerializerMixin):
    __tablename__ = 'messages'

    # Define columns for the Message model
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    username = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'<Message by {self.username}: {self.body[:10]}...>'
    

