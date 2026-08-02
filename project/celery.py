import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('atlas_ai')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Scheduled tasks
app.conf.beat_schedule = {
    'send-morning-briefings': {
        'task': 'ai.tasks.send_morning_briefings',
        'schedule': crontab(hour=9, minute=0),
    },
    'check-price-alerts': {
        'task': 'ai.tasks.check_price_alerts',
        'schedule': crontab(minute='*/5'),  # Every 5 minutes
    },
    'update-stock-prices': {
        'task': 'ai.tasks.update_stock_prices',
        'schedule': crontab(minute='*/15'),  # Every 15 minutes
    },
    'cleanup-old-messages': {
        'task': 'chat.tasks.cleanup_old_messages',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
}
