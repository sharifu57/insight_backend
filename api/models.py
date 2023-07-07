from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='profile')
    bio = models.CharField(max_length=300, null=True, blank=True)
    passion = models.IntegerField(choices=PASSION_CHOICES, default=0, null=True, blank=True)
    location = models.CharField(max_length=300, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    image = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)
    cover = models.ImageField(upload_to='images/%Y/%m/%d',null=True, blank=True)
    
    def __Str__(self):
        return f"{user.username}"
    
    @receiver(models.signals.post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        users_without_profile = User.objects.filter(profile__isnull=True)
        for user in users_without_profile:
            UserProfile.objects.create(user=user)
            
    @receiver(models.signals.post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()