import os
from django.db import models

# User class to store user information
class User(models.Model):
    first_name = models.CharField(max_length=100, default='John')
    last_name = models.CharField(max_length=100, default='Doe')
    email = models.EmailField(default='placeholder@example.com')

    def __str__(self):
        return self.email

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    organization = models.CharField(max_length=100)
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    publish = models.BooleanField()
    anonymous_account = models.BooleanField(null=True, blank=True)
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d %H:%M:%S')
    
class ReportFile(models.Model):
    report = models.ForeignKey(Report, related_name='report_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='org-report-uploaded-files/')

    def filename(self):
        return os.path.basename(self.file.name)

    def file_url(self):
        if self.file:
            return self.file.url
        return None
