from celery import Celery

app = Celery('notifications')
app.config_from_object('notification_service.celeryconfig')

if __name__ == '__main__':
    app.start()
