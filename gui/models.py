from django.db import models
from django.core.validators import RegexValidator, \
    MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


# Create your models here.

class PatientProfileModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    picture = models.TextField()
    first_name = models.CharField(max_length=12)
    last_name = models.CharField(max_length=35)
    gender = models.CharField(
        max_length=6,
        choices=[
            ("Male", "Male"),
            ("Female", "Female")
        ]
    )
    mobile_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must contain 10 digits: 9491432233"
    )
    mobile = models.CharField(
        max_length=10, unique=True,
        validators=[
            mobile_regex
        ]
    )
    dob = models.DateField()
    weight = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True, null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(150)
        ]
    )
    height = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        blank=True, null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    door = models.CharField(max_length=50, blank=True, null=True)
    street = models.CharField(max_length=50, blank=True, null=True)
    district = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True, null=True)
    pincode_regex = RegexValidator(
        regex=r'^\d{6}$',
        message="Pincode number must contain 6 digits: 517501"
    )
    pincode = models.CharField(
        max_length=10,
        validators=[
            pincode_regex
        ], blank=True, null=True
    )
    notes = models.TextField(null=True, blank=True)
    referral = models.ForeignKey('self', null=True, blank=True, related_name='patient_referral', on_delete=models.PROTECT)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_created", null=True, blank=True)
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "Patient Profile Record"
        verbose_name_plural = "Patient Profile Records"

