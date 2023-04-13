import json
from flask_mail import Message
from blog import cfg, mail, db
from flask import url_for
from datetime import date
from dateutil.relativedelta import relativedelta
from sqlalchemy import func
from operator import and_, itemgetter
from blog.models.SubscribeModel import StripeCustomer
import plotly
import plotly.graph_objects as go


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request", sender=cfg.RESET_MAIL, recipients=[user.email])
    msg.body = f'''{url_for("auth_controller.reset_pass", token=token, _external=True)}  :لاستعادة كلمة السر اضغط على الرابط التالي '''
    mail.send(msg)


def monthly_subscriber_info():
    month_first_day = date.today().replace(day=1)
    start_previous_month = month_first_day - relativedelta(months=1)
    end_previous_month = month_first_day - relativedelta(days=1)
    month_subs = StripeCustomer.query.filter(func.date(StripeCustomer.subscription_start) > end_previous_month).all()
    month_subs_count = len(month_subs)
    month_subs_sum = sum([x.amount for x in month_subs])
    previous_month_sub = StripeCustomer.query.filter(and_(StripeCustomer.subscription_start >= start_previous_month,
                                                          StripeCustomer.subscription_start <= end_previous_month)).all()
    previous_subs_count = len(previous_month_sub)
    previous_month_sum = sum([x.amount for x in previous_month_sub])
    total_sum = db.session.query(func.sum(StripeCustomer.amount)).first()[0]
    total_count = db.session.query(func.count(StripeCustomer.status)).first()[0]

    month_sum_percentage = get_change(month_subs_sum, previous_month_sum)
    month_count_percentage = get_change(month_subs_count, previous_subs_count)
    total_count_percentage = get_change(month_subs_count, total_count)
    total_sum_percentage = get_change(month_subs_sum, total_sum)

    return {
        "month_subs_sum": month_subs_sum,
        "month_subs_count": month_subs_count,
        "total_count": total_count,
        "total_sum": total_sum,
        "month_sum_percentage": month_sum_percentage,
        "month_count_percentage": month_count_percentage,
        "total_count_percentage": total_count_percentage,
        "total_sum_percentage": total_sum_percentage
    }


def get_change(current, previous):
    try:
        if previous is None:
            previous = 0
        if current == previous:
            return 0
        percentage_change = int(((float(current) - previous) / previous) * 100)
        return percentage_change
    except ZeroDivisionError:
        return 0


def subscriber_plot():
    list_sub_year = db.session.query(func.date(StripeCustomer.subscription_start),
                                     func.count(StripeCustomer.subscription_start)).filter(
        StripeCustomer.subscription_type == "year").group_by(func.date(StripeCustomer.subscription_start)).all()
    list_sub_month = db.session.query(func.date(StripeCustomer.subscription_start),
                                      func.count(StripeCustomer.subscription_start)).filter(
        StripeCustomer.subscription_type == "month").group_by(func.date(StripeCustomer.subscription_start)).all()

    list_sub_year.sort(key=itemgetter(0))
    list_sub_month.sort(key=itemgetter(0))

    x_year = []
    y_year = []
    x_month = []
    y_month = []

    for data in list_sub_year:
        x_year.append(data[0])
        y_year.append(data[1])
    for data in list_sub_month:
        x_month.append(data[0])
        y_month.append(data[1])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_year, y=y_year, line_shape='spline', name='اشتراكات سنوية'))
    fig.add_trace(go.Scatter(x=x_month, y=y_month, line_shape='spline', name='اشتراكات شهرية'))

    fig.update_layout(
        xaxis=dict(rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graph_json
