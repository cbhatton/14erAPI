from flask import Flask, jsonify, render_template, request, redirect
import json
from weather import get_weather
from flask_caching import Cache
from flask_apscheduler import APScheduler
from tools import apply_filters

from multiprocessing import Pool
from flask_bootstrap import Bootstrap5
from pymongo import MongoClient

app = Flask(__name__)
bootstrap = Bootstrap5(app)
app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'darkly'


client = MongoClient('mongodb://localhost:27017')
db = client['colorado14ers']
collection = db['peaks']

cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})


with open('colorado-14ers.json', 'r') as f:
    peaks = json.load(f)

scheduler = APScheduler()


# Preload weather data for all peaks and cache to file
def preload_weather():
    print('start')
    coords = [(float(lat), float(lon)) for lat, lon in [peak['lat/lon'].split(',') for peak in peaks.values()]]

    with Pool() as pool:
        results = pool.starmap(get_weather, coords)

    for peak_name, weather in zip(peaks.keys(), results):
        peaks[peak_name]['weather'] = weather

    for doc, weather in zip(collection.find(), results):
        collection.update_one({'_id': doc['_id']}, {'$set': {'weather': weather}})

    print('done')


# Schedule preloading weather data every 8 hours
scheduler.add_job(id='preload_weather_startup', func=preload_weather)
scheduler.add_job(id='preload_weather', func=preload_weather, trigger='interval', hours=8)


# Return all peaks
@app.route('/peaks')
def get_peaks():
    filtered_peaks = apply_filters(peaks)
    return jsonify(filtered_peaks)


# Return single peak
@app.route('/peaks/<peak_name>')
def get_peak(peak_name):
    return jsonify(peaks[peak_name])


# Return peaks by range
@app.route('/peaks/<range_name>')
def get_peak_by_range(range_name):
    pass


# Return weather for single peak
@app.route('/peaks/<peak_name>/weather')
def get_peak_weather(peak_name):
    lat_lon = peaks[peak_name]['lat/lon'].split(',')

    lat = float(lat_lon[0])
    lon = float(lat_lon[1].strip(' '))

    weather = get_weather(lat, lon)

    return weather


# Return weather for all peaks (cached)
@app.route('/peaks/weather')
def get_all_peak_weather():
    with open('weather.json', 'r') as f:
        weather = json.load(f)

    return weather


@app.route('/homepage')
def homepage():
    cls = request.form['class']
    precip = request.form['precip']
    range = request.form['range']
    ordering = request.form['ordering']

    filtered_peaks = apply_filters(peaks)
    return render_template('index.html', peaks=filtered_peaks,
                           cls=cls,
                           precip=precip,
                           range=range,
                           ordering=ordering)


@app.route('/filter', methods=['POST'])
def f():
    cls = request.form['class']
    precip = request.form['precip']
    range = request.form['range']
    ordering = request.form['ordering']

    filter_url = f"/homepage?"

    if cls != '':
        filter_url += f"class={cls}&"
    if precip != '':
        filter_url += f"precip={precip}&"
    if range != '':
        filter_url += f"range={range}&"
    if ordering != '':
        filter_url += f"ordering={ordering}"

    return redirect(filter_url)


if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run()
