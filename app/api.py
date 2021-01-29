import os
import sys
import json
from flask import Flask, request, jsonify, abort
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import exc
from flask_cors import CORS
from auth.auth import AuthError, requires_auth
from models.models import setup_db, db_drop_and_create_all
from models.models import Event, Manager, Participant, EventAttendance


app = Flask(__name__)
CORS(app)
setup_db(app)
db_drop_and_create_all()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    return response


## ROUTES

# Event

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
#@requires_auth('post:event')
#def add_event(jwt):
def add_event():
    try:
        name = request.json.get('name')
        genre = request.json.get('genre')
        province = request.json.get('province')
        city = request.json.get('city')
        date = request.json.get('date')
        image_link = request.json.get('image_link')
        manager_id = request.json.get('manager_id')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "add event request has missing parameters")

    if not name:
        print("in if", file = sys.stderr)
        abort(422, "add event request has missing parameters")

    try:
        new_event = Event(name=name, genre=genre, province=province, city=city, date=date, image_link=image_link, manager_id=manager_id)
        new_event.insert()
        print("NEW EVENT ID", file = sys.stderr)
        print(new_event.id, file = sys.stderr)
    
    except Exception:
        #db.session.rollback()
        abort(500, "add event request has missing parameters")

    return jsonify({
        'success':True
    })

# endpoint DELETE /event
# Role: Admin, Manager
@app.route('/event', methods=['DELETE'])
#@requires_auth('delete:event')
#def delete_event(jwt):
def delete_event():
    try:
        event_id = request.json.get('id')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "delete event request has missing parameters")
        
    if not event_id:
        print("in if", file = sys.stderr)
        abort(422, "delete event request has missing parameters")

    try:
        event = Event.query.get(event_id)

    except Exception:
        print("in except", file = sys.stderr)
        abort(422, "delete event request has missing parameters")

    if not event:
        abort(404, "delete event request has missing parameters")

    try:
        event.delete()

    except Exception:
        #db.session.rollback()
        abort(500, "delete event request has missing parameters")

    return jsonify({
        'success': True
    })

# endpoint PATCH /events/<id>
# Role: Admin, Manager
@app.route('/event', methods=['PATCH'])
#@requires_auth('patch:event')
#def update_event(jwt, event_id):
def update_event():
    try:
        event_id = request.json.get('id')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "update event request has missing parameters")
        
    if not event_id:
        print("in if", file = sys.stderr)
        abort(422, "update event request has missing parameters")

    try:
        event = Event.query.get(event_id)

    except Exception:
        print("in except", file = sys.stderr)
        abort(422, "update event request has missing parameters")

    if not event_id:
        abort(404, "update event request has missing parameters")

    name = request.json.get('name')
    genre = request.json.get('genre')
    province = request.json.get('province')
    city = request.json.get('city')
    date = request.json.get('date')
    image_link = request.json.get('image_link')
    manager_id = request.json.get('manager_id')

    try:
        if name:
            event.name = name
        if genre:
            event.genre = genre
        if province:
            event.province = province
        if city:
            event.city = city
        if date:
            event.date = date
        if image_link:
            event.image_link = image_link
        if manager_id:
            event.manager_id = manager_id

        event.update()

    except Exception:
        #db.session.rollback()
        abort(500, "update event request has missing parameters")
        
    return jsonify({
        'success': True
    })


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
        "message": str(error)
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": str(error)
    }), 404

@app.errorhandler(422)
def unprocessable_request(error):
    return jsonify({
        "success": False, 
        "error": 422,
        "message": str(error)
    }), 422

@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False, 
        "error": 500,
        "message": str(error)
    }), 500

#error handler for AuthError
@app.errorhandler(AuthError)
def handle_auth_error(exception):
    response = jsonify(exception.error)
    response.status_code = exception.status_code
    return response
