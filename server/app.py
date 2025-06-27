from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    messages = [message.to_dict() for message in Message.query.order_by(Message.created_at).all()]
    
    if request.method == 'GET':
        response = make_response(
            messages,
            200
        )
        return response
    
    elif request.method == 'POST':
        data = request.get_json()
        new_message = Message(
            body=data['body'], 
            username=data['username']
            )
            
        db.session.add(new_message)
        db.session.commit()
            
        return make_response(
            new_message.to_dict(),
            201
            )

@app.route('/messages/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter_by(id=id).first()
    
    if request.method == 'GET':
        response = make_response(
            message.to_dict(),
            200
        )
        return response
    
    elif request.method == 'PATCH':
        data = request.get_json()
        for attr in data:
            setattr(message, attr, data[attr])

        db.session.add(message)
        db.session.commit()

        message_dict =message.to_dict()

        response = make_response(
                message_dict,
                200
            )

        return response
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response_body = {
            "delete_successful": True,
            "message": "Message deleted."
        }
        response = make_response(
            response_body,
            200
        )
        
        return response

if __name__ == '__main__':
    app.run(port=5555)