import logging
from google.appengine.ext import db

import handlers
from ..controller.model_controller import ModelController
from ..model import models

##### post stuff
def activity_key(name = 'default'):
	return db.Key.from_path('activities', name)

class ActivityFront(handlers.BaseHandler):
	def get(self):
		uid = self.read_secure_cookie('user_id')
		exist_user = ModelController.object_by_id(models.User, uid)
		
		if not exist_user:
			self.error(404)
			return
		
		posts = ModelController.get_list_iter(exist_user, models.Post, '-created')
		logging.warning(type(posts))
		for p in posts:
			logging.warning(type(p))
			p._render_text = p.content.replace('\n', '<br>')
			
		self.render('myPost2.html', posts = posts)

class PostPage(handlers.BaseHandler):
	def get(self, post_id):
		post = ModelController.object_by_id(models.Post, post_id)
		
		if not post:
			self.error(404)
			return
		
#		logging.error(post.subject)	# for debug
		post._render_text = post.content.replace('\n', '<br>')
		self.render("myPost_permalink.html", p = post)

class NewPost(handlers.BaseHandler):
	def get(self):
		if self.user:
			self.render("createPost.html")
		else:
			self.redirect("/login")
	
	def post(self):
		if not self.user:
			self.redirect('/')
		
		uid = self.read_secure_cookie('user_id')
		exist_user = ModelController.object_by_id(models.User, uid)
		subject = self.request.get('subject')
		content = self.request.get('content')
		
		if subject and content:
			p = models.Post(parent = activity_key(), subject = subject, \
							content = content, author = exist_user)
			pid = ModelController.add_object(p)
			ModelController.update_mc_list(exist_user, p, '-created') # update the memcache for all posts
			self.redirect('/activity/%s' % pid)
		else:
			error = "subject and content, please!"
			self.render("createPost.html", subject=subject, content=content, error=error)
