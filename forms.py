from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3,max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                             validators=[DataRequired(), EqualTo('password')])
    age = IntegerField(u'Age',validators=[DataRequired()])
    sex = SelectField('Gender',choices=[("Male","Male"),("Female","Female"), ("Other","Other"), ("I don't want to share","I don't want to share")],validators=[InputRequired()])
    location = StringField("City", validators=[Length(min=-1,max=200)])
    summary =""
    profilePicture = FileField()
    isModerator = BooleanField("Are you a moderator?")
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username',
                        validators=[DataRequired()])
    password = PasswordField('Password',
                        validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    search = StringField('Search',validators=[DataRequired()])
    choice = SelectField('Filter',choices=[("museum","Museum"),("artist","Artist"),("artpiece","Artpiece"),("\"USER\"","User")],validators=[InputRequired()],render_kw = {'onchange':'myFunction()'} )
    choice_museum = SelectField('Museum Filter',choices=[("name","Name"),("location","Location")], validators=[InputRequired()])
    choice_artist = SelectField('Artist Filter',choices=[("name","Name"),], validators=[InputRequired()])
    choice_artpiece = SelectField('Art Piece Filter',choices=[("name","Name"),("museumName","Museum"),("artistName","Artist"),("era","Era"),("field","Field")], validators=[InputRequired()])
    choice_user = SelectField('User filter',choices=[("username","Username"),("location","Location")],validators=[InputRequired()])
    submit = SubmitField('Search')
