'''
Created on Dec 2, 2012

@author: songfanyang
'''

import logging
from datetime import datetime

import handlers
from ..model import goal
from ..model import task
from ..model import models
from ..controller.model_controller import ModelController
from ..controller.goal_controller import GoalController

class PlanFront(handlers.BaseHandler):
#    def get(self):
#        admin_goal = ModelController.object_by_id(models.User, 1)
#        goals = ModelController.get_list_iter(admin_goal, goal.Goal, '-create_date')
#        logging.warning(len(goals))
#        for g in goals:
#            g._render_text = g.content.replace('\n', '<br>')
#        
#        self.render('hotPlans2.html', goals = goals)  
        
    def get(self):
        self.render('hotPlans.html')

    