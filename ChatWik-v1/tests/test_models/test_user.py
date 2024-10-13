#!/usr/bin/python3
"""Models test cases for user module."""
from models.user import User
from models.private_message import PrivateMessage
from models.group import Group
from models import Storage
import unittest

class TestLecturer(unittest.TestCase):
    """Define test cases for User class."""

    def setUp(self):
        """Set up test environment."""

        # Create User object
        self.storage = Storage()
        self.user_attr = {"first_name": "John", "last_name": "Bush",
                     "email": "example@gmail.com", "password": "12345"}
        self.user = User(**self.user_attr)
        self.session = self.storage.get_session()
        self.session.add(self.user)
        self.session.commit()

    def tearDown(self):
        """Teardown test environment for every test."""
        self.session.query(User).delete()
        self.session.query(Group).delete()
        self.session.commit()

    def test_user_creation(self):
        """Test that the User object was saved and can be retrieved."""
        self.assertIsInstance(self.user, User)
        obj = self.session.query(User).filter_by(
                email="example@gmail.com").one()
        self.assertIsNotNone(obj)
        self.assertEqual("John", obj.first_name)
        self.assertEqual("Bush", obj.last_name)
        self.assertEqual("example@gmail.com", obj.email)
        self.assertEqual("12345", obj.password)

    def test_hash_password(self):
        """Test that password is correctly hashed."""
        self.user.hash_password()
        self.assertNotEqual(self.user.password, self.user_attr["password"])

    def test_check_password(self):
        """Test that password is correctly verified."""
        self.user.hash_password()
        self.assertTrue(self.user.check_password(self.user_attr["password"]))
        self.assertFalse(self.user.check_password("wrong password"))

    def test_user_privatemessage_relationship(self):
        """Test relationship b/w user and privatemessage class."""
        reciever = User(first_name="Moses", last_name="Okon",
                        email="mok@gmail.com", password="12345")
        self.session.add(reciever)
        self.session.commit()

        pmsg = PrivateMessage(
            sender_id=self.user.id, reciever_id=reciever.id, text="Hw u dey"
        )
        self.session.add(pmsg)
        self.session.commit()

        self.assertIsNotNone(pmsg)

        # Retrieved the message and check some attribute
        retrieved_msg = self.session.query(PrivateMessage).filter_by(
            sender_id=self.user.id, reciever_id=reciever.id
        ).first()
        self.assertIsNotNone(retrieved_msg)

        # Test attributes of sending end
        self.assertEqual(retrieved_msg.sender.first_name, self.user.first_name) 
        self.assertEqual(retrieved_msg.reciever.first_name, reciever.first_name)
        self.assertEqual(
            retrieved_msg.sender_id, reciever.recieved_messages[0].sender_id
        )
        self.assertEqual(
            retrieved_msg.sender_id, self.user.sent_messages[0].sender_id
        )

    def test_user_group_relationship(self):
        """Test relationship b/w user and privatemessage class."""
        group1 = Group(name="Coding")
        self.session.add(group1)
        self.session.commit()

        group2 = Group(name="Engineer")
        self.session.add(group2)
        self.session.commit()

        # Add user to groups
        group1.users.append(self.user)
        group2.users.append(self.user)

        retrieved_user = self.session.query(User).filter_by(
            email=self.user.email
        ).first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(len(retrieved_user.groups), 2)

    def test_user_private_msg_relationship(self):
        pass


if __name__ == "__main__":
    unittest.main()
