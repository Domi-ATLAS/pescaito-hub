from flask import render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer as Serializer
from app.modules.auth import auth_bp
from app.modules.auth.forms import SignupForm, LoginForm, PasswordRecoveryForm  # El formulario de recuperación
from app.modules.auth.services import AuthenticationService
from app.modules.profile.services import UserProfileService
from app.modules.auth.models import User  # Asumimos que el modelo de Usuario está en auth.models
from app import db

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
    s = Serializer(current_app.config['SECRET_KEY'])
    return s.dumps({'email': email})  # No necesitas `decode('utf-8')` en versiones modernas

def verify_reset_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token, max_age=600)  # Token válido por 10 minutos
    except Exception:
        return None  # Token inválido o expirado
    return data.get('email')  # Devuelve el email contenido en el token

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
from app.modules.auth.forms import SignupForm, LoginForm, PasswordRecoveryForm, ResetPasswordForm  
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
        user = User.query.filter_by(email=email).first()  # Busca el usuario en la BD
        if not user:
            flash("No existe una cuenta asociada con ese correo", "error")
            return render_template("auth/recover_password_form.html", form=form)

        # Genera el token y envía el correo
        try:
            token = generate_reset_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            msg = Message(
                'Recuperación de contraseña',
                recipients=[email],
                body=f"Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}"
            )
            mail.send(msg)
            flash("Hemos enviado un correo con las instrucciones para restablecer tu contraseña.", "success")
            return redirect(url_for('auth.password_recovery_success'))

        except Exception as e:
            flash(f"Error al enviar el correo: {e}", "error")
            return render_template("auth/recover_password_form.html", form=form)

    return render_template("auth/recover_password_form.html", form=form)


# Función para verificar el token
from werkzeug.security import generate_password_hash


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash('El token es inválido o ha expirado', 'error')
        return redirect(url_for('auth.recover_password'))

    user = User.query.filter_by(email=email).first()
    if not user:
        flash('Usuario no encontrado', 'error')
        return redirect(url_for('auth.recover_password'))

    # Crear una instancia del formulario
    form = ResetPasswordForm()

    if form.validate_on_submit():  # Validación de formulario usando Flask-WTF
        new_password = form.password.data
        user.password = generate_password_hash(new_password)  # Encripta la contraseña
        db.session.commit()
        flash('Tu contraseña ha sido actualizada exitosamente.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', form=form, token=token)

@auth_bp.route('/reset-password-static', methods=['GET', 'POST'])
def reset_password_static():
    if request.method == 'POST':
        email = request.form.get('email')
        new_password = request.form.get('new_password')

        if not email or not new_password:
            flash('Both email and password are required.', 'error')
            return render_template('auth/reset_password_static.html')

        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No user found with that email.', 'error')
            return render_template('auth/reset_password_static.html')

        try:
            user.password = generate_password_hash(new_password)  # Encripta la nueva contraseña
            db.session.commit()
            flash('Password updated successfully.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Error updating password: {e}', 'error')

    return render_template('auth/reset_password_static.html')
