import os
import json
from flask_sqlalchemy import SQLAlchemy
import unittest
from api import app
from models import setup_db, db_create_all
from models import Event, Manager, Participant, EventAttendance


class EventosTestCase(unittest.TestCase):
    """This class represents the eventos test case"""
    
    manager_id = 0
    event_id = 0
    participant_id = 0
    
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "eventos_test"
        self.database_domain = "localhost:5432"
        self.database_path = "postgresql://{}/{}".format(self.database_domain, self.database_name)
        setup_db(self.app, self.database_path)
        db_create_all()
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
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

    #POST /manager
    def test_post_manager_1(self):
        data = {
            "name":"manager-1"
        }
        res = self.client().post('/manager', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['manager']), 1)

    #POST /manager
    def test_post_manager_2(self):
        data = {
            "name":"manager-2"
        }
        res = self.client().post('/manager', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['manager']), 2)

    # DELETE /manager
    def test_delete_manager(self):
        data = {
            "id": 2
        }
        res = self.client().delete('/manager', json=data)
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

    #POST /event
    def test_post_event_1(self):
        data = {
            "name":"event-1",
            "manager_id":1
        }
        res = self.client().post('/event', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['event']), 1)

    #POST /event
    def test_post_event_2(self):
        data = {
            "name":"event-2",
            "manager_id":1
        }
        res = self.client().post('/event', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['event']), 2)

    # DELETE /event
    def test_delete_event(self):
        data = {
            "id": 2
        }
        res = self.client().delete('/event', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted']['id'], 2)

    #PATCH /event
    def test_patch_event(self):
        data = {
            "id":1,
            "name": "event-updated"
        }
        res = self.client().patch('/event', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['event']['name']), "event-updated")

    # GET /event
    def test_get_event_2(self):
        res = self.client().get('/event')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['events']), 0)

    
    # Participant Endpoints

    # GET /participant
    def test_get_participant_1(self):
        res = self.client().get('/participant')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['participants']), 0)

    #POST /participant
    def test_post_participant_1(self):
        data = {
            "name":"participant-1"
        }
        res = self.client().post('/participant', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['participant']), 1)

    #POST /participant
    def test_post_participant_2(self):
        data = {
            "name":"participant-2"
        }
        res = self.client().post('/participant', json=data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['participant']), 2)

    # DELETE /participant
    def test_delete_participant(self):
        data = {
            "id": 2
        }
        res = self.client().delete('/participant', json=data)
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
    #unittest.main()
    runner = unittest.TextTestRunner(failfast=True)
    runner.run(suite())
