import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

from os import path
if path.exists("envvar.py"):
  import envvar


app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/recipes")
def recipes():
    return render_template("recipes.html", recipes=mongo.db.recipes.find())


@app.route("/recipe_info/<recipe_id>")
def recipe_info(recipe_id):
    that_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipeinfo.html", recipe=that_recipe)


@app.route("/edit_recipe/<recipe_id>")
def edit_recipe(recipe_id):
    that_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories = mongo.db.categories.find()
    all_cuisine = mongo.db.cuisine.find()
    return render_template("editrecipe.html", recipe=that_recipe, cuisine=all_cuisine, categories=all_categories)


@app.route("/create_recipe")
def create_recipe():
    return render_template("create.html", categories=mongo.db.categories.find(), cuisine=mongo.db.cuisine.find())


@app.route("/shop")
def shop():
    return render_template("shop.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
