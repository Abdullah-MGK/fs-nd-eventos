import os
import sys
import json
from flask import Flask, request, jsonify, abort
#from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import exc
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import setup_db, db_create_all
from models import Event, Manager, Participant, EventAttendance


app = Flask(__name__)
CORS(app)

#NOTE: For Local Setup
database_name = "eventos"
database_domain = "localhost:5432"
database_path = "postgresql://{}/{}".format(database_domain, database_name)

#NOTE: For Heroku Setup
#database_path = os.environ['DATABASE_URL']

setup_db(app, database_path)

#NOTE: comment this for Heroku Setup
db_create_all()


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,DELETE,PATCH,OPTIONS')
    return response


## ROUTES

# Event

# endpoint GET /
# public endpoint
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'success':True
    })

# endpoint GET /event
# public endpoint
# TODO: paging
@app.route('/event', methods=['GET'])
def get_events():
    try:
        events = Event.query.order_by(Event.id).all()
        
    except Exception:
        abort(500, "get event request has missing parameters")
         
    return jsonify({
        'success':True,
        'events': [event.format() for event in events]
    })

# endpoint POST /event
# Role: Admin, Manager
@app.route('/event', methods=['POST'])
@requires_auth('post:event')
def add_event(jwt):
#def add_event():   #for no authorization
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
        'success':True,
        'event': new_event.format()
    })

# endpoint DELETE /event
# Role: Admin, Manager
@app.route('/event', methods=['DELETE'])
@requires_auth('delete:event')
def delete_event(jwt):
#def delete_event():    #for no authorization
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
        'success': True,
        'deleted': event.format()
    })

# endpoint PATCH /event
# Role: Admin, Manager
@app.route('/event', methods=['PATCH'])
@requires_auth('patch:event')
def update_event(jwt):
#def update_event():    #for no authorization
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
        'success': True,
        'event': event.format()
    })


# Manager

# endpoint GET /manager
# public endpoint
@app.route('/manager', methods=['GET'])
def get_managers():
    try:
        managers = Manager.query.order_by(Manager.id).all()
        
    except Exception:
        abort(500, "get managers request has missing parameters")
         
    return jsonify({
        'success':True,
        'managers': [manager.format() for manager in managers]
    })

# endpoint POST /manager
# Role: Admin
@app.route('/manager', methods=['POST'])
@requires_auth('post:manager')
def add_manager(jwt):
#def add_manager(): #for no authorization
    try:
        name = request.json.get('name')
        phone = request.json.get('phone')
        website = request.json.get('website')
        image_link = request.json.get('image_link')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "add manager request has missing parameters")
        
    if not name:
        print("in if", file = sys.stderr)
        abort(422, "add manager request has missing parameters")
        
    try:
        new_manager = Manager(name=name, phone=phone, website=website, image_link=image_link)
        new_manager.insert()
        print("NEW MANAGER ID", file = sys.stderr)
        print(new_manager.id, file = sys.stderr)
        
    except Exception:
        #db.session.rollback()
        abort(500, "add manager request has missing parameters")

    return jsonify({
        'success':True,
        'manager': new_manager.format()
    })

# endpoint DELETE /manager
# Role: Admin
@app.route('/manager', methods=['DELETE'])
@requires_auth('delete:manager')
def delete_manager(jwt):
#def delete_manager():  #for no authorization
    try:
        manager_id = request.json.get('id')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "delete manager request has missing parameters")
        
    if not manager_id:
        print("in if", file = sys.stderr)
        abort(422, "delete manager request has missing parameters")

    print("manager id", file = sys.stderr)

    try:
        manager = Manager.query.get(manager_id)

    except Exception:
        print("in except", file = sys.stderr)
        abort(422, "delete manager request has missing parameters")

    if not manager:
        abort(404, "delete manager request has missing parameters")

    try:
        manager.delete()

    except Exception:
        #db.session.rollback()
        abort(500, "delete manager request has missing parameters")

    return jsonify({
        'success': True,
        'deleted': manager.format()
    })


# Participant

# endpoint GET /participant
# Role: Admin
@app.route('/participant', methods=['GET'])
def get_participants():
    try:
        participants = Participant.query.order_by(Participant.id).all()
        
    except Exception:
        abort(500, "get participants request has missing parameters")

    return jsonify({
        'success':True,
        'participants': [participant.format() for participant in participants]
    })

# endpoint POST /participant
# Role: Admin, Manager, Participant
@app.route('/participant', methods=['POST'])
@requires_auth('post:participant')
def add_participant(jwt):
#def add_participant(): #for no authorization
    try:
        name = request.json.get('name')
        phone = request.json.get('phone')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "add participant request has missing parameters")
        
    if not name:
        print("in if", file = sys.stderr)
        abort(422, "add participant request has missing parameters")
        
    try:
        new_participant = Participant(name=name, phone=phone)
        new_participant.insert()
        print("NEW PARTICIPANT ID", file = sys.stderr)
        print(new_participant.id, file = sys.stderr)
        
    except Exception:
        #db.session.rollback()
        abort(500, "add participant request has missing parameters")

    return jsonify({
        'success':True,
        'participant': new_participant.format()
    })

# endpoint DELETE /participant
# Role: Admin, Manager, Participant
@app.route('/participant', methods=['DELETE'])
@requires_auth('delete:participant')
def delete_participant(jwt):
#def delete_participant():  #for no authorization
    try:
        participant_id = request.json.get('id')
        
    except Exception:
        print("in except", file = sys.stderr)
        abort(400, "delete participant request has missing parameters")
        
    if not participant_id:
        print("in if", file = sys.stderr)
        abort(422, "delete participant request has missing parameters")

    try:
        participant = Participant.query.get(participant_id)

    except Exception:
        print("in except", file = sys.stderr)
        abort(422, "delete participant request has missing parameters")

    if not participant:
        abort(404, "delete participant request has missing parameters")

    try:
        participant.delete()

    except Exception:
        #db.session.rollback()
        abort(500, "delete participant request has missing parameters")

    return jsonify({
        'success': True,
        'deleted': participant.format()
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
