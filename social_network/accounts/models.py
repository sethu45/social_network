from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='send_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=12, choices=(('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')))
    
class Friendship(models.Model):
    user1 = models.ForeignKey(User, related_name='friend1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friend2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)