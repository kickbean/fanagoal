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

class SettingFront(handlers.BaseHandler):
  def get(self):
    self.render('setting.html')