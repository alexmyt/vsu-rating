from apscheduler.schedulers.blocking import BlockingScheduler
import vgu_ratings

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=15)
def timed_job():
    print('This job is run every fifteen minutes.')
    vgu_ratings.fetch_all_ratings()

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()