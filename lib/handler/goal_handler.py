import logging
from datetime import datetime

import handlers
from ..model import goal
from ..model import task
from ..model import models
from ..controller.model_controller import ModelController
from ..controller.goal_controller import GoalController

class GoalFront(handlers.BaseHandler):
	def get(self):
#		uid = self.read_secure_cookie('user_id')
#		exist_user = ModelController.object_by_id(models.User, uid)
		
		if not self.user:
			self.error(404)
			return
		
		goals = ModelController.get_list_iter(self.user, goal.Goal, '-create_date')
		logging.warning(goals)
		for g in goals:
			g._render_text = g.content.replace('\n', '<br>')
		
		self.render('myGoal2.html', goals = goals)
		
	def post(self):
		action = self.request.get('create')
		logging.warning(action)
		if action=='newgoal':
			GoalController.create(self)
		
class GoalPage(handlers.BaseHandler):
	def get(self, goal_id):
		self.goal = ModelController.object_by_id(goal.Goal, goal_id)
		if not self.goal:
			self.error(404)
			return

#		logging.error(post.subject)	# for debug
		self.goal._render_text = self.goal.content.replace('\n', '<br>')
		
		tasks = ModelController.get_list_iter(self.goal, task.Task, 'create_date')
		for t in tasks:
			t._render_text = t.note.replace('\n', '<br>')
			t.goallen = (self.goal.end_date - self.goal.start_date).days + 1
			t.taskstart = (t.start_date - self.goal.start_date).days
			t.tasklen = (t.end_date - t.start_date).days + 1
		
		self.render("goal_permalink2.html", p = self.goal, tasks = tasks)
		
	def post(self, goal_id):
		if not self.user:
			self.redirect('')
			
		action = self.request.get('create')
		if action=='newgoal':
			GoalController.create(self)
			return
		
		if not self.goal:
			self.error(404)
			return	
			
		self.goal.flag = True
		ModelController.add_object(self.goal)
		ModelController.update_mc_list(self.user, self.goal, '-create_date')
		self.goal._render_text = self.goal.content.replace('\n', '<br>')
		self.render("goal_permalink2.html", p = self.goal)
		
class GoalCreate(handlers.BaseHandler):
	def get(self):
		if self.user:
			self.render("goal_create.html")
		else:
			self.redirect("/login")

	def post(self):
		GoalController.create(self)

class GoalEdit(handlers.BaseHandler):
	def get(self):
		if self.user:
			gid = self.request.get('gid')
			g = ModelController.object_by_id(goal.Goal, gid)
			logging.warning(g.subject)
			logging.warning(g.content)
			self.render("goal_create.html", 
					subject=g.subject, 
					start_date=g.start_date,
					end_date=g.end_date,
					content=g.content)
		else:
			self.redirect("/login")
	
	def post(self):
		gid = self.request.get('gid')
		GoalController.update(self,gid)