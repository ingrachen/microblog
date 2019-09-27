from webapp import login
from webapp import db as dbase
from flask import url_for
from flask import current_app
from datetime import datetime
from time import time
import jwt
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            'meta': {
                'page': page,
                'per_page': resources.pages,
                'total_items': resources.total
            },
            '_link': {'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                      'next': url_for(endpoint,page=page+1, per_page=per_page,
                                      **kwargs) if resources.has_next else None,
                      'prev': url_for(endpoint, page=page-1, per_page=per_page,
                                      **kwargs) if resources.has_prev else None
                      }
        }
        return data


class User(PaginatedAPIMixin, UserMixin, dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    username = dbase.Column(dbase.String(40), index=True, unique=True)
    nom = dbase.Column(dbase.String(40), index=True, unique=True)
    prenom = dbase.Column(dbase.String(40), index=True, unique=True)
    email = dbase.Column(dbase.String(40), index=True, unique=True)
    password_hash = dbase.Column(dbase.String(120))
    role = dbase.Column(dbase.Enum('admin', 'conseiller', 'client'))
    posts = dbase.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.username)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'post_count': self.posts.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.set_password(data['password'])

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if check_password_hash(self.password_hash, password):
            return True
        else:
            return False

    def get_content(self):
        return self.id, self.username, self.email

    def get_reset_password_token(self, expires_in=60):

        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):

        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Post(dbase.Model):
    id = dbase.Column(dbase.Integer, primary_key=True)
    body = dbase.Column(dbase.String(40))
    timestamp = dbase.Column(dbase.DateTime, index=True, default=datetime.utcnow)
    user_id= dbase.Column(dbase.Integer, dbase.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)




"""class Conseiller(UserMixin, dbase.Model):
    mle = dbase.Column(dbase.Integer, primaty_key=True)
    login = dbase.Column(dbase.String(40))
    date_debut = dbase.Column(dbase.DateTime)
    date_fin = dbase.Column(dbase.DateTime)"""



@login.user_loader
def load_user(id):
    return User.query.get(int(id))