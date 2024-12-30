from flask import Flask, render_template,abort, request, redirect, url_for,jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from model import *
from functools import wraps


def prof_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'prof' :
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function 

def prof_route(app):
    
    #done
    @app.route('/prof/dashboard', methods=["GET", "POST"])
    @login_required
    @prof_required
    def prof_dashboard():
        open_services = []
        
        o_serv = service_req.query.filter_by(prof_id=None, service_name = current_user.service).all()
        #print(serv_name)
        for serv in o_serv:
            cust = users.query.filter_by(id=serv.cust_id).first()
            pk = packages.query.filter_by(package_id=serv.package_id).first()
            if cust.city == current_user.city:
                t_dict = {
                    "service_uid": serv.req_id,
                    "package_name": pk.package_name,
                    "time": serv.time,
                    "date": serv.date,
                    "price": pk.price,
                    "location": cust.address + ", " + cust.city,
                    "description": serv.comments
                }
                open_services.append(t_dict)

        active_services = []    
        a_serv = service_req.query.filter(
        service_req.prof_id == current_user.id,
        service_req.status != "closed"
            ).all()
        for serv in a_serv:
            cust = users.query.filter_by(id=serv.cust_id).first()
            pk = packages.query.filter_by(package_id=serv.package_id).first()
            t_dict = {
                "service_uid": serv.req_id,
                "package_name": pk.package_name,
                "time": serv.time,
                "date": serv.date,
                "price": pk.price,
                "location": cust.address + ", " + cust.city,
                "description": serv.comments,
                "status":serv.status,
            }
            active_services.append(t_dict)
       
        print(active_services)  
        return render_template("prof_dashboard.html", open_services = open_services, active_services = active_services)
    
    #done
    @app.route('/prof/profile', methods=["GET", "POST"])
    @login_required
    @prof_required
    def prof_profile():
        serv_list = service_req.query.filter_by(prof_id=current_user.id).all()
        service_list = []
        for serv in serv_list:
            cust = users.query.filter_by(id=serv.cust_id).first()
            pk = packages.query.filter_by(package_id=serv.package_id).first()
            prof = users.query.filter_by(id=serv.prof_id).first()
            dict = {
                "service_id":serv.req_id,
                "package_name":pk.package_name,
                "price":pk.price,
                "duration":pk.duration,
                "time": serv.time,
                "date": serv.date,
                "rating":prof.reviews + "★",
                "status":serv.status,
                "location":cust.address,
                "cust_name":cust.name,
            

            }
            service_list.append(dict)
            
        
        data = {
            "name":current_user.name,
            "email":current_user.email,
            "phone":current_user.mobile,
            "address":current_user.address + ", " + current_user.city,
            "service":current_user.service,
            "history": service_list,
        }
        
        return render_template("prof_profile.html", data = data)
    
    #done
    @app.route('/prof/service/<service_uid>', methods=[ "POST"])
    @login_required
    @prof_required
    def accept(service_uid):
        if request.method == "POST":
            if request.get_json()["status"] == "accepted":
                print("success")
                serv = service_req.query.filter_by(req_id=service_uid).first()
                serv.prof_id = current_user.id
                serv.status = "accepted"
                db.session.commit()
                return jsonify({'m': 'success'})
            
            if request.get_json()["status"] == "closed":
                serv = service_req.query.filter_by(req_id=service_uid).first()
                serv.status = "closed"
                db.session.commit()
                return jsonify({'m': 'success'})
        

  