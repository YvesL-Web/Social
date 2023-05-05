from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from users.models import User
from django.db.models.signals import post_save

# Create your models here.
class FriendsList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    friends = models.ManyToManyField(User, blank=True, related_name="friends")
    
    def __str__(self):
        return self.user.username 
    
    
    def add_friend(self, account):
        # add a new friend
        if not account in self.friends.all():
            self.friends.add(account)

    def remove_friend(self, account):
        #  remove friend
        if account in self.friends.all():
            self.friends.remove(account)

    def unfriend(self, removee):
        # initiate the action of unfrieding someone
        remover_friends_list = self # person terminating the friendship
        #remove friend from remover friend list
        remover_friends_list.remove_friend(removee)

        #remove friend from removee friend list
        friends_list = FriendsList.objects.get(user=removee)
        friends_list.remove_friend(self.user)

    def is_mutual_friend(self, friend):

        # is this a friend
        if friend in self.friends.all():
            return True
        return False
    
class FriendRequest(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.username
    
    def accept(self):
        # Accept a friend request
        # Update both sender and receiver friend list
        receiver_friend_list = FriendsList.objects.get(user=self.receiver)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendsList.objects.get(user=self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.receiver)
                self.is_active =False
                self.save()

    def decline(self):
        # Decline a friend request
        # setting is_active field to false
        self.is_active = False
        self.save()

    def cancel(self):
        '''
        Cancel a friend request
        It's 'cancelled' by setting the 'is_active' field to Fasle
        this is only different with respect to 'declining' through the notification that is generated.
        '''
        self.is_active = False
        self.save()
        
# Signal
@receiver(post_save, sender=User)
def create_friend_list(sender, instance, created, **kwargs):
    if created:
        FriendsList.objects.create(user=instance)
