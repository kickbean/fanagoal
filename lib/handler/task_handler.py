'''
Created on Nov 6, 2012

@author: Zhixing
'''
import handlers
import goal_handler

import logging

from datetime import datetime
from ..model import task
from ..model import goal
from ..controller.model_controller import ModelController
from ..controller.goal_controller import GoalController
from ..controller.task_controller import TaskController


class TaskPage(handlers.BaseHandler):
	def get(self, task_id):
		currTask = ModelController.object_by_id(task.Task, task_id)

		if not currTask:
			self.error(404)
			return

#		logging.error(post.subject)	# for debug
		currTask._render_text = currTask.note.replace('\n', '<br>')
		self.render("task_permalink2.html", p = currTask)

class TaskCreate(handlers.BaseHandler):
	def get(self):
		if self.user:
			self.render("task_create3.html")
		else:
			self.redirect("/login")
			
	def post(self):
		TaskController.create(self)

class TaskEdit(handlers.BaseHandler):
	def get(self):
		if self.user:
			tid = self.request.get("tid")
			t = ModelController.object_by_id(task.Task, tid)
			self.render("task_create3.html", name=t.name, 
					freq_value=t.freq_value,
					freq_unit=t.freq_unit,
					start_date=t.start_date,
					end_date=t.end_date,
					note=t.note)
		else:
			self.redirect("/login")
	
	def post(self):
		tid = self.request.get('tid')
		TaskController.update(self, tid)