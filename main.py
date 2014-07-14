from lib.handler import goal_handler
from lib.handler import signup_handler
from lib.handler import act_handler
from lib.handler import mainpage_handler
from lib.handler import friend_handler
from lib.handler import task_handler
from lib.handler import hotPlan_handler
from lib.handler import setting_handler

import webapp2

app = webapp2.WSGIApplication([('/', mainpage_handler.MainPage),
                               ('/friends', friend_handler.Friends),
                               ('/activity', act_handler.ActivityFront),
                               ('/activity/([0-9]+)', act_handler.PostPage),
                               ('/activity/newpost', act_handler.NewPost),          
                               ('/signup', signup_handler.Register),
                               ('/login', signup_handler.Login),
                               ('/logout', signup_handler.Logout),
                               ('/goal', goal_handler.GoalFront),
                               ('/goal/newgoal', goal_handler.GoalCreate),
                               ('/goal/([0-9]+)', goal_handler.GoalPage),
                               ('/goal/edit', goal_handler.GoalEdit),
                               ('/task/create', task_handler.TaskCreate),
                               ('/task/edit', task_handler.TaskEdit),
                               ('/task/([0-9]+)', task_handler.TaskPage),
                               ('/hotPlans', hotPlan_handler.PlanFront),
                               ('/setting', setting_handler.SettingFront)
                               ]
                              ,debug=True)
