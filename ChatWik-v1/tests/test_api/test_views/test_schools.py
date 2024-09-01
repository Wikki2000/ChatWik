#!/usr/bin/python3
"""Handle test case for api/v1/views/schools modeules."""
from api.v1.app import app
from models.lecturer import Lecturer
from models.school import School
from models import storage
import unittest


class TestSchoolsApi(unittest.TestCase):
    """Handle test case for API request in schools.py"""

    def setUp(self):
        """Setup test environment."""
        self.session = storage.get_session()

        # Create lecturer object
        self.attr = {
               "first_name": "John",
               "last_name": "Doe",
               "email": "example@gmail.com",
               "password": "12345"
        }
        self.lecturer = Lecturer(**self.attr)
        self.session.add(self.lecturer)
        self.session.commit()

        # Create school object
        self.school = School(
                school_name="AKSU",
                dean_name="Dr. Moses",
                lecturer_id=self.lecturer.id
        )
        self.session.add(self.school)
        self.session.commit()

        self.url = "http://127.0.0.1:5001/api/v1/" + \
                   f"lecturer/{self.lecturer.id}/schools"

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        """Remove test data after each test."""
        sch = self.session.query(Lecturer).delete()
        self.session.commit()
        self.session.close()

    def test_post_school_empty_request(self):
        """Test that school object was created via the endpoint."""
        body = {}
        response = self.client.post(self.url, json=body)
        expected_json_response = {"error": "Empty Request Body"}
        self.assertEqual(response.json, expected_json_response)
        self.assertEqual(response.status_code, 400)

    def test_post_school_missing_field(self):
        """Handle test case of missing a name field"""
        body = {"dean_name": "John Bush"}
        expected_json_response = {"error": "school_name Field Missing"}
        response = self.client.post(self.url, json=body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, expected_json_response)

    def test_post_school_invalid_lecturer_id(self):
        """Handle test case for invalid lecturer id."""
        url = "http://127.0.0.1:5001/api/v1/" + \
               "lecturer/54545jyrdtdeea/schools"
        body = {"dean_name": "John Bush", "school_name": "AKSU"}
        expected_json_response = {
                "error": "Not Found",
                "message": "The requested URL was not found on the server"
        }
        response = self.client.post(url, json=body)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, expected_json_response)

    def test_post_school_successful(self):
        """Handle test case for successful request."""
        body = {"dean_name": "John Bush", "school_name": "AKSU"}
        response = self.client.post(self.url, json=body)
        self.assertEqual(response.status_code, 201)

    def test_get_school_success(self):
        """Handle test case for successful request."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["school_name"],
                         self.school.school_name) 
        self.assertEqual(response.json[0]["dean_name"],
                         self.school.dean_name)

    def test_get_school_failure(self):
        """Handle test case for unsuccessful request."""
        invalid_url = "http://127.0.0.1:5001/api/v1/" + \
                      "lecturer/54545jyrdtdeea/schools"
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, 404)
        expected_json_response = {
                "error": "Not Found",
                "message": "The requested URL was not found on the server"
        }
        self.assertEqual(response.json, expected_json_response)


if __name__ == "__main__":
    unittest.main()
