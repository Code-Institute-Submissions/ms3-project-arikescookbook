# Imported flask functionality and other needed libraries.
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

# Imported environment variables.
from os import path
if path.exists("envvar.py"):
    import envvar

# An instance of flask
app = Flask(__name__)

# MongoDB environment variables configuraton.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Declared mongo constant variable.
mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    """
    Opens home page i.e index.html
    """
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    """
    Opens recipe page and displays recipes list in the database
    """
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route("/create_recipe")
def create_recipe():
    """
    Opens create_recipe page and displays the categories and cuisine collections
    """
    return render_template("create.html", categories=mongo.db.categories.find(), cuisine=mongo.db.cuisine.find())


@app.route("/search_recipe", methods=["POST"])
def search_recipe():
    """
    The recipes search function using index
    """
    search_recipes = request.form.get("search_recipes")
    mongo.db.recipes.create_index([("$**", "text")])
    recipes = mongo.db.recipes.find({"$text": {"$search": search_recipes}})
    return render_template("recipes.html", recipes=recipes, search=True)


@app.route("/insert_recipe", methods=["POST"])
def insert_recipe():
    """
    Inserts the new recipe into the database
    """
    data = {"category_name": request.form.get("category_name"),
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "description": request.form.get("description"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients"),
            "instructions": request.form.get("instructions"),
            "servings": request.form.get("servings"),
            "created_by": request.form.get("created_by"),
            "date_created": request.form.get("date_created"),
            }
    recipe = mongo.db.recipes
    recipe.insert_one(data)
    new_recipe = recipe.find_one({"category_name": data["category_name"]})["_id"]
    return redirect(url_for("recipes", recipe_id=new_recipe))


@app.route("/recipe_info/<recipe_id>")
def recipe_info(recipe_id):
    """
    Opens the recipe_info page and displays the recipe
    """
    that_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipeinfo.html", recipe=that_recipe)


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    """
    Opens edit recipe page and displays the recipe on the form
    """
    that_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    all_cuisine = mongo.db.cuisine.find()
    return render_template("editrecipe.html", recipe=that_recipe, cuisine=all_cuisine, categories=all_categories)


@app.route("/update_recipe/<recipe_id>", methods=["POST"])
def update_recipe(recipe_id):
    """
    Updates the recipe details in the database
    """
    data = {"category_name": request.form.get("category_name"),
            "cuisine_type": request.form.get("cuisine_type"),
            "recipe_name": request.form.get("recipe_name"),
            "description": request.form.get("description"),
            "cooking_time": request.form.get("cooking_time"),
            "ingredients": request.form.get("ingredients"),
            "instructions": request.form.get("instructions"),
            "servings": request.form.get("servings"),
            "created_by": request.form.get("created_by"),
            "date_created": request.form.get("date_created"),
            }
    recipe = mongo.db.recipes
    recipe.update({"_id": ObjectId(recipe_id)}, data),
    return redirect(url_for("recipes", recipe_id=recipe_id))


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Deletes the data from the database
    """
    mongo.db.recipes.remove({"_id": ObjectId(recipe_id)})
    return redirect(url_for("recipes"))


@app.errorhandler(404)
def page_not_found(e):
    """
    Error handler
    """
    return render_template("pageerror.html"), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
