from flask import render_template, url_for,redirect
from webapp.models import User
from flask_login import login_required, current_user
from webapp.main import bp
from webapp import db

"""pour les éléments stqtiques tels que les images , les fichier css , ils sont mis , 
selon les best practices, dans un répértoire appelé static"""
#app = current_app.__get_current_object()


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    user = {'username': 'Sadia'}
    posts = [{'author': {'username': 'Amélie'}, 'body': 'Pas sympa le git avec PyCharm'},
             {'author': {'username': 'Jane'}, 'body': 'Mais non, il suffit de bien le configurer'}]


    return render_template('main/index.html', title="Page d'accueil", posts=posts)
    # return "<h1 style='color:red'> Hello, World </h1>"

@bp.route('/table')
def table():
    users = User.query.all()
    return render_template('main/table.html', title="Table", users=users)
    # return "<h1 style='color:red'> Hello, World </h1>



