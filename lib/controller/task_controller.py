'''
Created on Dec 12, 2012

@author: songfanyang
'''
from model_controller import ModelController
import logging

from datetime import datetime
from ..model import models
from ..model import goal
from ..model import task

class TaskController(ModelController):
    @classmethod
    def create(cls,page):
        if not page.user:
            page.redirect("/")
        
        gid = page.request.get('gid')
        page.goal = ModelController.object_by_id(goal.Goal, gid)
        name = page.request.get('name')
        start_date_raw = page.request.get('start_date')
        end_date_raw = page.request.get('end_date')

        freq_unit = page.request.get('freq_unit')
        freq_value_raw = page.request.get('freq_value')
        weekly_list = None
        note = page.request.get('note')
        
        if freq_unit == task.FreqUnit.Weekly:
            weekly_list = task.WeeklyList.cvtListToStr(page.request.get('weekly_list'))

        if name and start_date_raw and end_date_raw and freq_value_raw:         
            start_date = datetime.strptime(start_date_raw, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date_raw, "%m/%d/%Y").date()
            freq_value = int(freq_value_raw)
            if start_date>=page.goal.start_date and end_date<=page.goal.end_date:
                newTask = task.Task(parent = ModelController.object_parent(task.Task),
                            name = name,
                            goal = page.goal,    #suppose the current goal is saved
                            start_date = start_date,
                            end_date = end_date,
                            freq_unit = freq_unit,
                            freq_value = freq_value,
                            weekly_list = weekly_list,
                            note = note)
                tid = ModelController.add_object(newTask)
                ModelController.update_mc_list(page.goal, newTask, 'create_date')
                page.redirect("/goal/%s" % gid)
            else:
                error = "task date cannot exceed the span of this goal"
                page.render("task_create3.html", 
                        name=name, 
                        note=note, 
                        error_task=error)
        else:
            error = "Please specify the task name, start date, and end date!"
            page.render("task_create3.html", 
                        name=name, 
                        note=note, 
                        error_task=error)
  
    @classmethod
    def update(cls,page,task_id):
        if not page.user:
            page.redirect("/")
        
        name = page.request.get('name')
        start_date_raw = page.request.get('start_date')
        end_date_raw = page.request.get('end_date')

        freq_unit = page.request.get('freq_unit')
        freq_value = int(page.request.get('freq_value'))
        weekly_list = None
        note = page.request.get('note')
        
        if freq_unit == task.FreqUnit.Weekly:
            weekly_list = task.WeeklyList.cvtListToStr(page.request.get('weekly_list'))

        if name and start_date_raw and end_date_raw:
            logging.warning(start_date_raw)
#            start_date = datetime.strptime(start_date_raw, "%m/%d/%Y").date()
            start_date = datetime.strptime(start_date_raw, "%m/%d/%Y").date()
            end_date = datetime.strptime(end_date_raw, "%m/%d/%Y").date()
            
            t = ModelController.object_by_id(task.Task, task_id)
            t.name = name
            t.start_date = start_date
            t.end_date = end_date
            t.freq_unit = freq_unit
            t.freq_value = freq_value
            t.weekly_list = weekly_list
            t.note = note
            cls.add_object(t)
            page.redirect("/task/%s" % task_id)
        else:
            error = "Please specify the task name, start date, and end date!"
            page.render("task_create3.html", name=name, note=note, error_task=error)          