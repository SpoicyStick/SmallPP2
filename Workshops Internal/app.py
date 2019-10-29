from flask import Flask, render_template, request, url_for, redirect, session, escape, abort,g
import pymysql, hashlib
from hashlib import md5
import os
#from flaskext.mysql import MySQL
app = Flask(__name__)
app.secret_key = "pp"
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
# Connect to the database
def create_connection():
    return pymysql.connect(host='localhost',
                             user='root',
                             password='13COM',
                             db='pbase',
                             charset='utf8mb4'
                             ,cursorclass=pymysql.cursors.DictCursor)

class ServerError(Exception):
	pass

#display users
@app.route('/')
def home():
	connection = create_connection()
	with connection.cursor() as cursor:
		sql = "SELECT * from workshops"
		cursor.execute(sql)
		data = cursor.fetchall()
		datahome = list(data)
	if session.get('logged_in'):
		username_session = session['username']
		return render_template("index.html", data=datahome, session_user_name=username_session)

	username_session = ""
	return render_template("index.html",data=datahome)

	connection = create_connection()
	try:
		with connection.cursor() as cursor:
			sql = "SELECT * from users"
			cursor.execute(sql)
			data = cursor.fetchall()
			data = list(data)
	finally:
			connection.close()


	return render_template("index.html", results=data)

@app.route('/users')
def users():
	if session.get('logged_in'):
		username_session = escape(session['username']).capitalize()
		connection = create_connection()
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * from users"
				cursor.execute(sql)
				cursor.execute(sql)
				data = cursor.fetchall()
				data = list(data)
		finally:
			connection.close()
		return render_template("users.html", session_user_name=username_session, results=data)

	username_session = ""
	return render_template("index.html")

@app.route('/workshops')
def workshops():
	if session.get('logged_in'):
		username_session = escape(session['username']).capitalize()
		connection = create_connection()
		roleid = session.get('RoleID')
		try:
			with connection.cursor() as cursor:
				sql = "SELECT * from workshops"
				cursor.execute(sql)
				data = cursor.fetchall()
				data = list(data)
				sql = "SELECT * FROM workshopassign"
				cursor.execute(sql)
				enrolled = cursor.fetchall()
				enrolled = list(enrolled)
		finally:
			connection.close()
		return render_template("Workshops.html", session_user_name=username_session, results=data,session_role=roleid,enrolled = enrolled, user_id = session.get('ID'))

	username_session = ""
	return render_template("index.html")



# update from form
@app.route('/add_user', methods=['POST','GET'])
def new_user():
   connection = create_connection()
   if request.method == 'POST':
         form_values = request.form 
         first_name = form_values["firstname"]
         family_name = form_values["familyname"]
         email = form_values["email"]
         dateofbirth = form_values["dateofbirth"]
         username = form_values["username"]
         password = form_values["password"]
         #password = hashlib.md5(password.encode())
         roleid =3
        
         try:
            with connection.cursor() as cursor:
                # Create a new record
                print('1')
                sq_insert = "INSERT INTO users (FirstName,FamilyName,Email,DateOfBirth,Username,Password,RoleID) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                print('2')
                val = (first_name,family_name,email,dateofbirth,username,password,roleid)
                print('3')
                cursor.execute(sq_insert,(val))
                print('4')
                #save values in dbase
            connection.commit()
            cursor.close()
            #with connection.cursor() as cursor:
            #    #pull records and display
            #    sql = "SELECT LAST_INSERT_ID() ID"
            #    cursor.execute(sql)
            #    data = cursor.fetchall()
            #    data = list(data)
            #    print(f'data is{data}')
         finally:
                 connection.close()
                 return redirect(url_for('login'))
  
   return render_template("add_user.html")


@app.route('/add_workshop', methods=['POST','GET'])
def new_workshop():
   connection = create_connection()
   if request.method == 'POST':
         #workshopid = form_values.get('Id')
         form_values = request.form 
         title = form_values["title"]
         date = form_values["date"]
         room = form_values["room"]
         subject = form_values["subject"]
         teacher = 2


         try:
            with connection.cursor() as cursor:
                # Create a new record
                print('1')
                sql = "INSERT INTO workshops (Title,Date,Room,Subject,Teacher) VALUES (%s,%s,%s,%s,%s)"
                print('2')
                val = (title,date,room,subject,teacher)
                print('3')
                cursor.execute(sql,(val))
                print('4')
                #save values in dbase
                connection.commit()
                #cursor.close()
            #with connection.cursor() as cursor:
                #pull records and display
                sql = "SELECT * from workshops"
                cursor.execute(sql)
                data = cursor.fetchall()
                data = list(data)
         finally:
             connection.close()
             return redirect(url_for('workshops'))
   return render_template("add_workshop.html")



