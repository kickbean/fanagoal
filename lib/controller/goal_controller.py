'''
Created on Nov 29, 2012

@author: Songfan
'''
from model_controller import ModelController
import logging

from datetime import datetime
from ..model import models
from ..model import goal

class GoalController(ModelController):
    @classmethod
    def create(cls, page):
        if not page.user:
            page.redirect('/')
        
        uid = page.read_secure_cookie('user_id')
        exist_user = cls.object_by_id(models.User, uid)
        subject = page.request.get('subject')
        start_date_raw = page.request.get('start_date')
        end_date_raw = page.request.get('end_date')
        content = page.request.get('content')
        flag = False
        
        
        if subject and start_date_raw and end_date_raw and content:
            start_date = datetime.strptime(start_date_raw, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date_raw, "%m/%d/%Y").date()
            g = goal.Goal(parent = ModelController.object_parent(goal.Goal), subject = subject,
                          start_date = start_date, end_date = end_date,
                          content = content, author = exist_user, flag = flag)
            gid = cls.add_object(g)
            cls.update_mc_list(page.user, g, '-create_date') # update the memcache for all posts
            page.redirect('/goal/%s' % gid)
        else:
            error = "Please specify the subject, start date, end date and description!"
            page.render("goal_create.html", subject=subject, content=content, error=error)
  
    @classmethod
    def update(cls, page, goal_id):
        if not page.user:
            page.redirect('/')
        
        subject = page.request.get('subject')
        start_date_raw = page.request.get('start_date')
        end_date_raw = page.request.get('end_date')
        content = page.request.get('content')
        
        
        if subject and start_date_raw and end_date_raw and content:
            start_date = datetime.strptime(start_date_raw, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date_raw, "%m/%d/%Y").date()
            g = ModelController.object_by_id(goal.Goal, goal_id)
            g.subject = subject;
            g.start_date = start_date;
            g.end_date = end_date;
            gid = cls.add_object(g)
            cls.update_mc_list(page.user, g, '-create_date') # update the memcache for all posts
            page.redirect('/goal/%s' % gid)
        else:
            error = "Please specify the subject, start date, end date and description!"
            page.render("goal_create.html", subject=subject, content=content, error=error)
  