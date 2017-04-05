from flask import Flask,redirect,url_for,render_template
from flask import request
from flask import flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import  subprocess 
import  os
import json
from subprocess import check_output
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kite@localhost/buspass'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

@app.route('/')
def login():
    return render_template('login.html')
	
@app.route('/login_reg',methods=['GET','POST'])
def login_reg():
    if request.method == 'GET':
        return render_template('login.html')
    user = request.form['name']
    password = request.form['password']
    register = registration.query.filter_by(name=user,password=password).first()
    if  request.form['name'] == 'admin' and request.form['password'] == 'admin':
		return redirect(url_for('addbus',name=user))  
    if register is None:
        return redirect(url_for('login'))
    return redirect(url_for('success',name=user))
   

@app.route('/success/<name>')
def success(name):	
	return render_template('profile.html',registration=registration.query.filter_by(name='%s'%name))


@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/createpass')
def createpass():
	return render_template('createpass.html',registration=registration.query.order_by(registration.id.desc()).limit(1).all())
	
@app.route('/passdetails',methods = ['POST', 'GET'])
def passdetails():
	if request.method == 'POST':
		user = request.form['passid']	
		return redirect(url_for('details',passid=user))

																																																		
@app.route('/details/<int:passid>')
def details(passid):
	return render_template('details.html',renewpass=renewpass.query.filter_by(passid='%s'%passid))
	

@app.route('/passs')
def passs():
	return render_template('pass.html')	


@app.route('/renewpass')
def renewpass():
	return render_template('renew.html',createpass=createpass.query.order_by(createpass.id.desc()).limit(1).all())
	
@app.route('/addbus')
def addbus():
	return render_template('addbus.html')	
	
@app.route('/editbus')
def editbus():
	return render_template('editbus.html')
	
@app.route('/userdetails')
def userdetails():
	return render_template('userdetails.html',registration=registration.query.all())
		
@app.route('/smail')
def smail():
	return render_template('mail.html')
	
@app.route('/sendmail')
def sendmail():
	os.system('php -f mail.php')
	return render_template('templates/mail.php')
	

		
@app.route('/detailpass')
def detailpass():
	return render_template('detailpass.html',renewpass=renewpass.query.all())


class registration(db.Model):
	id = db.Column('register_id', db.Integer, primary_key = True )
	name=db.Column(db.String(50),unique=True)
	password=db.Column(db.String(50),unique=True)
	gender=db.Column(db.String(50))
	qualification=db.Column(db.String(50))
	address=db.Column(db.String(50),unique=True)
	email=db.Column(db.String(50),unique=True)
	city=db.Column(db.String(50))
	phone=db.Column(db.Integer,unique=True)	
	
	def __init__(self,name,password,gender,qualification,address,email,city,phone):
		self.name=name
		self.password=password
		self.gender=gender
		self.qualification=qualification
		self.address=address
		self.email=email
		self.city=city
		self.phone=phone 	
		

	@app.route('/register_page', methods = ['GET', 'POST'])
	def register_page():
		if request.method == 'POST':
			if not request.form['name'] or not request.form['password'] or not request.form['gender'] or not request.form['qualification'] or not request.form['address'] or not request.form['email'] or not request.form['city'] or not request.form['phone'] :
				flash('Please enter all the fields', 'error')
			else:
				register = registration(request.form['name'],request.form['password'],request.form['gender'],request.form['qualification'],request.form['address'],request.form['email'],request.form['city'],request.form['phone']   )         
				db.session.add(register)
				db.session.commit()
				flash('Record was successfully added')
			return redirect(url_for('register'))
		return render_template('register.html') 
		
class createpass(db.Model):
	id = db.Column('create_id', db.Integer, primary_key = True )
	passid = db.Column(db.Integer,unique=True)
	busno = db.Column(db.String(50))
	start = db.Column(db.String(50))
	end=db.Column(db.String(50))
	bustype=db.Column(db.String(50))
	amount=db.Column(db.Integer)
	cardno=db.Column(db.Integer,unique=True)
	cvvno=db.Column(db.Integer,unique=True)	
	stime=db.Column(db.DateTime)
	etime=db.Column(db.DateTime)
		
	
	def __init__(self,passid,busno,start,end,bustype,amount,cardno,cvvno,stime,etime):
		self.passid=passid
		self.busno=busno
		self.start=start
		self.end=end
		self.bustype=bustype
		self.amount=amount
		self.cardno=cardno
		self.cvvno=cvvno
		self.stime=stime
		self.etime=etime
		
		
		 	 	
	@app.route('/create_page', methods = ['GET', 'POST'])
	def create_page():
		if request.method == 'POST':
			if not request.form['passid'] or not request.form['busno'] or not request.form['start'] or not request.form['end'] or not request.form['bustype'] or not request.form['amount'] or not request.form['cardno'] or not request.form['cvvno'] or not request.form['stime'] or not request.form['etime'] :
				flash('Please enter all the fields', 'error')
			else:
				create = createpass(request.form['passid'],request.form['busno'],request.form['start'],request.form['end'],request.form['bustype'],request.form['amount'],request.form['cardno'],request.form['cvvno'],request.form['stime'],request.form['etime'] )         
				db.session.add(create)
				db.session.commit()
				flash('Record was successfully added')
				return redirect(url_for('createpass'))
			return render_template('createpass.html') 

