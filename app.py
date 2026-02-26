from flask import Flask
from config import *
from database.engine import db
from database.models import Task
from routes import init_routes

app = Flask(__name__)
app.config.from_object('config')

db.init_app(app)

with app.app_context():
    db.create_all()

init_routes(app)








if __name__ == "__main__":
    app.run(debug=True)


