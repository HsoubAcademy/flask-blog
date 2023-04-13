from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileAllowed
from flask_ckeditor import CKEditorField


class ArticleForm(FlaskForm):
    title = StringField("عنوان المقالة", validators=[DataRequired(), Length(min=5, max=255)])
    article_img = FileField("صورة المقالة", validators=[FileAllowed(['jpg', 'png'])])
    content = CKEditorField("محتوى المقالة", validators=[DataRequired(), Length(min=100, max=10000)])
    submit = SubmitField("نشر المقالة")