class renewpass(db.Model):
	id = db.Column('renew_id', db.Integer, primary_key = True )
	passid = db.Column(db.Integer,unique=True)
	busno = db.Column(db.String(50))
	start = db.Column(db.String(50))
	end=db.Column(db.String(50))
	bustype=db.Column(db.String(50))
	amount=db.Column(db.Integer)
	cardno=db.Column(db.Integer,unique=True)
	cvvno=db.Column(db.Integer,unique=True)	
	stime=db.Column(db.DateTime)
	etime=db.Column(db.DateTime)
		
		
	
	def __init__(self,passid,busno,start,end,bustype,amount,cardno,cvvno,stime,etime):
		self.passid=passid
		self.busno=busno
		self.start=start
		self.end=end
		self.bustype=bustype
		self.amount=amount
		self.cardno=cardno
		self.cvvno=cvvno
		self.stime=stime
		self.etime=etime
		
		
		 	 	
	@app.route('/renew_page', methods = ['GET', 'POST'])
	def renew_page():
		if request.method == 'POST':
			if not request.form['passid'] or not request.form['busno'] or not request.form['start'] or not request.form['end'] or not request.form['bustype'] or not request.form['amount'] or not request.form['cardno'] or not request.form['cvvno'] or not request.form['stime'] or not request.form['etime'] :
				flash('Please enter all the fields', 'error')
			else:
				renew = renewpass(request.form['passid'],request.form['busno'],request.form['start'],request.form['end'],request.form['bustype'],request.form['amount'],request.form['cardno'],request.form['cvvno'],request.form['stime'],request.form['etime'] )         
				db.session.add(renew)
				db.session.commit()
				flash('Record was successfully added')
				return redirect(url_for('renewpass'))
			return render_template('renew.html') 
			
			
class addbus(db.Model):
	id = db.Column('addbusid_id', db.Integer, primary_key = True )
	busnumber= db.Column(db.Integer)
	startroute=db.Column(db.String(50))
	endroute=db.Column(db.String(50))
	stopa=db.Column(db.String(50))
	stopb=db.Column(db.String(50))
	stopc=db.Column(db.String(50))
	stopd=db.Column(db.String(50))
	stope=db.Column(db.String(50))
	stopf=db.Column(db.String(50))
	stopg=db.Column(db.String(50))
	stoph=db.Column(db.String(50))
	stopi=db.Column(db.String(50))
	stopj=db.Column(db.String(50))
	stopk=db.Column(db.String(50))
	stopl=db.Column(db.String(50))
	
	def __init__(self,busnumber,startroute,endroute,stopa,stopb,stopc,stopd,stope,stopf,stopg,stoph,stopi,stopj,stopk,stopl):
		self.busnumber=busnumber
		self.startroute=startroute
		self.endroute=endroute
		self.stopa=stopa
		self.stopb=stopb
		self.stopc=stopc
		self.stopd=stopd
		self.stope=stope
		self.stopf=stopf
		self.stopg=stopg
		self.stoph=stoph
		self.stopi=stopi
		self.stopj=stopj
		self.stopk=stopk
		self.stopl=stopl
		
			
				
	@app.route('/addbus', methods = ['GET', 'POST'])
	def add_bus():
		if request.method == 'POST':
			if not request.form['busnumber'] or not request.form['startroute'] or not request.form['endroute'] or not request.form['stopa'] or not request.form['stopb'] or not request.form['stopc'] or not request.form['stopd'] or not request.form['stope'] or not request.form['stopf'] or not request.form['stopg'] or not request.form['stoph'] or not request.form['stopi'] or not request.form['stopj']or not request.form['stopk']or not request.form['stopl']:
					flash('Please enter all the fields', 'error')
			else:
				addbusid = addbus(request.form['busnumber'],request.form['startroute'],request.form['endroute'],request.form['stopa'],request.form['stopb'],request.form['stopc'],request.form['stopd'],request.form['stope'],request.form['stopf'],request.form['stopg'],request.form['stoph'],request.form['stopi'],request.form['stopj'],request.form['stopk'],request.form['stopl'])          
				db.session.add(addbusid)
				db.session.commit()
				flash('Record was successfully added')
			return redirect(url_for('addbus'))
		return render_template('addbus.html') 
		



if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
			
			

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True)
			
