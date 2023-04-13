from flask import render_template, url_for, flash, redirect, request
from blog.models.AuthModel import User
from blog.models.SubscribeModel import StripeCustomer
from blog.forms.AuthForm import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm
from blog import bcrypt, db, cfg
from flask_login import login_user, logout_user, current_user, login_required
from blog.utils.AuthUtils import send_reset_email
from flask_paginate import Pagination


class UserController:

    def user_login():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                flash("تم تسجيل الدخول بنجاح", "success")
                return redirect(request.args.get('next') or url_for('main_controller.home'))
            else:
                flash('فشل تسجيل الدخول! تأكد من كتابة البريد الإلكتروني وكلمة السر بشكل صحيح.', 'danger')
                return redirect(url_for("auth_controller.user_login"))
        return render_template('auth/login.jinja', form=form, title="تسجيل الدخول")

    def user_register():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            username = form.username.data
            login_user(user)
            flash(f'أهلا بك {username} في مدونة حسوب قم بالاشتراك حتى تتمكن من قراءة المقالات', "success")
            return redirect(url_for("main_controller.home"))
        return render_template('auth/register.jinja', form=form, title="إنشاء حساب")

    @login_required
    def user_logout():
        logout_user()
        flash("تم تسجيل الخروج", "warning")
        return redirect(url_for("main_controller.home"))

    def reset_request():
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        form = RequestResetForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            send_reset_email(user)
            flash('تم إرسال بريد إلكتروني يحوي رابط لتغيير كلمة السر', 'info')
            return redirect(url_for("auth_controller.user_login"))
        return render_template("auth/reset_request.jinja", title="إعادة تعيين كلمة السر", form=form)

    def reset_pass(token):
        if current_user.is_authenticated:
            return redirect(url_for("main_controller.home"))
        # user = User.verify_reset_token(token)
        if User.verify_reset_token(token) is None:
            flash('انتهت صلاحية الرابط، حاول مرة ثانية', 'warning')
            return redirect(url_for('auth_controller.reset_request'))
        form = ResetPasswordForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
            db.session.commit()
            flash('تم تغيير كلمة السر بنجاح، يمكنك تسجيل الدخول الآن', 'success')
            return redirect(url_for("auth_controller.user_login"))
        return render_template('auth/reset_pass.jinja', title='إعادة تعيين كلمة السر', form=form)

    @login_required
    def user_account():
        if current_user.is_admin:
            pagination = Pagination(total=len(current_user.articles))
            return render_template("auth/account.jinja", pagination=pagination)
        customer = StripeCustomer.query.filter_by(user_id=current_user.id).first()
        if customer and customer.subscription_id is not None:
            title = f"حسابي {current_user.username}"
            return render_template("auth/account.jinja", title=title, customer=customer, prices=cfg.prices)
        else:
            return render_template("auth/account.jinja")
