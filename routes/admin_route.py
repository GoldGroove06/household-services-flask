from flask import Flask, render_template,send_from_directory, request, redirect, url_for,jsonify, abort
from functools import wraps
from flask_login import  current_user
from sqlalchemy import and_, or_, not_  
from model import *
import os


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.type != 'admin':
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function 

def admin_route(app):
    u_cities = db.session.query(cities_list.city_name).distinct().all()
    cities = []
    for city in u_cities:
        cities.append(city[0])

    @app.route('/admin_dash', methods=['GET','POST'])
    @admin_required
    def admin_dash():
        return render_template('admin_dash.html')
    
    @app.route('/admin/manage/cust',methods=['GET','POST'])
    @admin_required
    def manage_cust():

        #get list of cities we serve
        return render_template('admin_manage_cust.html', cities=cities)
    

    @app.route('/admin/api/<city>/<route>',methods=['GET','POST'])
    @admin_required
    def api_serv(city, route):
        if request.method == 'GET':
             
            if route == 'serv':
                #fetch the services available in the city
                servas_id = cities_list.query.filter_by(city_name=city).all()
                
                data=[]
                for serv in servas_id:
                    servas = services.query.filter_by(service_id=serv.service_id).all()
                    
                    for serv in servas:
                        t_dict = {
                            "service_id":serv.service_id,
                            "service_name":serv.service_name,
                            "type":"service"
                            }
                        data.append(t_dict)
                    
                    pks = packages.query.filter_by(service_id=serv.service_id).all()
                    for pk in pks:
                        t_dict = {
                            "package_id":pk.package_id,
                            "package_name":pk.package_name,
                            "price":pk.price,
                            "duration":pk.duration,
                            "service_id":pk.service_id,
                            "type":"package"
                
                        }
                        data.append(t_dict)
              
                
                
                return jsonify(data)
            if route == 'cust':
                cust_user = users.query.filter_by(type='cust', city=city).all()
                data = []
                for cust in cust_user:
                    t_dict = {
                         "id":cust.id,
                        "name":cust.name,
                        "email":cust.email,
                        "mobile":cust.mobile,
                        "address":cust.address,
                        "status":cust.status,
                        "rating":cust.reviews,
                        "s_status":cust.s_status
                    }
                    data.append(t_dict)
                
                return jsonify(data)  
            
            if route == 'prof':
                prof_user = users.query.filter_by(type='prof', city=city).all()
                data = []
                for prof in prof_user:
                    t_dict = {
                         "id":prof.id,
                        "name":prof.name,
                        "email":prof.email,
                        "mobile":prof.mobile,
                        "address":prof.address,
                        "status":prof.status,
                        "rating":prof.reviews,
                        "s_status":prof.s_status
                    }
                    data.append(t_dict)
                
                   
                print(data)   
                return jsonify(data)  
            
            
                #fetch the cust available in the city
            
            
        

    @app.route('/admin/manage/serv', methods=['GET','POST'])
    @admin_required
    def manage_serv():
        
        #get list of cities we serve
        if request.method == 'GET':
                return render_template('admin_manage_serv.html', cities=cities)
        
        if request.method == 'POST':
            req=request.get_json()
            serv_val=req.get('id')
            type_val=req.get('type')
            if type_val == "package":
                packages.query.filter_by(package_id=serv_val).delete()
                cities_list.query.filter_by(service_id=serv_val).delete()
                db.session.commit()
                return jsonify({'m': 'success'})
            if type_val == "service":
                services.query.filter_by(service_id=serv_val).delete()
                cities_list.query.filter_by(service_id=serv_val).delete()
                db.session.commit()
                return jsonify({'m': 'success'})
        

    @app.route('/admin/servform/<servid>/<method>', methods=['POST', 'GET'])
    @admin_required
    def admin_servform(method, servid):
        
        if request.method == 'GET':
            if method == 'edit':
                serv = services.query.filter_by(service_id=servid).first()
                #get the details of the service using servid
                serv_data= {
                "service_uid":serv.service_id,
                "service_name":serv.service_name,
                }
                return render_template('admin_serv_form_edit.html', servid=servid, method=method, serv_data= serv_data)
            if method == 'add':

                    return render_template('admin_serv_form.html', method=method, city_name=servid)
               
        if request.method == 'POST':
            if method == 'add':
                    new = services(service_name=request.form['serv_name'],)
                    db.session.add(new)
                    db.session.commit()
                    service=services.query.all()
                    newservice=service[-1].service_id
                    city=cities_list(service_id=newservice,city_name=request.form['city_name'],)
                    db.session.add(city)
                    db.session.commit()
                    return redirect(url_for('manage_serv'))
            if method == 'edit':
                    serv = services.query.filter_by(service_id=servid).first()
                    serv.service_name = request.form['serv_name']
                    db.session.commit()

        return redirect(url_for('manage_serv'))
    
    @app.route('/admin/pkform/<servid>/<method>', methods=['POST', 'GET'])
    @admin_required
    def admin_pkform(method, servid):
        if request.method == 'GET':

            if method == 'edit':
                pk = packages.query.filter_by(package_id=servid).first()
                
                
                #get the details of the service using servid
                pk_data= {
                "package_id":pk.package_id,
                "package_name":pk.package_name,
                "price":pk.price,
                "duration":pk.duration,
                "service_id":pk.service_id,
                
                }
                return render_template('admin_serv_pkform_edit.html', servid=servid, method=method, pk_data= pk_data)
            if method == 'add':
                    serv_id_list = cities_list.query.filter_by(city_name=servid).all()

                    
                    serv_list = []
                    for s in serv_id_list:
                        serv = services.query.get(s.service_id)
                        print(serv)
                        temp = {
                             
                            "service_name":serv.service_name,
                        }
                        serv_list.append(temp)
                    return render_template('admin_serv_pkform.html', method=method, serv_list=serv_list)
               
        if request.method == 'POST':
            if method == 'add':
                
                serv_l= services.query.filter_by(service_name=request.form['service']).first()
                new = packages(
                    package_name=request.form['pk_name'],
                    price=request.form['price'],
                    service_id=serv_l.service_id,
                    duration=request.form['duration'],
                    )
                db.session.add(new)
                db.session.commit()
                return redirect(url_for('manage_serv'))
            if method == 'edit':
                    pk = packages.query.filter_by(package_id=servid).first()
                    pk.package_name=request.form['pk_name']
                    pk.price=request.form['price']
                    pk.duration=request.form['duration']
                    db.session.commit()
                    return redirect(url_for('manage_serv'))
        

    @app.route('/admin/manage/prof', methods=['GET','POST'])
    @admin_required
    def manage_prof():
        
        return render_template('admin_manage_prof.html', cities=cities)
    
    @app.route('/admin/action/<action>/<id>', methods=['GET'])
    @admin_required
    def admin_action(action, id):
        if request.method == 'GET':

            if action == "block":
                user = users.query.filter_by(id=id).first()
                user.status = "blocked"
                db.session.commit()

            if action == "unblock":
                user = users.query.filter_by(id=id).first()
                user.status = "active"
                db.session.commit()
        return jsonify({'m': 'success'})
    
    @app.route('/admin/verify/<id>',methods=['GET','POST'])
    @admin_required
    def admin_verify(id):
        prof = users.query.filter_by(id=id).first()
        if request.method == 'GET':
            
            data = {
                "prof_id":prof.id,
                "name":prof.name,
                "email":prof.email,
                "phone":prof.mobile,
                "address":prof.address + ', ' + prof.city,
                "docs":prof.doc_loc
            }
            return render_template('admin_verify.html', data=data)
        
        if request.method == 'POST':
            prof.s_status = "approved"
            db.session.commit()
        return redirect(url_for('manage_prof'))
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
         UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER')
         return send_from_directory(UPLOAD_FOLDER , filename)