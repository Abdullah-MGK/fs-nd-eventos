import os
import json
from flask_sqlalchemy import SQLAlchemy
import unittest
from api import app
# from models import db_drop_and_create_all
# from models import Event, Manager, Participant, EventAttendance

ADMIN_TOKEN = os.environ.get(
    'ADMIN_TOKEN', "ADMIN_TOKEN not found in environment")
MANAGER_TOKEN = os.environ.get(
    'MANAGER_TOKEN', "MANAGER_TOKEN not found in environment")
PARTICIPANT_TOKEN = os.environ.get(
    'PARTICIPANT_TOKEN', "PARTICIPANT_TOKEN not found in environment")

ADMIN_AUTH = ({'Authorization': 'Bearer ' + ADMIN_TOKEN})
MANAGER_AUTH = ({'Authorization': 'Bearer ' + MANAGER_TOKEN})
PARTICIPANT_AUTH = ({'Authorization': 'Bearer ' + PARTICIPANT_TOKEN})


class EventosTestCase(unittest.TestCase):
    """This class represents the eventos test case"""

    manager_id = 0
    event_id = 0
    participant_id = 0

    # https://fsnd-eventos.us.auth0.com/authorize?audience=Eventos&response_type=token&client_id=yE1MY2oQLRaBdPrAlau0C3wKvmMI9m9D&redirect_uri=http://127.0.0.1:5000/
    # manager1@ev.com : manager1@ev.com : manager
    # part1@ev.com : part1@ev.com : participant
    # admin1@ev.com : admin1@ev.com : admin

    def setUp(self):
        # Define test variables and initialize app
        self.client = app.test_client
        '''
        # self.app = app
        # self.client = self.app.test_client
        self.database_name = "eventos_test"
        self.database_domain = "localhost:5432"
            DATABASE_URL = "postgresql://{}/{}".format(
        self.database_domain, self.database_name)
        # setup_db(self.app, self.database_path)
        # db_drop_and_create_all()
        '''
        '''
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()
        '''

    def tearDown(self):
        """Executed after each test"""
        pass

    # Endpoints testcases

    # Root Endpoints

    # GET /

    def test_root(self):
        res = self.client().get('/')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    # Manager Endpoints

    # GET /manger

    def test_get_manager_1(self):
        res = self.client().get('/manager')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['managers']), 0)

    # POST /manager
    def test_post_manager_1(self):
        data = {
            "name": "manager-1",
            "phone": "0501234567",
            "website": "www.google.com",
            "image_link": "https://i.imgur.com/0hQyd5L.gif"
        }
        res = self.client().post(
            '/manager', json=data, headers=ADMIN_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['manager']['name'], "manager-1")

    # POST /manager
    def test_post_manager_2(self):
        data = {
            "name": "manager-2",
            "phone": "0507654321",
            "website": "www.facebook.com",
            "image_link": "https://i.imgur.com/0hQyd5L.gif"
        }
        res = self.client().post(
            '/manager', json=data, headers=ADMIN_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['manager']['name'], "manager-2")

    # DELETE /manager
    def test_delete_manager(self):
        data = {
            "id": 2
        }
        res = self.client().delete(
            '/manager', json=data, headers=ADMIN_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted']['id'], 2)

    # GET /manger
    def test_get_manager_2(self):
        res = self.client().get('/manager')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['managers']), 1)

    # Event Endpoints

    # GET /event

    def test_get_event_1(self):
        res = self.client().get('/event')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['events']), 0)

    # POST /event
    def test_post_event_1(self):
        data = {
            "name": "event-1",
            "manager_id": 1,
            "genre": ["Music"],
            "province": "Eastern",
            "city": "Khobar",
            "image_link": "https://i.imgur.com/0hQyd5L.gif"
        }
        res = self.client().post(
            '/event', json=data, headers=MANAGER_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['event']['name'], "event-1")

    # POST /event
    def test_post_event_2(self):
        data = {
            "name": "event-2",
            "manager_id": 1,
            "genre": ["Movie"],
            "province": "Western",
            "city": "Jeddah",
            "image_link": "https://i.imgur.com/0hQyd5L.gif"
        }
        res = self.client().post(
            '/event', json=data, headers=MANAGER_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['event']['name'], "event-2")

    # DELETE /event
    def test_delete_event(self):
        data = {
            "id": 2
        }
        res = self.client().delete(
            '/event', json=data, headers=MANAGER_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted']['id'], 2)

    # PATCH /event
    def test_patch_event(self):
        data = {
            "id": 1,
            "name": "event-updated"
        }
        res = self.client().patch(
            '/event', json=data, headers=MANAGER_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['event']['name'], "event-updated")

    # GET /event
    def test_get_event_2(self):
        res = self.client().get('/event')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['events']), 1)

    # Participant Endpoints

    # GET /participant

    def test_get_participant_1(self):
        res = self.client().get('/participant')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['participants']), 0)

    # POST /participant
    def test_post_participant_1(self):
        data = {
            "name": "participant-1",
            "phone": "0504567123"
        }
        res = self.client().post(
            '/participant', json=data, headers=PARTICIPANT_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['participant']['name'], "participant-1")

    # POST /participant
    def test_post_participant_2(self):
        data = {
            "name": "participant-2",
            "phone": "0501122334"
        }
        res = self.client().post(
            '/participant', json=data, headers=PARTICIPANT_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['participant']['name'], "participant-2")

    # DELETE /participant
    def test_delete_participant(self):
        data = {
            "id": 2
        }
        res = self.client().delete(
            '/participant', json=data, headers=PARTICIPANT_AUTH)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted']['id'], 2)

    # GET /participant
    def test_get_participant_2(self):
        res = self.client().get('/participant')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['participants']), 1)


def suite():
    suite = unittest.TestSuite()

    # run Root tests
    suite.addTest(EventosTestCase('test_root'))

    # run Manager tests
    suite.addTest(EventosTestCase('test_get_manager_1'))
    suite.addTest(EventosTestCase('test_post_manager_1'))
    suite.addTest(EventosTestCase('test_post_manager_2'))
    suite.addTest(EventosTestCase('test_delete_manager'))
    suite.addTest(EventosTestCase('test_get_manager_2'))

    # run Event tests
    suite.addTest(EventosTestCase('test_get_event_1'))
    suite.addTest(EventosTestCase('test_post_event_1'))
    suite.addTest(EventosTestCase('test_post_event_2'))
    suite.addTest(EventosTestCase('test_delete_event'))
    suite.addTest(EventosTestCase('test_patch_event'))
    suite.addTest(EventosTestCase('test_get_event_2'))

    # run Participant tests
    suite.addTest(EventosTestCase('test_get_participant_1'))
    suite.addTest(EventosTestCase('test_post_participant_1'))
    suite.addTest(EventosTestCase('test_post_participant_2'))
    suite.addTest(EventosTestCase('test_delete_participant'))
    suite.addTest(EventosTestCase('test_get_participant_2'))

    return suite


# Make the tests conveniently executable
if __name__ == "__main__":
    # unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
