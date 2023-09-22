from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe import Recipe
from datetime import datetime




# SHOW 'CREATE_NEW_RECIPE' PAGE
@app.route('/new_recipe')
def new_recipe():
    if "user_id" not in session:
        flash("You are log out , please logged in",'register')
        return redirect("/")
    
    return render_template("new_recipe.html")




# CREATE NEW RECIPE PROCESS
@app.route('/new_recipe/process', methods=['POST'])
def create_recipe():
    
    #  condition radio button
    if 'under_30' not in request.form:
        session['under_30'] = None
    else:
        session['under_30'] = request.form['under_30']

    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "under_30": session["under_30"],
        "instructions": request.form["instructions"],
        "date": request.form["date"],
        "user_id": session["user_id"]
    }

    # validate method
    if not Recipe.validate_recipe(data):
        # Make it so the data the user input isn't lost when they have an error
        session["name"] = request.form["name"]
        session["description"] = request.form["description"]
        session["instructions"] = request.form["instructions"]
        session["date"] = request.form["date"]
        return redirect("/new_recipe")

    # save the new recipe to the db
    recipe_id =  Recipe.create_recipe(data)

    # save the new recipe id
    session["recipe_id"] = recipe_id

    # redirect
    return redirect('/dashboard')




# SHOW 'EDIT_RECIPE' PAGE

@app.route('/recipe/edit/<int:recipe_id>')
def edit_recipe(recipe_id):

    if "user_id" not in session:
        flash("You are log out , please logged in",'register')
        return redirect("/")

    data = {
        "recipe_id" : recipe_id
    }

    recipe = Recipe.get_one(data)

    return render_template("edit_recipe.html", specific_recipe = recipe)



# EDIT(UPDATE) RECIPE PROCESS

@app.route('/recipe/edit/<int:recipe_id>/process', methods=['POST'])
def edit_recipe_process(recipe_id):

    # condition radio button

    if 'under_30' not in request.form:
        session['under_30'] = None
    else:
        session['under_30'] = request.form['under_30']


    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "under_30": session["under_30"],
        "instructions": request.form["instructions"],
        "date": request.form["date"],
        "recipe_id" : recipe_id 
    }

    if not Recipe.validate_recipe(data):
        return redirect(f"/recipe/edit/{recipe_id}")

    Recipe.update_recipe(data)

    return redirect('/dashboard')



# SHOW PAGE 'DETAILS SPECIFIC RECIP'

@app.route('/recipe/<int:recipe_id>')
def show_recipe(recipe_id):

    if "user_id" not in session:
        flash("You are log out , please logged in",'register')
        return redirect("/")

    data = {
        "recipe_id" : recipe_id
    }

    
    recipe = Recipe.get_one(data)

    # date formatting
    date = datetime.strptime(recipe.date, "%Y-%m-%d").strftime("%B %dth %Y")

    return render_template("show_recipe.html", specific_recipe = recipe, date_formatting = date)




# DELETE SPECIFIC RECIPE PROCESS

@app.route('/recipe/delete/<int:recipe_id>')
def delete_recipe(recipe_id):
    
    data = {
        "recipe_id" : recipe_id
    }

    Recipe.delete_recipe(data)

    return redirect('/dashboard')