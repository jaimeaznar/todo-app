import os
from flask import Flask, flash, redirect, render_template, request, url_for, abort, Response
from flask_login import current_user, login_user, login_required, logout_user
from flask_login import LoginManager
from forms import LoginForm, SignupForm, TaskForm
from models import db, setup_db,db_drop_and_create_all, User, Task
from flask_bootstrap import Bootstrap

login_manager = LoginManager()

def create_app(test_config=None):
    # create and cofigure the app
    app = Flask(__name__)
    app.config.from_object('config.DevConfig')
    Bootstrap(app)

    setup_db(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PATCH,POST,DELETE,OPTIONS'
        )

        return response
    
    login_manager.init_app(app)
    

    '''
    uncomment the following line to initialize the datbase
    !! NOTE THIS WILL DROP ALL RECORDS AND START DB FROM SCRATCH
    !! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
    '''
    # db_drop_and_create_all()


    """Route declaration."""

    

    @app.route('/')
    def home():
        """Landing page."""
        return render_template('home.html')


    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        """
        User sign-up page.

        GET requests serve sign-up page.
        POST requests validate form & user creation.
        """
        form = SignupForm()

        if form.validate_on_submit():
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user is None:
                user = User(
                    name=form.name.data,
                    email=form.email.data,
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()  # Create new user
                login_user(user)  # Log in as newly created user
                print('login as newly created user')
                return redirect(url_for('tasks'))
            flash('A user already exists with that email address.')
        return render_template('signup.html', form=form)


    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """
        Log-in page for registered users.

        GET requests serve Log-in page.
        POST requests validate and redirect user to dashboard.
        """
        # Bypass if user is logged in
        if current_user.is_authenticated:
            print('user authenticated')
            return redirect(url_for('tasks'))  

        form = LoginForm()
        # Validate login attempt
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()  
            if user and user.check_password(password=form.password.data):
                login_user(user)
                print('logging in user')
                return redirect(url_for('tasks'))
            flash('Invalid username/password combination')
            return redirect(url_for('login'))
        return render_template('login.html', form=form)


    @login_manager.user_loader
    def load_user(user_id):
        """Check if user is logged-in upon page load."""
        if user_id is not None:
            return User.query.get(user_id)
        return None


    @login_manager.unauthorized_handler
    def unauthorized():
        """Redirect unauthorized users to Login page."""
        flash('You must be logged in to view that page.')
        return redirect(url_for('login'))

    @app.route("/logout", methods=['GET'])
    @login_required
    def logout():
        """User log-out logic."""
        logout_user()
        return redirect(url_for('login'))

    
    @app.route("/tasks", methods=["GET"])
    @login_required
    def tasks():
        error = False
        # access the db
        try:
            user_id=current_user.get_id()
            tasks = [{
            'id': task.id,
            'description': task.description,
            'user_id': task.user_id
        } for task in Task.query.filter_by(user_id=user_id)]


        except BaseException:
            print('An error occurred. No tasks to display currently.')
            error = True

        if error:
            abort(404)

        else:
            
            return render_template('tasks.html',tasks=tasks)
            

    
    
    #----------------------------------------------------------------------------#
    # Create Taks.
    #----------------------------------------------------------------------------#

    @app.route('/create-task', methods=['GET'])
    @login_required
    def create_task_form():
        return render_template('create_task.html', form=TaskForm())

    
    @app.route('/create-task', methods=['POST'])
    @login_required
    def create_task_submission():
        error = False
        # add to db
        try:
            # create product object with form data
            new_task = Task(
                description=request.form.get('description'),
                user_id=current_user.get_id()   
            )
            # add to db
            new_task.insert()

        except BaseException:
            error = True
            db.session.rollback()
            print('Task ' + request.form['description'] + ' was not listed.')
        finally:
            # close session
            db.session.close()
            print(
                'Task ' +
                request.form['description'] +
                ' was successfully added!')

        if error:
            abort(400)
        else:
            return redirect(url_for('tasks'))

    
    #----------------------------------------------------------------------------#
    # Taks Done.
    #----------------------------------------------------------------------------#
    @app.route('/task-done/<int:task_id>', methods=['POST'])
    @login_required
    def task_done(task_id):
        print(task_id)
        print(type(task_id))
        # TODO: take values from the form submitted, and update existing
        # get artist from db
        try:
            print('inside try')
            task = Task.query.filter_by(id=task_id).first_or_404()
            
            #set values. Get them from request body
            if task.state:
                task.state = False
            else:
                task.state = True
            
            # commit changes
            db.session.commit()

        except BaseException as e:
            print(f'<<<<{e.__str__()}')
            flash('An error occurred while editing the task. Please try again later.')
            error = True
            db.session.rollback()
        finally:
            db.session.close()


        return redirect(url_for('tasks', tasks = Task.query.all()))

    #----------------------------------------------------------------------------#
    # Taks Delete.
    #----------------------------------------------------------------------------#

    @app.route('/delete/<int:task_id>', methods=['POST'])
    @login_required
    def delete_product(task_id):
        error = False
        task = Task.query.filter_by(id=task_id).first_or_404()

        # SQLAlchemy ORM to delete a record. Handle cases where the session
        # commit could fail.
        try:
            task.delete()
        except BaseException as e:
            print(f'<<<<{e.__str__()}')
            error = True
            db.session.rollback()
        finally:
            db.session.close()

        if error:
            print(
                f'An error ocurred when trying to delete the {task.name}. Please try again later.')
            abort(404)
        else:
            # delete image

            return redirect(url_for('tasks'))

  




    return app

app = create_app()

if __name__ == "__main__":
    app.run()

    