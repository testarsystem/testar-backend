from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now

User = get_user_model()


class Competition(models.Model):
    class Meta:
        db_table = 'Competition'
    title = models.CharField(max_length=200, null=False)
    description = models.TextField(null=True, blank=True)
    test = models.ForeignKey('testn.Test', on_delete=models.PROTECT, related_name='competitions', null=False)
    created = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(null=False)
    finish_time = models.DateTimeField(null=False)
    duration = models.TimeField(null=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='competitions', null=False)

    def duration_seconds(self):
        return (self.duration.hour * 60 + self.duration.minute) * 60 + self.duration.second


class Participant(models.Model):
    class Meta:
        db_table = 'Participant'
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participants', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='participated')
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants', null=False)
    points = models.FloatField(null=True)

    def start(self):
        self.start_time = now()

    def finish(self):
        self.end_time = now()


class Submission(models.Model):
    class Meta:
        db_table = 'ParticipantSubmission'
    participant = models.ForeignKey('Participant', on_delete=models.CASCADE, related_name='submissions', null=False)
    test = models.ForeignKey('testn.Test', on_delete=models.CASCADE, null=False)
    question = models.ForeignKey('testn.Question', on_delete=models.CASCADE, null=False)
    answer = models.ForeignKey('testn.Answer', on_delete=models.CASCADE, null=False)
