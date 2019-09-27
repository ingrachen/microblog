
from flask import request
from flask import render_template, flash, redirect, url_for
from webapp.auth.forms import LoginForm, SubscriptionForm, ResetPasswordRequestForm, ResetPasswordForm
from werkzeug.urls import url_parse
from webapp.models import User
from flask_login import current_user, login_user, logout_user
import datetime
from webapp.auth.email import send_password_reset_email
from flask_babel import _
from webapp.auth import bp
from webapp import db

@bp.route('/')
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:

        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Login ou mot de passe invalide'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Authentification', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/inscription', methods=['GET', 'POST'])
def inscription():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    inscript_form = SubscriptionForm()
    if inscript_form.validate_on_submit():
        user = User(username=inscript_form.username.data, nom=inscript_form.nom.data,
                    prenom=inscript_form.prenom.data, email=inscript_form.email.data)
        user.set_password(inscript_form.password.data)
        db.session.add(user)
        db.session.commit()
        print("add user", user)
        # verifier que user n'existe pas deja
        flash(_('You are subscribed now! you can log in now to access your account!!'))
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('auth.login')
        return redirect(next_page)
    return render_template('auth/inscription.html', title='Inscription', inscript_form=inscript_form)


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        #print("ooooooooooooook", user)
        if user:
            send_password_reset_email(user)
        flash(_('consultez votre email et suivez les instructions'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html', form=form)

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset '))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.app_template_filter('format_date')
def format_date(text):
    if isinstance(text, datetime.datetime):
        return text.strftime("%d/%m/%Y")
    return text