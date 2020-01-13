from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
conn = 'mongodb://localhost:27017'
client = PyMongo.MongoClient(conn)

mars_db = mongo.mars_db
mars_db.drop()

@app.route('/')
def index():

    final_results = mars_db.find_one()
    return render_template("index.html",mars_results = final_results)


@app.route('/scrape')
def scrape ():
    mars_dict = scrape_mars.scrape()

    mars_db.insert_one(mars_dict)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug = True)