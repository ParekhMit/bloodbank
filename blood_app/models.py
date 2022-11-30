from django.db import models
from django.contrib.auth.models import User


SEX = ((0, 'Female'),(1, 'Male'))
DESEASE = ((0, 'Alpha thalasemia'), (1, 'beta thalasemia'), (2, 'normal'))
class Category(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    pincode = models.CharField(max_length=100, null=True)
    otp = models.CharField(max_length=100, null=True)
    password = models.CharField(max_length=100, null=True)
    blood_group = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    dob = models.DateField(null=True)
    disease = models.CharField(max_length=100, null=True, blank=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username



class Blood_Donation(models.Model):
    status = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    blood_group = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    place = models.CharField(max_length=100, null=True, blank=True)
    blood_pressure = models.CharField(max_length=100, null=True, blank=True)
    blood_units = models.CharField(max_length=100, null=True, blank=True)
    purpose = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True,null=True)
    donation_date = models.DateField(null=True, blank=True)
    recieve_date = models.DateField(null=True, blank=True)
    active = models.BooleanField(null=True, blank=True, default=False)
    hiv = models.BooleanField(null=True, blank=True, default=False)
    hapetitis_c = models.BooleanField(null=True, blank=True, default=False)
    hapetitis_b = models.BooleanField(null=True, blank=True, default=False)
    syphilis = models.BooleanField(null=True, blank=True, default=False)
    active = models.BooleanField(null=True, blank=True, default=False)
     

    def __str__(self):
        return self.user.user.username

class Order(models.Model):
    status = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    blood_donation = models.ForeignKey(Blood_Donation, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=100, null=True, blank=True)
    blood_units = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.user.user.username

class TestPredict(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    symptom = models.TextField(null=True, blank=True)
    result = models.TextField(null=True, blank=True)
    prediction = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username