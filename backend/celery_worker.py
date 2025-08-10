from app import create_app
from app.tasks.celery_tasks import celery

app = create_app()
app.app_context().push()

if __name__ == '__main__':
    celery.start()
