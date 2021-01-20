
from datetime import datetime
from database import app
from flask import render_template,Flask,url_for,flash,redirect,request,session, send_from_directory
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from forms import RegistrationForm, LoginForm, SearchForm
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
import uuid

from db import Database
from models.Artist import Artist
from models.ArtPiece import ArtPiece
from models.Comment import Comment
from models.FavArtist import FavArtist
from models.FavArtPiece import FavArtPiece
from models.FavMuseum import FavMuseum
from models.Museum import Museum
from models.User import User

import psycopg2
import psycopg2.extras
import secret

import os
import hashlib

UPLOAD_FOLDER = '/static/img'
ALLOWED_EXTENSIONS = set(['png','jpg','jpeg','gif'])

app=Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'af65ae4e13b08a4eef049756b4259621'
app.config['BASE_DIR'] = os.path.dirname(__file__)
app.config['UPLOADED_PHOTOS_DEST'] = app.config['BASE_DIR'] + UPLOAD_FOLDER
photos = UploadSet('photos',IMAGES)
configure_uploads(app, photos)
patch_request_class(app)
@app.route('/')
@app.route('/home',methods=['GET','POST'])
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        user = session.get('username',None),
        title='Home Page',
        year=datetime.now().year,
    )
@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username',None)
    return render_template(
        'index.html',
        user = None,
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/register',methods=['GET','POST'])
def register():
    db = Database()
    """Renders the contact page."""
    form = RegistrationForm()
    if form.validate_on_submit():
        fn = secure_filename(str(uuid.uuid4()))
        print(fn)
        filename = photos.save(form.profilePicture.data, name = fn+".")
        #file_url = photos.url(filename)
        print(filename)
        user=User(form.username.data,generate_password_hash(form.password.data),form.age.data,form.sex.data,form.location.data , form.email.data , form.summary , filename , form.isModerator.data )
        db.user_add(user)
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('logout'))
    return render_template(
        'register.html',
        title='Register',
        form=form,
    )

@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('username',None) != None:
        return redirect(url_for('home'))
    else:
        form = LoginForm()
        db = Database()
        if form.validate_on_submit():
            if db.login(form.username.data,form.password.data):
                flash('You have been logged in!', 'success')
                session['username'] = form.username.data
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)


@app.route("/search", methods=['GET','POST'])
def search():
    form = SearchForm(choice="museum")
    db=Database()
    fres = []
    if form.validate_on_submit():
        if (form.choice.data == "museum") :
            result = db.museum_search(form.choice_museum.data, form.search.data)
        elif (form.choice.data == "artist"):
            result = db.artist_search(form.choice_artist.data, form.search.data)
        elif (form.choice.data == "artpiece"):
            result = db.artpiece_search(form.choice_artpiece.data, form.search.data)
        else:
            result = db.user_search(form.choice_user.data, form.search.data)
            
        for r in result:
            fres.append(r[0]) 
        return redirect(url_for('results',res = fres))
    return render_template('search.html',title='Search',form=form,user = session.get('username',None),)

@app.route("/results",methods=['GET','POST'])
def results():
    form = SearchForm(choice="museum")
    db=Database()
    result = request.args.getlist('res')
    fres = []
    if form.validate_on_submit():
        if (form.choice.data == "museum") :
            result = db.museum_search(form.choice_museum.data, form.search.data)
        elif (form.choice.data == "artist"):
            result = db.artist_search(form.choice_artist.data, form.search.data)
        elif (form.choice.data == "artpiece"):
            result = db.artpiece_search(form.choice_artpiece.data, form.search.data)
        else:
            result = db.user_search(form.choice_user.data, form.search.data) 
        for r in result:
            fres.append(r[0]) 
        return redirect(url_for('results',res = fres))
    return render_template('results.html',title='Results',form=form,user = session.get('username',None),results=result)

@app.route("/userprofile",methods=['GET','POST'])
def userprofile():
    db=Database()
    username = request.args.get('res')
    userinfo = db.user_userinfo(username)
    return render_template('userprofile.html',title='User Profile',user = session.get('username',None),info=userinfo)

@app.route("/static/img/<filename>")
def upload(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'],filename)
