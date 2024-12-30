from flask import Flask, render_template,abort, request, redirect, url_for,jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model import *
from functools import wraps

def cust_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'cust':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

def customer_route(app):
    

    #done only left thing is pop serv list 
    @app.route('/dashboard')
    @login_required
    @cust_required
    def main():
        #filter the categories acc to avaible services cat name from db
        # available services city list
        print(current_user.city)
        city_filter = cities_list.query.filter_by(city_name=current_user.city).all()
        service_list =[]

        for city in city_filter:
            temp = services.query.filter_by(service_id=city.service_id).first() 
            service_list.append(temp)
       
        print(type(service_list))
        
        pop_services_list=[
            {"serv-name":"Cleaning",
            "serv-img":"/static/img/cleaning.jpg"},
            {"serv-name":"Electrician",
            "serv-img":"/static/img/electrician.jpg"},
            {"serv-name":"Personal Care",
            "serv-img":"/static/img/pers.jpg"},
            {"serv-name":"Laundry & Ironing",
            "serv-img":"/static/img/iron.jpg"},
            {"serv-name":"Pet Care",
            "serv-img":"/static/img/pet.jpg"},
        ]

        
        return render_template("cust_dashboard.html", pop_services_list=pop_services_list, title="Dashboard", categories=service_list) 

   
   
    
    #done
    @app.route('/search/<category>', methods=['GET'])
    @login_required
    @cust_required
    def search(category):
       
        serv = services.query.filter_by(service_name=category).first()
        results = packages.query.filter_by(service_id=serv.service_id).all()
        data = []
        for result in results:
            temp = {
                "package_name":result.package_name,
                "price":result.price,
                "duration":result.duration,
                'service_id':result.service_id,
                'package_id':result.package_id,
            }
            data.append(temp)
        
                
            
        
        return jsonify(data)
    
    #done
    @app.route('/profile')
    @login_required
    @cust_required
    def profile():
        serv_list = service_req.query.filter_by(cust_id=current_user.id).all()
        service_list = []
        for serv in serv_list:
            pk = packages.query.filter_by(package_id=serv.package_id).first()
            if serv.prof_id == None:
                
                dict = {
                "service_id":serv.req_id,
                "package_name":pk.package_name,
                "price":pk.price,
                "duration":pk.duration,
                "prof_name":"not assigned yet",
                "time": serv.time,
                "date": serv.date,
                "rating":"",
                "status":serv.status,
            }
            else :
                prof = users.query.filter_by(id=serv.prof_id).first()
                dict = {
                "service_id":serv.req_id,
                "package_name":pk.package_name,
                "price":pk.price,
                "phone":prof.mobile,
                "duration":pk.duration,
                "prof_name":prof.name,
                "time": serv.time,
                "date": serv.date,
                "rating":"★ " + prof.reviews,
                "status":serv.status,
            }
            service_list.append(dict)
            
        
        data = {
            "name":current_user.name,
            "email":current_user.email,
            "phone":current_user.mobile,
            "address":current_user.address + ", " + current_user.city,
            "history": service_list,
        }
        return render_template("cust_profile.html", data = data)
    
    #done
    @app.route('/book/<package_id>')
    @login_required
    @cust_required
    def book(package_id, method=['GET' , "POST"]):
        #need to get the package details
        pk = packages.query.filter_by(package_id=package_id).first()
        serv = services.query.filter_by(service_id=pk.service_id).first()
        data = {"service_name":serv.service_name,
                "package_name":pk.package_name,
                "price":pk.price,
                "duration":pk.duration,
                }
        
       
        return render_template("cust_book.html", package_id=package_id, data = data)

    #done
    @app.route('/booking/<package_id>', methods=["POST"])
    @login_required
    @cust_required
    def booking(package_id):
        if request.method == "POST":
            pk = packages.query.get(package_id)
            serv_name = services.query.get(pk.service_id)
            new_book = service_req(
                cust_id = current_user.id,
                package_id = package_id,
                status = "requested",
                time = request.form['time'],
                date = request.form['date'],
                comments = request.form['comments'],
                service_name = serv_name.service_name
            )
            db.session.add(new_book)
            db.session.commit()
        return redirect("/dashboard")
    
    #done
    @app.route('/bookedit/<service_uid>', methods=["GET", "POST"])
    @login_required
    @cust_required
    def bookedit(service_uid):
        #fetch the service details using the service_uid
        if request.method == "POST":
            serv = service_req.query.get(service_uid)
            serv.time = request.form['time']
            serv.date = request.form['date']
            serv.comments = request.form['comments']
            db.session.commit()

            return redirect("/profile")
        
        if request.method == "GET":
            serv = service_req.query.filter_by(req_id=service_uid).first()
            pk = packages.query.filter_by(package_id=serv.package_id).first()
       
            serv_data = {   
                    "service_uid":service_uid,
                    "package_name":pk.package_name,
                    "price":pk.price,
                    "duration":pk.duration,
                    "status":serv.status,
                    "time": serv.time,  
                    "date": serv.date,
                    "comments": serv.comments,
                }
            return render_template("cust_editbook.html", data = serv_data, edit = True)
    
    #need to think about the close process
    #left
    @app.route('/close/<service_uid>', methods=["GET", "POST"])
    @login_required
    @cust_required
    def close(service_uid):
        #fetch the service details using the service_uid
        if request.method == "POST":
            pk = service_req.query.filter_by(req_id=service_uid).first()
            pk.status = "cust_closed"
            pk.comments = request.form['remarks']
            
            prof = users.query.get( pk.prof_id)
            if prof.reviews != 0:
                prof.reviews = (float(prof.reviews) + float(request.form["rating"])) / 2
            elif float(prof.reviews) == 0:
                prof.reviews = float(request.form["rating"])
            db.session.commit()
            return redirect("/profile")
        if request.method == "GET":
            req = service_req.query.filter_by(req_id = service_uid).first()
            pk = packages.query.get(req.package_id)
            prof = users.query.get(req.prof_id)
            serv_data = {   
                    "service_uid":req.req_id,
                    "package_name":pk.package_name,
                    "price":pk.price,
                    "prof_name":prof.name,
                    "duration":pk.duration,
                   
                }
            return render_template("cust_close.html", serv_data = serv_data)