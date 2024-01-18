from flask_apscheduler import APScheduler

from main import preload_weather


def init_scheduler(app):
    scheduler = APScheduler()

    # Schedule preloading weather data every 8 hours
    scheduler.add_job(id='preload_weather_startup', func=preload_weather)
    scheduler.add_job(id='preload_weather', func=preload_weather, trigger='interval', hours=8)
    scheduler.init_app(app)

