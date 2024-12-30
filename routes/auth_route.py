from flask import Flask, render_template,abort,request,flash, redirect, url_for 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model import *
from sqlalchemy.orm import Session
from functools import wraps
from werkzeug.utils import secure_filename
import os



def auth_route(app):
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(id):
        return users.query.get(id)
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
           
            email = request.form['email']
            password = request.form['password']
            user = users.query.filter_by(email=email).first()
            if user!=None and user.password == password:
                
                if user.type == "cust":
                    login_user(user)
                    return redirect('/dashboard')
                elif user.type == "prof":
                    if user.s_status == "pending":
                        return "Your account is not yet approved <a href='/'> Go back to homepage</a>", 401
                        

                    else:   
                        login_user(user)   
                        return redirect('/prof/dashboard')
                    
            
            return "Invalid credentials <a href='/'> Go back to homepage</a>", 401
        
        return render_template('login.html', user= "customer", action="/login", forward="/signup")
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            user = users.query.filter_by(email=email).first()
            if user!=None and user.password == password:
                
                if user.type == "admin":
                    login_user(user)
                    return redirect('/admin_dash')

        return render_template('login.html', user= "admin", action="/admin/login", forward="/admin_dash")
    
    
    
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect('/')

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            new_user = users(
                name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                mobile=request.form['phone'],
                address=request.form['address'],
                city=request.form['city'],
                status = "active",
                type = "cust"
                

            )

            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        if request.method == 'GET':
            u_cities = db.session.query(users.city).distinct().all()
            cities = []
            for city in u_cities:
                cities.append(city[0])
            return render_template('signup.html', user= "customer", action="/signup", forward="/login", cities=cities)
       
    
    def allowed_file(filename):
                return '.' in filename and \
                        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    
    @app.route('/prof/signup', methods=['GET', 'POST'])
    def prof_signup():
        if request.method == 'POST':
            
            
            file = request.files['file']
            
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            

            new_user = users(
                name=request.form['name'],
                email=request.form['email'],
                password=request.form['password'],
                mobile=request.form['phone'],
                address=request.form['address'],
                city=request.form['city'],
                status = "active",
                type = "prof",
                service = request.form['service'],
                s_status = "pending",
                reviews = "0",
                doc_loc = filename,

                

            )

            db.session.add(new_user)
            db.session.commit()
            flash('Signup successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        if request.method == 'GET':
            u_cities = db.session.query(users.city).distinct().all()
            cities = []
            for city in u_cities:
                cities.append(city[0])
            servs = services.query.all()
            data = []
            for serv in servs:
                    t_dict = {
                        "service_uid":serv.service_id,
                        "service_name":serv.service_name,
                        
                    }
                    data.append(t_dict)
            return render_template('signup.html', user= "professional", action="/prof/signup", forward="/prof/login", cities=cities, serv = data)

    
    

        