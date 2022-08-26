import traceback
from celery import shared_task
from grader_app.imageprocessor import Sheet
from grader_app.models import AnswerSheet, AnsweredQuestion
from test_app.models import Test, Question
import random


@shared_task
def process_images(test_id, test_ans_id, is_shuffled=False):
    try:

        try:
            test_ans_id: AnswerSheet = AnswerSheet.objects.get(id=test_ans_id)
        except:
            raise ValueError("Invalid Answer Sheet ID")
        test_ans_id.status = "Processing"
        test_ans_id.save()
        # Gets Marked List Details
        marked_list = Sheet(test_ans_id.image.file.read()).answerlist

        # Shuffling Function for Marked List
        if not Sheet.student_id or not test_ans_id.student:
            test_ans_id.status = "Set Student ID"
            test_ans_id.failed = True
            test_ans_id.save()
            return
        elif test_ans_id.student:
            Sheet.student_id = test_ans_id.student.id

        test_ans_id.image.file.close()
        questions = Question.objects.filter(test_id=test_id).order_by("created_at")
        total_qs = questions.count()
        if is_shuffled:
            questions = random.Random(Sheet.student_id).shuffle(list(questions))
        final_score = 0
        final_qs_list = []
        print(marked_list)
        for k, v in marked_list.items():
            if k > total_qs:
                continue
            question = questions[k - 1]
            _temp_ans_q = AnsweredQuestion(
                answer_sheet_id=test_ans_id,
                question=question,
                is_correct=question.correct_option == int(v),
            )
            final_qs_list.append(_temp_ans_q)
            final_score += question.marks if _temp_ans_q else 0
        AnsweredQuestion.objects.bulk_create(final_qs_list)
        # Update Answer Sheet
        test_ans_id.score = final_score
        test_ans_id.status = "Successful"
        test_ans_id.save()
        # End of Update Answer Sheet
    except:
        traceback.print_exc()
        test_ans_id.status = "Failed"
        test_ans_id.failed = True
        test_ans_id.save()
