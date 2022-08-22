from celery import shared_task
from grader_app.imageprocessor import Sheet

@shared_task
def work(test_id, test_paper_img_link):
    marked_list = Sheet(test_paper_img_link)
