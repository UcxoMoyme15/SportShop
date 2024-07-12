from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, IntegerField
from wtforms.validators import DataRequired, length, equal_to, ValidationError
from flask_wtf.file import FileField, FileSize, FileAllowed
from models import User

class RegisterForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), length(min=8, max=20)])
    repeat_password = PasswordField("Repeat Password", validators=[DataRequired(), equal_to("password")])
    email = EmailField("Enter Email", validators=[DataRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    username = StringField("Enter Username", validators=[DataRequired()])
    password = PasswordField("Enter Password", validators=[DataRequired(), length(min=8, max=20)])
    login = SubmitField("Log in")

class ProductForm(FlaskForm):
    img = FileField("Product's Picture", validators=[FileAllowed(["jpg", "png"], FileSize)])
    name = StringField("Product's name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    submit = SubmitField("Add Product")
