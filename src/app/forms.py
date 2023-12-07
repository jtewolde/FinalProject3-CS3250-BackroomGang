'''
CS3250 - Software Development Methods and Tools - Fall 2023
Project 03- Video Playlist Manager Web Application
Description: This forms.py file is meant for implementing the forms for the application
Group Name: Backroom Gang

'''

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, TextAreaField, DateField
from wtforms.validators import DataRequired

# TODO 1: Implement User Story 1: Registration and Signing up (USE SIGNUP FORM FROM PREVIOUS PROJECTS BUT MODIFY IT TO FIT THIS PROJECT)


class RegistrationForm(FlaskForm):
    """ This class is meant for implementing the registration form for the application """
    id = StringField('ID', validators=[DataRequired()])  # user id
    email = StringField('Email', validators=[DataRequired()])  # email address
    creation_date = DateField('Creation Date', validators=[
                              DataRequired()])  # date of creation
    passwd = PasswordField('Password', validators=[DataRequired()])  # password
    passwd_confirm = PasswordField('Confirm Password', validators=[
                                   DataRequired()])  # password confirmation
    submit = SubmitField('Sign Up')


# TODO 2: Implement User Story 2: Login and Signing in (USE LOGIN FORM FROM PREVIOUS PROJECTS BUT MODIFY IT TO FIT THIS PROJECT)
class LoginForm(FlaskForm):
    """ This class is meant for implementing the login form for the application """
    id = StringField('ID', validators=[DataRequired()])  # user id
    passwd = PasswordField('Password', validators=[DataRequired()])  # password
    submit = SubmitField('Login')

# TODO 3: Implement User Story 3: Create a Playlist (USE INVOICE FORM FROM PREVIOUS PROJECTS BUT MODIFY IT TO FIT THIS PROJECT BY USING THE CLASS DIAGRAM)


class PlaylistForm(FlaskForm):
    """ This class is meant for implementing the playlist form for the application """
    # id = IntegerField('ID#', validators=[DataRequired()]) # playlist id
    name = StringField('Playlist Name', validators=[
                       DataRequired()])  # playlist name
    creation_date = DateField('Creation Date', validators=[
                        DataRequired()]) # date of creation
    creator_name = StringField('Creator Name', validators=[
                               DataRequired()])  # creator id
    description = TextAreaField('Description', validators=[
                                DataRequired()])  # description of playlist
    # number of videos in playlist
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Create Playlist')

# TODO 4: Implement User Story 3: Add a Video to a Playlist (USE ITEM FORM FROM PREVIOUS PROJECTS BUT MODIFY IT TO FIT THIS PROJECT BY USING THE CLASS DIAGRAM)


class VideoForm(FlaskForm):
    """ This class is meant for implementing the video form for the application """
    name = StringField('Video Title', validators=[
                       DataRequired()])  # video name
    url = StringField('URL', validators=[DataRequired()])  # url of video
    length = StringField('Length', validators=[
                         DataRequired()])  # length of video
    submit = SubmitField('Add Video')
