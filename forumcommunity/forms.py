from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from forumcommunity.models import User
from flask_login import current_user


class FormRegister(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(3,15)])
    c_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    btn_register = SubmitField('Sign Up')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()           # Validation for existing email. Check when registering.
        if user:
            raise ValidationError('This email is already being used, try another one.')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(3,15)])
    remember = BooleanField('Remember')
    btn_login = SubmitField('Sign in')



class FormEdit(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    picture = FileField('Update photo', validators=[FileAllowed(['jpg', 'png'])])

    sk_python = BooleanField('Python')
    sk_js = BooleanField('JavaScript')
    sk_java = BooleanField('Java')
    sk_sql = BooleanField('SQL')
    sk_powerbi = BooleanField('Power BI')
    sk_php = BooleanField('PHP')
    sk_go = BooleanField('GO')
    sk_ruby = BooleanField('Ruby')
    sk_c = BooleanField('C#')
    sk_cc = BooleanField('C++')
    sk_swift = BooleanField('Swift')

    btn_edit = SubmitField('Edit Profile')

    def validate_email(self, email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()          
            if user:
                raise ValidationError('This email is already being used, try another one.')



class FormPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(2,400)])
    body = TextAreaField('Write your post', validators=[DataRequired()])
    btn_post = SubmitField('Create')

