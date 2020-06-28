"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_message_model.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes
from sqlalchemy import exc

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app


app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True
# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

sess = db.session


class MessageModelTestCase(TestCase):
    """Test Message model."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u = User.signup("test3", "email1@email.com", "password", None)
        u.id = 111
        sess.commit()

        self.u = User.query.get(111)
        self.test_id = 111

        m1 = Message(text="trending warble", user_id=self.test_id)
        m2 = Message(text="Eating some lunch", user_id=self.test_id)

        sess.add_all([m1, m2])
        sess.commit()

        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        sess.rollback()
        return res

    def test_message_model(self):
        """Does basic model work?"""

        m = Message(text="aaaaaa", user_id=111)
        m.id = self.test_id
        sess.add(m)
        sess.commit()

        m = Message.query.get(111)
        self.assertEqual(m.text, "aaaaaa")
        self.assertIsNotNone(m.timestamp)
        self.assertEqual(m.user_id, self.test_id)

        #User should have 3 message
        self.assertEqual(len(self.u.messages), 3)
        self.assertEqual(self.u.messages[2].text, "aaaaaa")

    def test_like_new_message(self):
        """Test liking a message from a user"""

        m = Message(id=2222, text="round and round0", user_id=self.test_id)
        sess.add(m)
        sess.commit()

        u = User.query.get(111)

        u.likes.append(m)
        sess.commit()

        l = Likes.query.filter(Likes.user_id == 111).all()
        self.assertEqual(len(l), 1)
        self.assertEqual(l[0].message_id, 2222)





