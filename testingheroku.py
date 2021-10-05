from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SECRET_KEY'] = "Futureime21"
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://vykjdeiaptubch:32eca6f9f825d0478014c320daeb3347bc5b50226af10ae619b47c02dbae36da@ec2-44-199-26-122.compute-1.amazonaws.com:5432/df993q19u6tf7h'
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

from routes import loginaccess

loginaccess.setup_page_routing(app, Base, db)

if __name__ == '__main__':
    app.run()
