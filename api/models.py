from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
class MainModel(models.Model):
    is_active = models.BooleanField(null=True, blank=True, default=True)
    is_deleted = models.BooleanField(null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    def softdelete(self):
        self.is_deleted = True
        self.is_active = False
        self.updated = pendulum.now()
        self.save()

    class Meta:
        abstract = True
        
PASSION_CHOICES = (
    (1, 'Marketing'),
    (2, 'Science and Technology'),
    (3, 'Sports'),
    (4, 'Sex and Life')
)
class UserProfile(MainModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    bio = models.CharField(max_length=300, null=True, blank=True)
    passion = models.IntegerField(choices=PASSION_CHOICES, default=0, null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)
    cover = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)
    
    def __str__(self):
        return self.user.email
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
    

class Post(MainModel):
    code = models.CharField(max_length=300, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    attachment = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)
    geolocation = models.CharField(max_length=300, blank=True, null=True)
    
    def __str__(self):
        return self.code


class Comment(MainModel):
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, related_name='comment', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email  