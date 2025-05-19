from django.db import models
from django.shortcuts import reverse
from django.core.validators import EmailValidator

# Create your models here.

# pricing list
s_c = 6500
p_p = 1000
m_p = 1500
c_m_p = 500

BatchNumber = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
]


class Batch(models.Model):
    year = models.CharField(max_length=4)
    batch = models.CharField(max_length=2, choices=BatchNumber, blank=True, null=True)
    stream = models.CharField(max_length=2, choices=BatchNumber, blank=True, null=True)
    last_no = models.IntegerField(default=0)


class Nysc(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="First Name",
        help_text="Enter your first name"
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Last Name",
        help_text="Enter your last name"
    )
    email = models.EmailField(
        validators=[EmailValidator()],
        verbose_name="Email Address",
        help_text="Enter a valid email address",
        null=False,  # Ensure database doesn't allow null
        blank=False  # Ensure form validation requires this field
    )
    capturing = models.BooleanField(
        default=False,
        verbose_name="Capturing",
        null=False,  # Ensure database doesn't allow null
        blank=False  # Ensure form validation requires this field
    )
    call_up = models.BooleanField(
        default=False,
        verbose_name="Call Up Letter",
        null=False,  # Ensure database doesn't allow null
        blank=False  # Ensure form validation requires this field
    )
    passport = models.BooleanField(
        default=False,
        verbose_name="Passport Photograph"
    )
    medical_certificate = models.BooleanField(
        default=False,
        verbose_name="Medical Fitness Certificate"
    )
    concord_printing = models.BooleanField(
        default=False,
        verbose_name="Medical Certificate Concord printing"
    )
    slot = models.SlugField()
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=20, blank=True, null=True)

    def get_amount(self):
        amount = s_c  # base charge (assuming it's always included)
        if self.passport:
            amount += p_p
        if self.medical_certificate:
            amount += m_p
        if self.concord_printing:
            amount += c_m_p
        return amount

    def get_verify_payment(self):
        return reverse("nysc:verify", kwargs={
            'pk': self.pk,
        })

    def get_preview(self):
        return reverse("nysc:preview", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
