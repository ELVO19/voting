from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Student(models.Model):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=128)
    date_registered = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password_hash)

    def __str__(self):
        return self.email


class Category(models.Model):
    name = models.CharField(max_length=50)  # e.g. "Class Representative"
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='candidates')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='candidates/', blank=True, null=True)
    bio = models.TextField(blank=True)

    def vote_count(self):
        return self.vote_set.filter(is_invalidated=False).count()

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Vote(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_invalidated = models.BooleanField(default=False)
    invalidation_reason = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.student.email} -> {self.candidate.name}"

class AllowedVoter(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email