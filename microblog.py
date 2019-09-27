from webapp import create_app, db
from webapp.models import User, Post
#from webapp import cli


app = create_app()
#cli.register(app)
@app.shell_context_processor
def make_shell_context():
     return {'dbase': db , 'User': User , ' Post': Post}