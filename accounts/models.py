from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class FriendRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected')
    ]

    sender = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='sent_requests')
    receiver = models.ForeignKey(
        'CustomUser', on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.status})"


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name,
                          last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(email, first_name, last_name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def send_friend_request(self, receiver):
        friend_request, created = FriendRequest.objects.get_or_create(
            sender=self, receiver=receiver)
        return friend_request

    def accept_friend_request(self, sender):
        friend_request = FriendRequest.objects.get(
            sender=sender, receiver=self)
        if friend_request.status == 'pending':
            friend_request.status = 'accepted'
            friend_request.save()
            self.friends.add(sender)
            sender.friends.add(self)

    def reject_friend_request(self, sender):
        friend_request = FriendRequest.objects.get(
            sender=sender, receiver=self)
        if friend_request.status == 'pending':
            friend_request.status = 'rejected'
            friend_request.save()