@app.route('/edit_record', methods=['POST','GET'])
def update_user():
	user_id = request.args.get('id')
	connection = create_connection()
	if request.method == 'POST':
			form_values = request.form 
			first_name = form_values.get("firstname")
			family_name = form_values.get("familyname")
			email = form_values.get("email")
			password = form_values.get("password")
			dob = "2001-10-01"
			user_id = form_values.get('Id')
			try:
				with connection.cursor() as cursor:
					# Create a new record
					sql = "UPDATE users `users` SET FirstName=%s,FamilyName=%s,Email=%s,DateOfBirth=%s,Password=%s WHERE ID=%s"
					val = (first_name,family_name,email,dob,password, user_id)
					cursor.execute(sql,(val))
					data = cursor.fetchall()
					data = list(data)
					#save values in dbase
				connection.commit()
				cursor.close()
			finally:
				connection.close()
			return redirect(url_for('hello'))
	try:
		
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_id)
			data = cursor.fetchone()
			data = data
	finally:
		connection.close()
	return render_template("Edit_record.html",data=data)


@app.route('/edit_workshop', methods=['POST','GET'])
def update_workshop():
	id = request.args.get('id')
	connection = create_connection()
	if request.method == 'POST':
			form_values = request.form 

			id = form_values.get('id')
			title = form_values.get("title")
			date = form_values.get("date")
			room = form_values.get("room")
			subject = form_values.get("subject")
			teacher = form_values.get("teacher")

			try:
				with connection.cursor() as cursor:
					# Create a new record
					sql = "UPDATE workshops `workshops` SET Title=%s,Date=%s,Room=%s,Subject=%s,Teacher=%s WHERE WorkshopID=%s"
					val = (title,date,room,subject,teacher,id)
					cursor.execute(sql,(val))
					data = cursor.fetchall()
					data = list(data)
					#save values in dbase
				connection.commit()
				cursor.close()
			finally:
				connection.close()
			return redirect(url_for('home'))
	try:
		
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from workshops WHERE WorkshopID=%s"
			cursor.execute(sql,(id))
			data = cursor.fetchone()
			data = data
	finally:
		connection.close()
	return render_template("Edit_workshop.html",data=data)
