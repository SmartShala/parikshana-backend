from time import sleep
from celery import shared_task


@shared_task
def work(name, age):
    sleep(10)
    print(f"{name} {age}")
    return f"{name}+{age}"
