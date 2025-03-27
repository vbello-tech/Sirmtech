from django.db import models
from django.shortcuts import reverse
from django.core.validators import EmailValidator

# Create your models here.

# pricing list
c_p = 4000
p_p = 1000
m_p = 1000


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
        help_text="Do you need capturing?"
    )
    passport = models.BooleanField(
        default=False,
        verbose_name="Passport",
        help_text="Do you need passport?"
    )
    medical_certificate = models.BooleanField(
        default=False,
        verbose_name="Medical Certificate",
        help_text="Do you want medical certificate?"
    )
    slot = models.SlugField()
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=20, blank=True, null=True)

    def get_amount(self):
        if self.passport and self.medical_certificate:
            return c_p + p_p + m_p
        elif self.passport and not self.medical_certificate:
            return c_p + p_p
        elif not self.passport and self.medical_certificate:
            return c_p + m_p

    def get_verify_payment(self):
        return reverse("nysc:verify", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
