from flask_app import app
from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




# HOME 
@app.route("/")
def home():
   return redirect('/register')



# SHOW REGISTER PAGE
@app.route("/register")
def register_page():
   if "user_id" in session: 
        session["user_created"] = False  
        flash("you are  logged in, please log out", 'dashboard')
        return redirect ("/dashboard")
   
   return render_template("register.html")



# REGISTER / CREATE NEW USER
@app.route('/register_process', methods=['POST'])
def register_process():
    
    data = {
        "fname" : request.form["firstname"],
        "lname" : request.form["lastname"],
        "eml" : request.form["email"],
        "psswrd" : request.form["password"],
        "conf_pass" : request.form["conf_pass"],
    }

    # validate method
    if not User.validate_user_infos(data): 
        # Make it so the data the user input isn't lost when they have an error
        session["firstname"] = request.form["firstname"]
        session["lastname"] = request.form["lastname"]
        session["email"] = request.form["email"]
        return redirect("/register")
    
    data["psswrd"] =  bcrypt.generate_password_hash(request.form['password'])

    user_id = User.create_user(data)

    session["user_id"] = user_id

    session["firstname"] = request.form["firstname"] 

    return redirect('/dashboard')





# SHOW LOGIN PAGE
@app.route("/login")
def login_page():
   if "user_id" in session: 
        flash("You are  logged in, please log out", 'dashboard')
        return redirect ("/dashboard")
   
   return render_template("login.html")




# LOGIN / SHOW USER SESSION
@app.route('/login_process', methods=['POST'])
def login():
    #validate login info
    data = { "email" : request.form["email"] }
    this_user = User.user_with_specific_email(data)
    if not this_user:
        flash("Invalid Email", "login")
        session["email"] = request.form["email"]
        return redirect("/login")
    if not bcrypt.check_password_hash(this_user.password, request.form['password']):
        flash("Invalid Password", "login")
        session["email"] = request.form["email"]
        return redirect('/login')
    
    
    #put the user ID into session and redirect to dashboard
    session['user_id'] = this_user.id

    #save user firstname
    session["firstname"] = this_user.first_name 

    return redirect('/dashboard')




# SHOW DASHBOARD PAGE
@app.route('/dashboard')
def dashboard():

    if "user_id" not in session:
        flash("You are log out , please logged in",'register')
        return redirect("/")

    all_recipes = Recipe.get_all()

    # reset session variables
    session["name"] = ''
    session["description"] = ''
    session["instructions"] = ''
    session["date"] = ''

    return render_template("dashboard.html", all_recipes = all_recipes)



# END SESSION
@app.route('/logout')
def logout():
    session.clear()
    return redirect ("/login")




@app.errorhandler(404)  # we specify in parameter here the type of error, here it is 404
def page_not_found(
    error,
):  # (error) is important because it recovers the instance of the error that was thrown
    return f"<h2 style='text-align:center;padding-top:40px'>Error 404. Sorry! No response. Try again</h2>"  