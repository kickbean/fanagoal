'''
Created on Nov 13, 2012

@author: Zhixing
'''

from google.appengine.ext import db

from goal import Goal

class FreqUnit:
    Daily = "day"
    Weekly = "week"
    Monthly = "month"
    
class WeeklyList:
    @classmethod
    def isValidStr(cls, weekly_list):
        if (not isinstance(weekly_list, str)) or (len(weekly_list) != 7):
            return False
        for day in weekly_list:
            if (day not in ('0', '1')):
                return False
    
    @classmethod
    def cvtListToStr(cls, weekly_list):
        if (len(weekly_list) == 7):
            return ''.join(weekly_list)
        else:
            return None

##### task stuff
class Task(db.Model):
    default_collection = 'tasks'
     
    name = db.StringProperty(required = True)
    goal = db.ReferenceProperty(Goal, collection_name = default_collection, required = True)
    start_date = db.DateProperty(required = True)
    end_date = db.DateProperty(required = True)
    freq_unit = db.StringProperty(required = True)
    freq_value = db.IntegerProperty(required = True)
    create_date = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    weekly_list = db.StringProperty()
    note = db.TextProperty()
    
    @classmethod
    def by_name(cls, name):
        return cls.all().filter('name =', name).run(limit = 100)
    
#    @classmethod
#    def create(self, parent, name, goal, start_date, end_date, freq_unit, freq_value, weekly_list, note):
#        super(Task, self).__init__(parent)
#        self.name = name
#        self.goal = goal
#        self.start_date = start_date
#        self.end_date = end_date
#        self.freq_unit = freq_unit
#        self.freq_value = freq_value
#        if freq_unit == FreqUnit.Weekly:
#            self.weekly_list = weekly_list
#        if note is not None:
#            self.note = note
