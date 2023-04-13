from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from blog.models.AuthModel import User


class LoginForm(FlaskForm):
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email()])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    remember = BooleanField('تذكرني')
    submit = SubmitField("تسجيل الدخول")


class RegistrationForm(FlaskForm):
    username = StringField("اسم المستخدم", validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email(message="البريد غير صالح")])
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    confirm_password = PasswordField("تأكيد كلمة السر", validators=[DataRequired(), EqualTo('password',
                                                                                            message="يجب أن يتطابق حقل كلمة السر مع تأكيد كلمة السر")])
    submit = SubmitField("تسجيل الدخول")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('البريد الإلكتروني موجود مسبقا. قم باستعادة كلمة السر في حال نسيانها.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('يجب أن يكون اسم المستخدم فريد، قم باختيار اسم آخر')


class RequestResetForm(FlaskForm):
    email = StringField("البريد الالكتروني", validators=[DataRequired(), Email()])
    submit = SubmitField("استعادة كلمة السر")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('لا يوجد بريد إلكتروني مسجل بهذا الاسم')


class ResetPasswordForm(FlaskForm):
    password = PasswordField("كلمة السر", validators=[DataRequired()])
    confirm_password = PasswordField("تأكيد كلمة السر", validators=[DataRequired(), EqualTo('password',
                                                                                            message="يجب أن يتطابق حقل كلمة السر مع تأكيد كلمة السر")])
    submit = SubmitField("تغيير كلمة السر")
