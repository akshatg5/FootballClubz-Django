from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    pass

#the first class is of the Football Club containing all the information about the club
class FootballClub(models.Model):
    #defining all the information we need to write about a football team. 
    club_name = models.CharField(max_length=128)
    club_country = models.CharField(max_length=128)
    club_stadium = models.CharField(max_length=128,null=True)
    club_logo = models.ImageField(upload_to='club_logos/')
    club_desc = models.TextField()
    club_manager = models.CharField(max_length=128)
    networth = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    added_by = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    
    def __str__(self):
        return f"{self.club_name}"
    
class Player(models.Model):
    player_img = models.ImageField(upload_to='players/',null=True)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    age = models.PositiveIntegerField()
    position = models.CharField(max_length=64)
    nationality = models.CharField(max_length=128,null=True,blank=True)
    football_club = models.ForeignKey('FootballClub',on_delete=models.CASCADE,related_name="club_squad")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_who_liked_club")
    liked_club = models.ForeignKey(FootballClub,on_delete=models.CASCADE,related_name="liked_by_users",null=True,blank=True)
    liked_player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name="liked_by_users",null=True,blank=True)
    
    def __str__(self):
        if self.liked_club:
            return f"{self.user.username} liked {self.liked_club.club_name}"
        elif self.liked_player:
            return f"{self.user.username} liked {self.liked_player.first_name} {self.liked_player.last_name}"

class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(max_length=640)
    commented_club = models.ForeignKey(FootballClub,on_delete=models.CASCADE,related_name="comments",null=True)
    commented_player = models.ForeignKey(Player,on_delete=models.CASCADE,related_name="comments",null=True)
    
    def __str__(self):
        if self.commented_club:
            return f"Comment by {self.user.username} on {self.commented_club.club_name}"
        elif self.commented_player:
            return f"Comment by {self.user.username} on {self.commented_player.first_name} {self.commented_player.last_name}"
    

    
    
    
