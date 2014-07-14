import random
import hashlib
from string import letters

from google.appengine.ext import db

##### user stuff
class User(db.Model):
    email = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True)
    firstname = db.StringProperty(required = True)
    lastname = db.StringProperty(required = True)
    
    @classmethod
    def by_email(cls, email):
        u = cls.all().filter('email =', email).get()
        return u
    
    @classmethod
    def make_salt(cls, length = 5):
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_pw_hash(cls, email, pw, salt = None):
        if not salt:
            salt = User.make_salt()
        h = hashlib.sha256(email + pw + salt).hexdigest()
        return '%s,%s' % (salt, h)
    
    @classmethod
    def valid_pw(cls, email, password, h):
        salt = h.split(',')[0]
        return h == User.make_pw_hash(email, password, salt)
    
##    @classmethod
#    def register(cls, email, pw):
#        pw_hash = cls.make_pw_hash(email, pw)
#        return cls(parent = cls.user_parent(),
#                    email = email,
#                    pw_hash = pw_hash)
    
    @classmethod
    def login(cls, email, pw):
        u = cls.by_email(email)
        if u and cls.valid_pw(email, pw, u.pw_hash):
            return u

class Post(db.Model):
    default_collection = 'posts'
    
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    author = db.ReferenceProperty(User, collection_name = default_collection, required = True)
