from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler

executors = {
    'default': ThreadPoolExecutor(50),
}
scheduler = BackgroundScheduler({'apscheduler.timezone': 'Europe/Moscow'},
                                executors=executors)
scheduler.start()
