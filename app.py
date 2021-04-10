# Importing dependencies
from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

# Let's break down what this code is doing.
# The first line says that we'll use Flask to render a template, redirecting to another url, 
# and creating a URL.
# The second line says we'll use PyMongo to interact with our Mongo database.
# The third line says that to use the scraping code, we will convert from Jupyter notebook to Python.

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform 
# resource identifier similar to a URL.

# "mongodb://localhost:27017/mars_app" is the URI we'll be using to connect our app to Mongo. 
# This URI is saying that the app can reach Mongo through our localhost server, using port 27017, 
# using a database named "mars_app".

# Set up App Route

@app.route("/")
# This function is what links our visual representation of our work, our web app, to the code that powers it.
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
# This function is setting up the scraping route
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update({}, mars_data, upsert=True)
    return redirect('/', code=302)

if __name__ == "__main__":
   app.run(debug=True)