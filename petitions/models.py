from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def yes_votes_count(self):
        return self.vote_set.filter(vote_type='yes').count()
    
class Vote(models.Model):
    VOTE_TYPES = [
        ('yes', 'Yes'),
    ]

    id = models.AutoField(primary_key=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=3, choices=VOTE_TYPES, default='yes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['petition', 'user']

    def __str__(self):
        return f"{self.user.username} voted {self.vote_type} on {self.petition.title}"