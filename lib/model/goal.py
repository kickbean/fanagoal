from google.appengine.ext import db
import models

##### goal stuff
class Goal(db.Model):
	default_collection = 'goals'
	
	subject = db.StringProperty(required = True)
	start_date = db.DateProperty(required = True)
	end_date = db.DateProperty(required = True)
	create_date = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)
	content = db.TextProperty()
	flag = db.BooleanProperty(required = True)
	author = db.ReferenceProperty(models.User, collection_name = default_collection, required = True)
	
	@classmethod
	def by_name(cls, name):
		return cls.all().filter('name =', name).run(limit = 100)