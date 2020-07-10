import requests
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/', methods={'GET'})
def index_get():

    cities = City.query.all()

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=d645341da3d5cd09006398538afc96c0'
    
    weather_data = []

    for city in cities:
        r = requests.get(url.format(city.name)).json()
        weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon']
        }

        weather_data.append(weather)

    return render_template('weather.html', weather_data = weather_data)


@app.route('/', methods={'POST'})
def index_post():
    err_msg = ''
    new_city = request.form.get('city')
    
    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()
        if not existing_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()
        else:
            err_msg = 'City already exists!'



    return redirect(url_for('index_get'))