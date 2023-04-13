from flask_login import login_required, current_user
from blog import cfg, stripe, db
from flask import render_template, flash, redirect, url_for
from blog.models.AuthModel import User
from blog.models.SubscribeModel import StripeCustomer
from blog.utils.AuthUtils import monthly_subscriber_info, subscriber_plot
from blog.utils.MainUtils import Paginate


class AdminController:

    @login_required
    def users_control():
        if current_user.username == cfg.OWNER_USERNAME:
            pagination, users_list = Paginate(cfg.USERS_PER_PAGE, User, User.id.desc())
            return render_template('auth/users_control.jinja', title='المستخدمين', users_list=users_list,
                                   pagination=pagination)

    @login_required
    def role_grant(user_id):
        user = User.query.get_or_404(user_id)
        if user.username == cfg.OWNER_USERNAME:
            flash(f'العملية غير ممكنة', 'warning')
            return redirect(url_for('auth_controller.users_control'))
        if current_user.username == cfg.OWNER_USERNAME:
            if user.is_admin:
                flash(f'المستخدم {user.username} يملك صلاحية الإدارة مسبقاً', 'warning')
                return redirect(url_for('auth_controller.users_control'))
            customer = StripeCustomer.query.filter_by(user_id=user.id).first()
            if customer:
                stripe.Subscription.delete(customer.subscription_id)
                StripeCustomer.query.filter(StripeCustomer.customer_id == customer.customer_id).delete()
            user.is_admin = True
            db.session.commit()
            flash(f'تم منح صلاحية الإدارة للمستخدم {user.username}', 'warning')
            return redirect(url_for('auth_controller.users_control'))
        else:
            flash(f'العملية غير ممكنة', 'warning')
            return redirect(url_for('main_controller.home'))

    @login_required
    def role_revoke(user_id):
        user = User.query.get_or_404(user_id)
        if user.username == cfg.OWNER_USERNAME:
            flash(f'العملية غير ممكنة', 'warning')
            return redirect(url_for('auth_controller.users_control'))
        if current_user.username == cfg.OWNER_USERNAME:
            if user.is_admin:
                user.is_admin = False
                db.session.commit()
                flash(f'تم سحب صلاحية الإدارة من المستخدم {user.username}', 'warning')
            else:
                flash(f'المستخدم {user.username} لايملك صلاحية الإدارة', 'warning')
            return redirect(url_for('auth_controller.users_control'))
        else:
            flash(f'العملية غير ممكنة', 'warning')
            return redirect(url_for('main_controller.home'))

    @login_required
    def sub_panel():
        if current_user.username == cfg.OWNER_USERNAME:
            monthly_data = monthly_subscriber_info()
            graph_json = subscriber_plot()
            return render_template('auth/sub_panel.jinja', monthly_data=monthly_data, graph_json=graph_json,
                                   title='لوحة التحكم')
        else:
            flash('لاتملك صلاحية الوصول للصفحة المطلوبة', 'warning')
            return redirect(url_for('main_controller.home'))
