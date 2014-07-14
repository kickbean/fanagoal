import re
import logging

import handlers
from ..model import models
from ..controller.model_controller import ModelController

PASS_RE = re.compile(r"^.{6,20}$")
def valid_password(password):
	return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
#	logging.warning(email)
	return email and EMAIL_RE.match(email)

NAME_RE = re.compile(r"^[a-zA-Z]+$")
def valid_name(name):
	return name and NAME_RE.match(name)

class Signup(handlers.BaseHandler):
	def get(self):
		self.render("signup.html")
	
	def post(self):
		have_error = False
		
		self.email = self.request.get('email')
		self.password = self.request.get('password')
		self.firstname = self.request.get('firstname')
		self.lastname = self.request.get('lastname')
		
		params = dict(email = self.email,
					  firstname = self.firstname,
					  lastname = self.lastname)

		if not valid_name(self.firstname) or not valid_name(self.lastname):
			params['error_msg'] = "The name seems not correct."
			have_error = True
		
		if not valid_password(self.password):
			params['error_msg'] = "Choose password longer than 6 digits."
			have_error = True
		
		if not valid_email(self.email):
			params['error_msg'] = "That's not a valid email."
			have_error = True
		
		if have_error:
			self.render('signup.html', **params)
		else:
			self.done()
	
	def done(self, *a, **kw):
		raise NotImplementedError


class Register(Signup):
	def done(self):
		#make sure the user doesn't already exist
		u = models.User.by_email(self.email)
		if u:
			msg = 'That email already exists.'
			self.render('signup.html', error_msg = msg)
		else:
			u = models.User(parent = ModelController.object_parent(models.User), 
							email = self.email, 
							pw_hash = models.User.make_pw_hash(self.email, self.password),
							firstname = self.firstname,
							lastname = self.lastname)
			ModelController.add_object(u)
			
			self.login(u)
			logging.info('Adding account='+self.email)
			self.redirect('/goal')

class Login(handlers.BaseHandler):
	def get(self):
		self.render('login.html')
	
	def post(self):
		email = self.request.get('email')
		password = self.request.get('password')
		
		if email and password:
			u = models.User.login(email, password)
			if u:
				self.login(u)
				self.redirect('/goal')
				return
		
		msg = 'Invalid login'
		self.render('login.html', email = email, error_msg = msg)

class Logout(handlers.BaseHandler):
	def get(self):
		self.logout()
		self.redirect('/')
