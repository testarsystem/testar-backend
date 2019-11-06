from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Test(models.Model):
    class Meta:
        db_table = 'Test'
    title = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tests')
    created = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    class Meta:
        db_table = 'Question'

    text = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')


class Answer(models.Model):
    class Meta:
        db_table = 'Answer'

    text = models.CharField(max_length=50)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    created = models.DateTimeField(auto_now_add=True)
