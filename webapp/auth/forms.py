from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, validators
from wtforms.validators import ValidationError
from webapp.models import User
from flask_babel import lazy_gettext as _l


class LoginForm(FlaskForm):
    username = StringField(_l('Utilisateur'), [validators.DataRequired()])
    password = PasswordField(_l('mot de passe'), [validators.DataRequired()])
    remember_me = BooleanField(_l('se rappeler de moi'))
    submit = SubmitField(_l('Me connecter '))


class SubscriptionForm(FlaskForm):
    username = StringField(_l('Utilisateur'), [validators.DataRequired(), validators.Length(min=5, max=15)])
    nom = StringField(_l('nom'), [validators.DataRequired()])
    prenom = StringField(_l('prenom'), [validators.DataRequired()])
    email = StringField("email",  [validators.DataRequired(), validators.Length(min=6, max=35)])
    password = PasswordField(_l('password'), [validators.DataRequired()])
    confirm = PasswordField("repeat password", [validators.EqualTo('password', message="Password must match!")])
    submit = SubmitField(_l('Envoyer'))

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_l("username deja utilisé, choisissez un autre"))
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_l("email deja utilisé, choisissez un autre"))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('mot de passe'), [validators.DataRequired()])
    password2= PasswordField(_l('Repeter votre mot de passe'),  [validators.DataRequired(),
                        validators.EqualTo('password')])
    submit =SubmitField("Submit")

class ResetPasswordRequestForm(FlaskForm):
    email = StringField("Email", [validators.DataRequired(), validators.Email()])
    submit = SubmitField("Request password reset")