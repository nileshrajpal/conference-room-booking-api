from apscheduler.schedulers.background import BackgroundScheduler
from .slots_update import update_slots


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_slots, trigger='cron', hour='00', minute='00')
    scheduler.start()
