import handlers
class Friends(handlers.BaseHandler):
    def get(self):
        self.render('friends2.html')
