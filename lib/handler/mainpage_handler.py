import handlers
from ..model import models
from ..controller.model_controller import ModelController

class MainPage(handlers.BaseHandler):
    def get(self):
        uid = self.read_secure_cookie('user_id')
        if uid:
            exist_user = ModelController.object_by_id(models.User, uid)
            if exist_user:
                self.redirect('/friends')
                return
#        self.render('fana_front.html')
        self.render('index2.html')
