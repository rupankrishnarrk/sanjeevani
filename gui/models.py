from django.db import models
from django.core.validators import RegexValidator, \
    MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from uuid import uuid4
from gui import validators


# Create your models here.
class AllergiesModel(models.Model):
    id = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.id


class BranchModel(models.Model):
    name = models.CharField(
        primary_key=True,
        max_length=255,
        choices=[
            ("Karkambadi Road", "Karkambadi Road")
        ]
    )
    address = models.TextField()
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="location_created")
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="location_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Branch"
        verbose_name_plural = "Branches"


class UserProfileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='userprofile')
    designation = models.CharField(
        max_length=255,
        choices=[
            ("Staff", "Staff"),
            ("Admin", "Admin"),
            ("Doctor", "Doctor"),
            ("Manager", "Manager"),
            ("Therapist", "Therapist"),
            ("Receptionist", "Receptionist"),
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
    branch = models.ForeignKey(BranchModel, on_delete=models.PROTECT)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_created")
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="staff_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


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
        max_digits=5,
        decimal_places=2,
        blank=True, null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(150)
        ]
    )
    height = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True, null=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )
    allergies = models.ManyToManyField(AllergiesModel, blank=True)
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
    branch = models.ForeignKey(BranchModel, on_delete=models.PROTECT)
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
    patient = models.ForeignKey(PatientProfileModel, on_delete=models.PROTECT, related_name='patient_timeline')
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
    follow_up = models.DateField()
    follow_up_status = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    branch = models.ForeignKey(BranchModel, on_delete=models.PROTECT)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patienttimeline_created", null=True, blank=True)
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patienttimeline_modified", null=True, blank=True)

    class Meta:
        ordering = ['-createdDate']
        verbose_name = "Patient Timeline"
        verbose_name_plural = "Patient Timelines"


class TreatmentTypesModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField(
        max_length=255,
        choices=(
            ("General",
             (("Other", "Other"),
              ("Rejuvenate Therapy", "Rejuvenate Therapy"))),
            ("Panchakarma",
             (("Abhyanganam Swedanam Therapy", "Abhyanganam Swedanam Therapy"),
              ("Abhyanga Shirodhara Therapy", "Abhyanga Shirodhara Therapy"),
              ("Kashaya Dhara Therapy", "Kashaya Dhara Therapy"),
              ("Kashaya Vasti Therapy", "Kashaya Vasti Therapy"),
              ("Kati Vasti Therapy", "Kati Vasti Therapy"),
              ("Kizhi Therapy", "Kizhi Therapy"),
              ("Ksheera Dhara Therapy", "Ksheera Dhara Therapy"),
              ("Marma Therapy Therapy", "Marma Therapy Therapy"),
              ("Navara Kizhi Therapy", "Navara Kizhi Therapy"),
              ("Patrapinda Swedanam Therapy", "Patrapinda Swedanam Therapy"),
              ("Pizhizhil Therapy", "Pizhizhil Therapy"),
              ("Podi Kizhi Therapy", "Podi Kizhi Therapy"),
              ("Shirodhara Therapy", "Shirodhara Therapy"),
              ("Takradhara Therapy", "Takradhara Therapy"),
              ("Udavarthanam Therapy", "Udavarthanam Therapy"),
              ("Upanaham Therapy", "Upanaham Therapy"))),
        ), unique=True
    )
    price = models.IntegerField()
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatmenttypes_created", null=True, blank=True)
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatmenttypes_modified", null=True, blank=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Treatment Type"
        verbose_name_plural = "Treatment Types"


class PatientScheduleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    schedule_timeline = models.ForeignKey(PatientTimelineModel, on_delete=models.PROTECT, related_name='patient_schedule_timeline')
    treatment = models.ForeignKey(TreatmentTypesModel, on_delete=models.PROTECT)
    staff = models.ManyToManyField(UserProfileModel, related_name='patient_staff')
    datetime = models.DateTimeField()
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Patient Schedule"
        verbose_name_plural = "Patient Schedules"


class PatientFilesModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    files_timeline = models.ForeignKey(PatientTimelineModel, on_delete=models.PROTECT,
                                          related_name='patient_files_timeline')
    file_type = models.CharField(
        max_length=255,
        choices=[
            ("Medical Report", "Medical Report"),
            ("Radiology Report", "Radiology Report"),
            ("Laboratory Report", "Laboratory Report"),
            ("Medical Prescription", "Medical Prescription")
        ]
    )
    file = models.FileField()

    class Meta:
        verbose_name = "Patient File"
        verbose_name_plural = "Patient Files"


class AppointmentModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255)
    visit = models.CharField(
        max_length=255,
        choices=[
            ("Therapy", "Therapy"),
            ("Medicine", "Medicine"),
            ("Consultation", "Consultation"),
        ]
    )
    phone_regex = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must contain 10 digits: 9491432233"
    )
    mobile = models.CharField(
        max_length=10,
        validators=[
            phone_regex
        ]
    )
    starttime = models.DateTimeField(validators=[validators.validate_time_in_work_hours])
    status = models.CharField(
        blank=True, null=True,
        max_length=255,
        choices=[
            ('Completed', 'Completed'),
            ('Not Interested', 'Not Interested'),
            ('Missed', 'Missed'),
        ]
    )
    notes = models.TextField(blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_created", null=True, blank=True)
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"


class ReminderModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    task = models.CharField(max_length=255)
    starttime = models.DateTimeField()
    status = models.BooleanField()
    notify = models.ManyToManyField(User, related_name='notify' )
    notes = models.TextField(blank=True, null=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminder_created", null=True, blank=True)
    modifiedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reminder_modified", null=True, blank=True)
    createdDate = models.DateTimeField(auto_now_add=True)
    modifiedDate = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"