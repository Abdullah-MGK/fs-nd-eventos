import os
import sys
import json
from flask import Flask, request, jsonify, abort
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import exc
from flask_cors import CORS
from auth.auth import AuthError, requires_auth


app = Flask(__name__)
CORS(app)


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    return response


## ROUTES

# endpoint GET /events
# public endpoint
@app.route('/events', methods=['GET'])
def get_events():
    return jsonify({
        'success':True
    })

# endpoint GET /event-details
# public endpoint
@app.route('/event-details', methods=['GET'])
def get_event_details():
    return jsonify({
        'success':True
    })

# endpoint POST /event
# Role: Admin, Manager
@app.route('/event', methods=['POST'])
@requires_auth('post:event')
def add_event(jwt):
    return jsonify({
        'success':True
    })

# endpoint DELETE /events/<id>
# Role: Admin, Manager
@app.route('/events/<int:event_id>', methods=['DELETE'])
@requires_auth('delete:event')
def delete_event(jwt, event_id):
    return jsonify({
        'success': True
    })

# endpoint PATCH /events/<id>
# Role: Admin, Manager
@app.route('/events/<int:event_id>', methods=['PATCH'])
@requires_auth('patch:event')
def update_event(jwt, event_id):
    return jsonify({
        'success': True
    })

# endpoint POST /participant
# Role: Participant
@app.route('/participant', methods=['POST'])
@requires_auth('post:participant')
def add_participant(jwt):
    return jsonify({
        'success':True
    })

# endpoint DELETE /events/<id>/<id>
# Role: Participant
@app.route('/events/<int:event_id>/<int:participant_id>', methods=['DELETE'])
@requires_auth('delete:participant')
def delete_participant(jwt, event_id, participant_id):
    return jsonify({
        'success': True
    })


## Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False, 
        "error": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "Not Found"
    }), 404

@app.errorhandler(422)
def unprocessable_request(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": "Unprocessable Request"
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": "Internal Server Error"
    }), 500
