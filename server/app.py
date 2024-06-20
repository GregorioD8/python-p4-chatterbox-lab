from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

# Here's what the CORS configuration looks like (in the server/app.py file):
# from flask import Flask
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# Create an instance of the Flask class
app = Flask(__name__)
# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Enable Cross-Origin Resource Sharing (CORS) for the app
CORS(app)
# Set up the Flask-Migrate extension for database migrations
migrate = Migrate(app, db)
# Initialize the app with the database
db.init_app(app)

# Define the route to handle GET and POST requests for messages
@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        # Handle GET request: retrieve all messages ordered by created_at
        messages = Message.query.order_by('created_at').all()
        # Create a response with the list of messages and a 200 OK status
        return make_response([message.to_dict() for message in messages], 200)
    
    elif request.method == 'POST':
        # Handle POST request: create a new message
        data = request.get_json()
        message = Message(
            body=data['body'],
            username=data['username']
        )
        # Add the new message to the database session and commit it
        db.session.add(message)
        db.session.commit()

        # Create a response with the new message dictionary and a 201 Created status
        return make_response(message.to_dict(), 201)

# Define the route to handle PATCH and DELETE requests for a specific message by ID
@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    # Query the message with the given ID from the database
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'PATCH':
        #Handle PATCH request: update the message
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        # Add the updated message to the database session and commit it
        db.session.add(message)
        db.session.commit()

        # Create a response with the updated message dictionary and a 200 OK status
        return make_response(message.to_dict(), 200)
    
    elif request.method == 'DELETE':
        #Handle DELETE request: delete the message
        db.session.delete(message)
        db.session.commit()

        #create a response indicating the message was deleted and a 200 OK status 
        return make_response({'deleted': True}, 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
