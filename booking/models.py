# booking/models.py

from django.db import models

class FitnessClass(models.Model):
    CLASS_TYPES = (
        ('Yoga', 'Yoga'),
        ('Zumba', 'Zumba'),
        ('HIIT', 'HIIT'),
    )
    name = models.CharField(max_length=100, choices=CLASS_TYPES)
    instructor = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    available_slots = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name} on {self.datetime} by {self.instructor}"


class Booking(models.Model):
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField()
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client_name} booked {self.fitness_class}"
