from .models import Competition


def calculate_result_individual(participant, save=True):
    total_points = 0
    for submission in participant.submissions.all():
        question = submission.question
        answer = submission.answer
        q_corrects = len(question.answers.filter(correct=True).all())
        if answer.correct:
            total_points += 1 / q_corrects
    participant.points = total_points
    if save:
        participant.save()
    return participant


def calculate_result(competition: Competition):
    for participant in competition.participants.all():
        calculate_result_individual(participant)

