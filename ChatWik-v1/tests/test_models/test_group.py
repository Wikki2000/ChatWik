#!/usr/bin/python3
"""Models test cases for user module."""
from models.user import User
from models.group_message import GroupMessage
from models.group import Group
from models import Storage
import unittest


class TestLecturer(unittest.TestCase):
    """Define test cases for Group class."""

    def setUp(self):
        """Set up test environment."""

        # Create User object
        self.storage = Storage()
        self.user_attr = {"first_name": "John", "last_name": "Bush",
                     "email": "example@gmail.com", "password": "12345"}
        self.user = User(**self.user_attr)
        self.session = self.storage.get_session()

        # Create Group object
        self.grp_attr = {"name": "Coding", "description": "Software Engineers grp."}
        self.grp = Group(**self.grp_attr)

        # Save Group and User object to database
        self.session.add_all([self.grp, self.user])
        self.session.commit()

    def tearDown(self):
        """Teardown test environment for every test."""
        self.session.query(User).delete()
        self.session.query(Group).delete()
        self.session.commit()

    def test_group_creation(self):
        """Test that the Group object was saved and can be retrieved."""
        self.assertIsInstance(self.grp, Group)
        obj = self.session.query(Group).filter_by(
                id=self.grp.id).one()
        self.assertIsNotNone(obj)
        self.assertEqual("Coding", obj.name)

    def test_group_groupmessage_relationship(self):
        """Test relationship of Group and GroupMessages."""
        grp_msg = GroupMessage(
            user_id=self.user.id, group_id=self.grp.id, text="Hi guys"
        )
        self.session.add(grp_msg)
        self.session.commit()

        self.assertEqual(grp_msg.group.name, self.grp.name)
        self.assertEqual(grp_msg.user.id, self.user.id)


if __name__ == "__main__":
    unittest.main()
