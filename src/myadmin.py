from flask import redirect, url_for, flash
from flask_admin import AdminIndexView, expose
from flask_login import current_user




class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if current_user.is_authenticated:
            id = current_user.user_id
            if id == 1:
              return super(MyAdminIndexView, self).index()  
        if not current_user.is_authenticated:
            flash('U have to be Admin to do Admin things')
            return redirect(url_for('login'))
        else:
            flash('U have to be Admin to do Admin things')
            return redirect(url_for('dashboard'))
