from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_user, logout_user
from itsdangerous import TimedSerializer as Serializer
from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, PasswordRecoveryForm  # El formulario de recuperación
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User  # Asumimos que el modelo de Usuario está en auth.models

# Configuración
authentication_service = AuthenticationService()
user_profile_service = UserProfileService()


@auth_bp.route("/signup/", methods=["GET", "POST"])
def show_signup_form():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = SignupForm()
    if form.validate_on_submit():
        email = form.email.data
        if not authentication_service.is_email_available(email):
            return render_template("auth/signup_form.html", form=form, error=f'Email {email} in use')

        try:
            user = authentication_service.create_with_profile(**form.data)
        except Exception as exc:
            return render_template("auth/signup_form.html", form=form, error=f'Error creating user: {exc}')

        # Log user
        login_user(user, remember=True)
        return redirect(url_for('public.index'))

    return render_template("auth/signup_form.html", form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.index'))

    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        if authentication_service.login(form.email.data, form.password.data):
            return redirect(url_for('public.index'))

        return render_template("auth/login_form.html", form=form, error='Invalid credentials')

    return render_template('auth/login_form.html', form=form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.index'))

# Función para generar el token
def generate_reset_token(email):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=600)  # 10 minutos de expiración
    return s.dumps({'email': email}).decode('utf-8')

# Función para enviar el correo con el enlace de recuperación
def send_reset_email(user_email):
    token = generate_reset_token(user_email)
    reset_url = url_for('auth.reset_password', token=token, _external=True)  # El enlace para la recuperación

    msg = Message('Password Reset Request', recipients=[user_email])
    msg.body = f'Please click the following link to reset your password: {reset_url}'
    
    try:
        mail.send(msg)  # Enviar el correo
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# app/modules/auth/routes.py
from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from app import mail  # Importar mail aquí, donde lo necesitamos

from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, PasswordRecoveryForm
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from flask_mail import Message  # Para enviar el correo

authentication_service = AuthenticationService()
user_profile_service = UserProfileService()

# Ruta para recuperación de contraseña
@auth_bp.route('/recover_password', methods=['GET', 'POST'])
def recover_password():
    form = PasswordRecoveryForm()

    if form.validate_on_submit():
        email = form.email.data
        # Enviar correo de recuperación de contraseña
        try:
            msg = Message('Recuperación de contraseña',
                          recipients=[email])
            msg.body = "Este es un correo para la recuperación de tu contraseña."
            mail.send(msg)  # Usamos mail aquí
            return redirect(url_for('auth.password_recovery_success'))
        except Exception as e:
            return render_template("auth/recover_password_form.html", form=form, error=str(e))

    return render_template("auth/recover_password_form.html", form=form)

# Función para verificar el token
def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except:
        return None  # Token inválido o expirado
    return data['email']


# Ruta para resetear la contraseña
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('That is an invalid or expired token', 'error')
        return redirect(url_for('auth.recover_password'))

    user = User.query.filter_by(email=email).first()  # Obtén el usuario por correo
    if request.method == 'POST':
        new_password = request.form['password']  # La nueva contraseña que el usuario ingresa
        user.password = new_password  # Aquí deberías encriptar la contraseña antes de guardarla
        db.session.commit()  # Guarda la nueva contraseña en la base de datos
        flash('Your password has been updated!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)  # Muestra el formulario para cambiar la contraseña