# Tasks
# Per assessment AS91902 Document; complex techniques include creating queries
# which insert, update or delete to modify data
#so you should add new routes for edit_user, user_details and delete_user using
#record ids
# create the html pages needed
# modify database to include an image field which will store the image
# filename(eg pic.jpg) in database and implement this functionality in code
# where applicable
@app.route('/delete_record', methods=['POST','GET'])
def delete_record():
	user_ID = request.args.get('id')
	connection = create_connection()
	if request.method == 'POST':
		form_values = request.form 
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "DELETE FROM `users` WHERE ID=%s"
				val = (user_ID)
				cursor.execute(sql,(val))
				data = cursor.fetchall()
				data = list(data)
			#save values in dbase
			connection.commit()
			cursor.close()
		finally:
			connection.close()
			return redirect(url_for('home'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from users where ID=%s"
			cursor.execute(sql, user_ID)
			data = cursor.fetchone()
			data = data
	finally:
		connection.close()
	return render_template("delete_record.html",data=data)

@app.route('/delete_workshop', methods=['POST','GET'])
def delete_workshop():
	workshop_Id = request.args.get('id')
	connection = create_connection()
	if request.method == 'POST':
		form_values = request.form 
		try:
			with connection.cursor() as cursor:
				# Create a new record
				sql = "DELETE FROM `workshops` WHERE WorkshopID = %s"
				val = (workshop_Id)
				cursor.execute(sql,(val))
				data = cursor.fetchall()
				data = list(data)
			#save values in dbase
			connection.commit()
			cursor.close()
		finally:
			connection.close()
			return redirect(url_for('workshops'))
	try:
		with connection.cursor() as cursor:
			#pull records and display
			sql = "SELECT * from workshops where WorkshopID = %s"
			cursor.execute(sql, workshop_Id)
			data = cursor.fetchone()
			data = data
	finally:
		connection.close()
	return render_template("delete_workshop.html",data=data)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = create_connection()
    if  session.get('logged_in'):
        display_all_records()
        username_session = escape(session['username']).capitalize()
        return redirect(url_for("index", results=data,session_user_name=username_session))
    error = None
    try:
        with connection.cursor() as cursor:
         if request.method == 'POST':
            username_form = request.form['username']
            select_sql = "SELECT COUNT(1) FROM users WHERE UserName = %s"
            val = (username_form)
            cursor.execute(select_sql,val)
            #data = cursor.fetchall()

            if not list(cursor.fetchone())[0]:
                raise ServerError('Invalid username')

            password_form = request.form['password']
            select_sql = "SELECT RoleID,ID,Password from users WHERE UserName = %s"
            val = (username_form)
            cursor.execute(select_sql,val)
            data = list(cursor.fetchall())
            print(data)
            for row in data:
                #print(md5(password_form.encode()).hexdigest())
                if password_form == row['Password']:
                    session['username'] = request.form['username']
                    session['logged_in'] = True
                    session['ID'] = row['ID']
                    print(session['ID'])
                    session['RoleID'] = row['RoleID']
                    if 'url' in session:
                       return redirect(session['url'])
                    return redirect(url_for('home'))

            raise ServerError('Invalid password')
    except ServerError as e:
        error = str(e)
        session['logged_in'] = False

    return render_template('Login.html', error=error)

def display_all_records(role="admin",Id=0):
	global data
	connection = create_connection()
	try:
		with connection.cursor() as cursor:
			#pull records and display using a left join
			#select_sql = *SELECT* from users
			#if role not *admin*
			select_sql = "SELECT users.Id As Id,users.Email AS Email,users.FirstName AS FirstName, users.FamilyName As"
			if int(Id) > 0:
				print(select_sql)
				print(Id)
				select_sql = select_sql + " Where users Id=" + Id
				val = (int(Id))
				print(select_sql)
				cursor.execute(select_sql)
				data = cursor.fetchall()
				data = list(data)
	finally:
		connection.close()

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('home'))

#@app.route('/enrol', methods=['GET'])
#def enrol():
#	connection=create_connection()
#	id = request.args.get('id')
#	userid = session['ID']
#	with connection.cursor() as cursor:
#		# Create a new record
#			print('1')
#			sql ="INSERT INTO `workshopassign` (WorkshopID,UserID) VALUES (%s,%s)"
#			print('2')
#			val =(id,userid)
#			print('3')
#			cursor.execute(sql,(val))
#			print('4')
#			#save values in dbase
#			connection.commit()
#			cursor.close()
#	return redirect(url_for('enroluser'))

#@app.route('/enroluser')
#def enroluser():
#	connection=create_connection()
#	userid = session['ID']
#	with connection.cursor() as cursor:
#		try:
#			sql = "SELECT * from workshopassign"
#			cursor.execute(sql)
#			data = cursor.fetchall()
#			data=list(data)
#		finally:
#			connection.close()
#	return render_template('enroluser.html',data=data)
def display_workshop_records():
	connection = create_connection()
	try:
		with connection.cursor() as cursor:
			select_sql = "SELECT WorkshopId as workshopId FROM Workshopassign WHERE UserID = %s"
			cursor.execute(select_sql,id)
			data = cursor.fetchall()
			enrolledData = list(data)
			print(enrolledData)
	finally:
		connection.close()
	return enrolledData



@app.route('/enrol', methods=['GET'])
def enrol():
        if not g.username:
            #get workshop id from parameters
            w_id = request.args.get('wid')
            # store in session
            session['url'] = url_for('enrol',wid=w_id)
            # redirect to login page and return to enrol with url stored in
            # session
            return redirect(url_for('login'))
        connection = create_connection()
        uid = session['ID']
        wid = request.args.get('wid')
        # if user is teacher or admin cant enrol
        if session['RoleID'] == 1 or session['RoleID'] == 2:
            return redirect(url_for('workshops',error="Admins and Teachers are not eligble to Enrol"))
        try:
            with connection.cursor() as cursor:
               # check if user has not already enrolled
                sql = "select * from workshopassign where UserID= %s AND WorkshopID = %s"
                val1 = (uid,wid)
                cursor.execute(sql,val1)
                wkenrols = cursor.fetchall()
                if len(wkenrols) == 0:
                   # Create a new record
                    insert_sql = "INSERT INTO workshopassign (WorkshopID, UserID) VALUES (%s,%s)"
                    val = (wid,uid)
                    cursor.execute(insert_sql,(val))
                    #save values in dbase
                    connection.commit()
                    cursor.close()
                else:
                    error = "you have already enrolled in this workshop"
                    #username=""
                    #display_workshop_records(username,Id=0)
                    return redirect(url_for('workshops',error=error))
        finally:
             connection.close()
             #return to enrol workshop pages
             username = ""
             #display_workshop_records(username,Id=0)
        return redirect(url_for('workshops'))
    #return render_template('workshops.html',results=data)
@app.route('/disenrol', methods=['get'])
def disenrol():
    w_id = request.args.get('wid')
    u_id = session['ID']
    # check if admin or userid is same as in session
    if session['ID'] != u_id and session['RoleID'] != 3:
        return redirect(url_for('dashboard',error="you do not have permission"))
    #return error
    else:
        connection = create_connection()
        try:
            with connection.cursor() as cursor:
               # check if user has not already enrolled
                sql = "select * from workshopassign where UserID= %s and WorkshopID = %s"
                val1 = (u_id,w_id)
                cursor.execute(sql,val1)
                wkenrols = cursor.fetchall()
                if len(wkenrols) == 0:# record does not exist
                    return redirect(url_for('dashboard',error="that record does not exist"))
                # record exists delete it
                delete_sql = "delete from workshopassign where UserID=%s and WorkshopID =%s"
                val = (u_id,w_id)
                cursor.execute(delete_sql,val)
                #save values in dbase
                connection.commit()
                cursor.close()
        finally:
             connection.close()
             #return to dashboard
        return redirect(url_for('dashboard',message="successfully disenrolled"))


@app.route('/dashboard')
def dashboard():
    if not g.username:
            session['url'] = url_for('dashboard')
            return redirect(url_for('login'))
    connection = create_connection()
    user_name = session['username']
    roleid = session["RoleID"]
    userid = session['ID']
    try:
            with connection.cursor()as cursor:
                select_sql = "SELECT * FROM workshops"
                cursor.execute(select_sql)
                wkshop = cursor.fetchall()
                wkshop = list(wkshop)
                #print(wkshop)
    #finally:
                #connection.close()
    #try:
            with connection.cursor()as cursor:
                select_sql = "SELECT * FROM users"
                cursor.execute(select_sql)
                users = cursor.fetchall()
                users = list(users)
                #print(users)
            with connection.cursor()as cursor:
                select_sqlr = "SELECT * FROM roles"
                cursor.execute(select_sqlr)
                roles = cursor.fetchall()
                roles = list(roles)
                #print(users)

            with connection.cursor()as cursor:
                select_sqlw = "SELECT wa.ID assignID, wa.UserID uid, u.FirstName FirstName, u.FamilyName FamilyName, w.Title Title, w.WorkshopID WorkshopID, w.Room Room, w.Date Date  FROM workshopassign wa INNER JOIN workshops w ON wa.WorkshopID = w.WorkshopID INNER JOIN users u ON wa.UserID = u.ID"
                if roleid == 3:
                    select_sqlw = select_sqlw + " Where u.ID=" + str(userid)
                if roleid == 2:
                    select_sqlw = select_sqlw + " Where Teacher=" + str(userid)
                cursor.execute(select_sqlw)
                assigns = cursor.fetchall()
                assigns = list(assigns)
                #print(users)
    finally:
                connection.close()

#    display_workshop_records(user_name)
#    if roleid==2:

    return render_template('dashboard.html', users=users, roles=roles,results=wkshop, session_user_name=user_name,roleid=roleid,userid=userid, assigns=assigns)


@app.before_request
def before_request():
	g.username = None
	if 'username' in session:
		g.username = session['username']


if __name__ == '__main__':
	class ServerError(Exception):pass
	import os
	HOST = os.environ.get('SERVER_HOST', 'localhost')
	try:
		PORT = int(os.environ.get('SERVER_PORT', '5555'))
	except ValueError:
		PORT = 5555
	app.run(HOST, PORT, debug=True)


