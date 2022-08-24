from celery import shared_task
from grader_app.imageprocessor import Sheet
from grader_app.models import AnswerSheet
from test_app.models import Test, Question


@shared_task
def process_images(test_id, test_ans_id):
    try:

        try:
            test_ans_id: AnswerSheet = AnswerSheet.objects.get(id=test_ans_id)
        except:
            raise ValueError("Invalid Answer Sheet ID")
        test_ans_id.status = "Processing"
        test_ans_id.save()
        # Gets Marked List Details
        marked_list = Sheet(test_ans_id.image.file.read()).answerlist
        test_ans_id.image.file.close()
        questions = Question.objects.filter(test_id=test_id).order_by("created_at")
        total_qs = questions.count()
        final_score = 0

        for k, v in marked_list.items():
            if k > total_qs:
                continue
            question = questions[k - 1]
            if question.correct_option == (ord(v) - 65):
                final_score += question.marks

        # Update Answer Sheet
        test_ans_id.score = final_score
        test_ans_id.status = "Successful"
        test_ans_id.save()
        # End of Update Answer Sheet
    except:
        test_ans_id.status = "Failed"
        test_ans_id.failed = True
        test_ans_id.save()
