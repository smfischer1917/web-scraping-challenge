from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, url="mongodb://localhost:27017/mars_app")


# Route to render index temp using data from Mongo
@app.route("/")

# Locate one record of data from the mongo database
mars_data = mongo.db.collection.find_one()

# Return template and data
return render_template("index.html", mars_dict=mars_data)

# Trigger for scrape function
@app.route("/scrape")
def scrape()
mars_data = scrape_mars.scrape_info()

#Update Mongo database
mondo.db.collection.update({}, mars_data, insert=True)

