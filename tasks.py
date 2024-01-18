from celery.schedules import crontab
from celery import Celery

celery = Celery('tasks', backend='rpc://', broker='pyamqp://')

@celery.task
def preload_weather_data():
    weather_data = {}

    coords = [(float(lat), float(lon)) for lat, lon in [peak['lat/lon'].split(',') for peak in peaks.values()]]
    print(coords)

    with Pool() as pool:
        results = pool.starmap(get_weather, coords)

    for peak_name, weather in zip(peaks.keys(), results):
        weather_data[peak_name] = weather

    return jsonify(weather_data)

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Executes every 8 hours
    sender.add_periodic_task(crontab(hour='*/8'), preload_weather_data.s())