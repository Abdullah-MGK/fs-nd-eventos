import os
import json
from flask_sqlalchemy import SQLAlchemy
import unittest
from api import app
# from models import db_drop_and_create_all
# from models import Event, Manager, Participant, EventAttendance


class EventosTestCase(unittest.TestCase):
    """This class represents the eventos test case"""

    manager_id = 0
    event_id = 0
    participant_id = 0

    # https://fsnd-eventos.us.auth0.com/authorize?audience=Eventos&response_type=token&client_id=yE1MY2oQLRaBdPrAlau0C3wKvmMI9m9D&redirect_uri=http://127.0.0.1:5000/
    # manager1@ev.com : manager1@ev.com : manager
    # part1@ev.com : part1@ev.com : participant
    # admin1@ev.com : admin1@ev.com : admin

    admin_token = ({'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZXWTJZNnZjZjV4WU1JZWc4S0s0RyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtZXZlbnRvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxMWFjZGNkZjdiNWEwMDcxOGRmMTMwIiwiYXVkIjoiRXZlbnRvcyIsImlhdCI6MTYxMjExMjA4OCwiZXhwIjoxNjEyMTE5Mjg4LCJhenAiOiJ5RTFNWTJvUUxSYUJkUHJBbGF1MEMzd0t2bU1JOW05RCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmV2ZW50IiwiZGVsZXRlOm1hbmFnZXIiLCJkZWxldGU6cGFydGljaXBhbnQiLCJwYXRjaDpldmVudCIsInBvc3Q6ZXZlbnQiLCJwb3N0Om1hbmFnZXIiLCJwb3N0OnBhcnRpY2lwYW50Il19.0UjuQSuDvAeOi6_UdRdIW_PhzKp-3cvfbls1DiUCP7TO0vO8TEcjPMlBNWxB6ersy5oWZsQoUpE98dOxASBQhZ_vLPb5wfE2Hz1QIYUYEYhaHIFxThjtRvYF6aj8-GeolNcpYMimREQfMVTndP3tQP_0Dsrf87EHrwNNpxUHZZq_FsztppUCrxKL57XxuGd-ZbMALUCtsHaDFNTfCb7ZFdoEvuIXnGAGzevmRHNm5hagotVQCCnXgrtukk3CF7YKS4UeMHM2L3AabChTFlyu3BmeyNzeNpc8zzeEJpvCok7hrIuxNgiXFd5oWDchbgrdZ9fN-qD77shPGRiusbEyCw'})

    manager_token = ({'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZXWTJZNnZjZjV4WU1JZWc4S0s0RyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtZXZlbnRvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxMWFjOTU1MTg1M2IwMDZhMDEzMDY2IiwiYXVkIjoiRXZlbnRvcyIsImlhdCI6MTYxMjExMjEyMSwiZXhwIjoxNjEyMTE5MzIxLCJhenAiOiJ5RTFNWTJvUUxSYUJkUHJBbGF1MEMzd0t2bU1JOW05RCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmV2ZW50IiwicGF0Y2g6ZXZlbnQiLCJwb3N0OmV2ZW50Il19.QZSyof3QfNDJulRWj3CuR8lMq10XBkQ_ddLOjOzi1a_N-xYgzZx6KGNV4o7sP8rar8wvdE174yb5qeZRQ-bbMM8ArA0qe0vTh8x716J-aMejyT8TFfs4yAINn4Ot6816k16JHErOv7rCz2fK9zr-yocF6zBJN69L0zwlkYr1WXB-EE4rZWq9TWmZVX4-VfR-2I3nJQN2iS8EtfGa-ytx3E965g_ulCu_jNX79-6zbEd7ZJ81j5vZZqHdR6tc0TfovTRrW8_qjymapiTQyhzhf_6u3qXr1hCGAyj8OMVmzcA0XCIYgl_oZnzp_DA4sEdJMu1gxH7KjK1wHc9fgwMyxQ'})

    participant_token = ({'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlZXWTJZNnZjZjV4WU1JZWc4S0s0RyJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtZXZlbnRvcy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAxMWFjYzA0NDFmZDYwMDcwODI0YzBiIiwiYXVkIjoiRXZlbnRvcyIsImlhdCI6MTYxMjExMjE2MCwiZXhwIjoxNjEyMTE5MzYwLCJhenAiOiJ5RTFNWTJvUUxSYUJkUHJBbGF1MEMzd0t2bU1JOW05RCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnBhcnRpY2lwYW50IiwicG9zdDpwYXJ0aWNpcGFudCJdfQ.jG7YoeQDrBbYNH2vssAT54_9pWhv63ZORC_mb9qT0RSsP-SAWMzQFhPatb51Z_WWgfXL3xCjq97u6upcQ2N-7MbInsgHUybpYKHm5JUlwyzwqbJAa-xyS78wM6YWDT7xeTCQmCLXgt6YRw3rHg-7fU3C0WNAKqfGLtojPvZBy6TCuskIeTna9qshhmcZeYNxhTOEOUxCGdEMmMKH5K1eiVHnAAzqxTK8VvgMiZ4dS-ODIZkQfi3oZO9lTVb3suSXSDnsk6KYMSUTKt-jPd8W76mZvit_KsvNZToHtlk7ACqo922bzcyMKxHsWzSqpJxyr1CFpeBqZ4EwlogdxgBvSA'})

    def setUp(self):
        # Define test variables and initialize app
        # self.app = app
        # self.client = self.app.test_client
        self.client = app.test_client
        self.database_name = "eventos_test"
        self.database_domain = "localhost:5432"
        self.database_path = "postgresql://{}/{}".format(
            self.database_domain, self.database_name)
        # setup_db(self.app, self.database_path)
        # db_drop_and_create_all()

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
            '/manager', json=data, headers=self.admin_token)
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
            '/manager', json=data, headers=self.admin_token)
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
            '/manager', json=data, headers=self.admin_token)
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
            '/event', json=data, headers=self.manager_token)
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
            '/event', json=data, headers=self.manager_token)
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
            '/event', json=data, headers=self.manager_token)
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
            '/event', json=data, headers=self.manager_token)
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
            '/participant', json=data, headers=self.participant_token)
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
            '/participant', json=data, headers=self.participant_token)
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
            '/participant', json=data, headers=self.participant_token)
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
