from django.db import models
from django.shortcuts import reverse

# Create your models here.

# pricing list
c_p = 4000
p_p = 1000
m_p = 1000


class Nysc(models.Model):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    capturing = models.BooleanField(blank=True, null=True)
    passport = models.BooleanField(blank=True, null=True)
    medical = models.BooleanField(blank=True, null=True)
    slot = models.SlugField()
    payment_status = models.BooleanField(default=False)
    payment_id = models.CharField(max_length=20, blank=True, null=True)

    def get_amount(self):
        if self.passport and self.medical:
            return c_p + p_p + m_p
        elif self.passport and not self.medical:
            return c_p + p_p
        elif not self.passport and self.medical:
            return c_p + m_p

    def get_verify_payment(self):
        return reverse("nysc:verify", kwargs={
            'pk': self.pk,
        })

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
