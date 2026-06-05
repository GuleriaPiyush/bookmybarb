from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Service(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    duration_minutes = models.PositiveIntegerField(default=30)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    required_slot = models.IntegerField(default=1)

class ScheduleTemplate(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TemplateSlot(models.Model):
    template = models.ForeignKey(ScheduleTemplate, on_delete=models.CASCADE, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['start_time']
        unique_together = ('template', 'start_time')

class Slot(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ('date', 'start_time')

class Booking(models.Model):
    status_choice = [
        ('PENDING','Pending Approval'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]

    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='bookings_as_service')
    slots = models.ManyToManyField(Slot, related_name='bookings_as_slot')
    status = models.CharField(max_length=15, choices=status_choice, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

class ShopSetting(models.Model):
    auto_accept_booking = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)