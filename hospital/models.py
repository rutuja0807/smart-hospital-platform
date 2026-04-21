from django.db import models


class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    fees = models.DecimalField(max_digits=8, decimal_places=2)

    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Patient(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField()

    # ✅ BACK TO SIMPLE TIME
    time = models.TimeField()

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], default='pending')

    meeting_link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # ✅ prevent double booking
        unique_together = ('doctor', 'date', 'time')

    def __str__(self):
        return f"{self.patient.name} - {self.doctor.name} - {self.date} - {self.time}"