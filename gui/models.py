from django.db import models
from django.core.validators import RegexValidator, \
    MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from uuid import uuid4


# Create your models here.

class StaffProfileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    designation = models.CharField(
        max_length=255,
        choices=[
            ("Doctor", "Doctor"),
            ("Therapist", "Therapist"),
        ]
    )
    name = models.CharField(max_length=255)
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
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_created")
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Staff Record"
        verbose_name_plural = "Staff Records"


class PatientProfileModel(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    identifier = models.UUIDField(default=uuid4, unique=True, editable=False)
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

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.get_full_name()

    class Meta:
        verbose_name = "Patient Profile Record"
        verbose_name_plural = "Patient Profile Records"


class PatientTimelineModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.PROTECT, related_name='patient')
    visit = models.CharField(
        max_length=100,
        choices=[
            ("Rejuvenate Therapy", "Rejuvenate Therapy"),
            ("Panchakarma Therapy", "Panchakarma Therapy"),
            ("Consultation", "Consultation")
        ]
    )
    reason = models.CharField(
        max_length=255,
        choices=[
            ("General", "General"),
            ("Psoriasis", "Psoriasis"),
            ("Fever or Cold", "Fever or Cold")
        ]
    )
    notes = models.TextField()


class PatientScheduleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    schedule = models.ForeignKey(PatientTimelineModel, on_delete=models.PROTECT, related_name='patient_schedule')
    staff = models.ForeignKey(StaffProfileModel, on_delete=models.PROTECT, related_name='patient_staff')
    datetime = models.DateTimeField()
    type = models.CharField(
        max_length=255,
        choices=[
            ("Abhyanganam Swedanam", "Abhyanganam Swedanam"),
            ("Abhyanga Shirodhara", "Abhyanga Shirodhara"),
            ("Kashaya Dhara", "Kashaya Dhara"),
            ("Kashaya Vasti", "Kashaya Vasti"),
            ("Kati Vasti", "Kati Vasti"),
            ("Kizhi", "Kizhi"),
            ("Ksheera Dhara", "Ksheera Dhara"),
            ("Rejuvenate Therapy", "Rejuvenate Therapy"),
            ("Marma Therapy", "Marma Therapy"),
            ("Navara Kizhi", "Navara Kizhi"),
            ("Patrapinda Swedanam", "Patrapinda Swedanam"),
            ("Pizhizhil", "Pizhizhil"),
            ("Podi Kizhi", "Podi Kizhi"),
            ("Shirodhara", "Shirodhara"),
            ("Takradhara", "Takradhara"),
            ("Udavarthanam", "Udavarthanam"),
            ("Upanaham", "Upanaham"),
        ]
    )
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Patient Schedule"
        verbose_name_plural = "Patient Schedules"