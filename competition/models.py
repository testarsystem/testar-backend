from django.db import models
from django.contrib.auth import get_user_model

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


class Participant(models.Model):
    class Meta:
        db_table = 'Participant'
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name='participants', null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='participants', null=False)

