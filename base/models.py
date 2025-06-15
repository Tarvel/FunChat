from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def validate_img(file):
    valid_extensions = (".jpg", ".jpeg", ".png", ".svg")
    if not file.name.lower().endswith(valid_extensions):
        raise ValidationError(
            "Unsupported file extension. Use .jpg, .jpeg, .png or .svg"
        )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=200, verbose_name="First name", null=False)
    last_name = models.CharField(max_length=200, verbose_name="Last name", null=False)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(
        upload_to="profile_images/",
        default="profile_images/default.svg",
        blank=True,
        null=True,
        validators=[validate_img],
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name="participants", blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.body[0:40]
