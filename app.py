from flask import Flask, render_template
from scrape_mars import scrape

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Connect to a database. Will create one if not already available.
db = client.scrape_db



# Creates a collection in the database and inserts two documents
#db.scrape.insert_many(
#    [
#        {
#            'player': 'Jessica',
#            'position': 'Point Guard'
#        },
#        {
#            'player': 'Mark',
#            'position': 'Center'
#        }
#    ]
#)


# Set route
@app.route('/')
def index():
    scrape_values = list(db.scrape.find())
    if len(scrape_values) == 0:
        scrape_values = [scrape(),]
        print(scrape_values)
    return render_template('index.html', scrape_values=scrape_values)

@app.route('/scrape')
def call_scrape():
    # Drops collection if available to remove duplicates
    db.scrape.drop()
    scrape_values = scrape()
    db.scrape.insert_one(scrape_values)
    print(scrape_values)
    return render_template('index.html', scrape_values=[scrape_values,])

if __name__ == "__main__":
    app.run(debug=True)