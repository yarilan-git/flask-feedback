
from flask  import Flask, render_template, request, flash, jsonify, redirect, session
from models import db, connect_db, User, Feedback
from forms import User_form, Login_form, Feedback_form
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)

app.config['SECRET_KEY'] = '123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def home_page():
    """ Redirects to the register page """
    return render_template('index.html', title="Welcome")

@app.route('/register', methods=['POST', 'GET'])
def register_user():
    """ If reached via a GET mothod, shows an empty form that allows prividing user information. If reached via a POST method, validates the data provided by the user. If the validation passes, registers the user in the database.  Otherwise, re-renders the form with error messages."""
    user_form = User_form()
    if user_form.validate_on_submit():
        user=User(username=user_form.user_name.data,
                  password=User.encrypt(user_form.password.data),
                  email=user_form.email.data,
                  first_name=user_form.f_name.data,
                  last_name=user_form.l_name.data)
        try:
            db.session.add(user)
            db.session.commit()
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        except IntegrityError:
            flash("This username already exist!")
    
    return render_template('register.html', form=user_form, title="User registration")

@app.route('/users/<username>')
def show_user_info(username):
    """ Displays the user information and their feedbacks if any """
    if "username" in session and session['username'] == username:
        user = User.query.get(username)
        msg = f"Welcome, {username}!"
        return render_template('user.html', title="User Info", msg=msg, user=user)
    else:
        msg="You are not autorized!"
        return render_template('user.html', title="User Info", msg=msg)
    

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user_and_feedbacks(username):
    """ Deletes a user and his/her feedbacks if any """
    if "username" in session and session['username'] == username:
        user=User.query.get(username)
        db.session.delete(user)
        db.session.commit()
        session.pop('username')
        return redirect('/')

    
        

@app.route('/login', methods=['POST', 'GET'])
def login():
    """ If reached via a GET mothod, shows an empty form that allows the user to enter login information. If reached via a POST method, validates the data provided by the user. If the validation passes, logs the user in.  Otherwise, re-renders the form with error messages."""
    login_form = Login_form()
    if login_form.validate_on_submit():
        if User.authentication_ok(login_form.user_name.data, login_form.password.data):
            session['username'] = login_form.user_name.data
            return redirect(f'/users/{login_form.user_name.data}')
        else:
            flash("The username or the password are incorrect!")
    return render_template('login.html', form=login_form, title="Login")

@app.route('/logout', methods=['POST'])
def logout():
    """ Logs out a user and goes back to the home page """
    if "username" in session:
        session.pop('username')
        return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def add_feedback(username):
    """ Adds a new feedback for a logged in user """
    feedback_form=Feedback_form()
    if feedback_form.validate_on_submit():
        if "username" in session and session['username'] == username:
            feedback=Feedback(title=feedback_form.title.data,
                              content=feedback_form.content.data,
                              username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{username}')
    else:
        return render_template('add_feedback.html', title='Add feedback', username=username, feedback_form=feedback_form)

@app.route('/feedbacks/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
    """ Deletes a feedback for a logged in user """
    feedback=Feedback.query.get(id)
    if "username" in session and session['username'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{feedback.username}")

@app.route('/feedbacks/<int:id>/update', methods=['GET','POST'])
def update_feedback(id):
    """ Updates the title and or content of a feedback for a logged in user """
    feedback=Feedback.query.get(id)
    feedback_form=Feedback_form(obj=feedback)
    if feedback_form.validate_on_submit():
        if "username" in session and session['username'] == feedback.username:
            feedback.title=feedback_form.title.data
            feedback.content=feedback_form.content.data
            try:
                db.session.add(feedback)
                db.session.commit()
                return redirect(f"/users/{feedback.username}")
            except:
                flash("Updadting the feedback has failed!")
        else:
            flash("You are not authorized to do this!")

    
    return render_template('update_feedback.html', title='Update feedback', username=feedback.username, feedback_form=feedback_form, feedback=feedback)




        
    










