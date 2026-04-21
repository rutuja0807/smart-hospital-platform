from django.shortcuts import render, redirect
from .models import Doctor, Patient, Appointment
from django.contrib.auth.decorators import login_required
print("VIEWS FILE LOADED")
print("PATIENTS:", Patient.objects.all())
print("DOCTORS:", Doctor.objects.all())

@login_required(login_url='/login/')
def home(request):
    query = request.GET.get('q')

    if query:
        doctors = Doctor.objects.filter(
            name__icontains=query
        ) | Doctor.objects.filter(
            specialization__icontains=query
        )
    else:
        doctors = Doctor.objects.all()

    return render(request, 'index.html', {'doctors': doctors})


def register_patient(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        Patient.objects.create(
            name=name,
            email=email,
            phone=phone
        )
        return redirect('/index/')

    return render(request, 'register.html')


@login_required(login_url='/login/')
def book_appointment(request):
    patients = Patient.objects.all()
    doctors = Doctor.objects.all()
    appointments = Appointment.objects.all()

    if request.method == 'POST':
        patient_id = request.POST.get('patient')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not (patient_id and doctor_id and date and time):
            return render(request, 'appointment.html', {
                'error': 'All fields are required!',
                'patients': patients,
                'doctors': doctors,
                'appointments': appointments
            })

        patient = Patient.objects.get(id=patient_id)
        doctor = Doctor.objects.get(id=doctor_id)

        exists = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time
        ).exists()

        if exists:
            return render(request, 'appointment.html', {
                'error': 'This time slot is already booked!',
                'patients': patients,
                'doctors': doctors,
                'appointments': appointments
            })

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            date=date,
            time=time,
            status="confirmed",
            meeting_link="https://meet.jit.si/" + str(patient.name)
        )

        return redirect('/appointment/')

    return render(request, 'appointment.html', {
        'patients': patients,
        'doctors': doctors,
        'appointments': appointments
    })


def cancel_appointment(request, id):
    app = Appointment.objects.get(id=id)
    app.status = "cancelled"
    app.save()
    return redirect('/appointment/')


@login_required(login_url='/login/')
def dashboard(request):
    return render(request, 'dashboard.html')


def doctor_detail(request, id):
    doctor = Doctor.objects.get(id=id)
    return render(request, 'doctor_detail.html', {'doctor': doctor})



@login_required(login_url='/login/')
def dashboard(request):
    total_doctors = Doctor.objects.count()
    total_patients = Patient.objects.count()
    total_appointments = Appointment.objects.count()

    booked = Appointment.objects.filter(status='confirmed').count()
    cancelled = Appointment.objects.filter(status='cancelled').count()

    return render(request, 'dashboard.html', {
        'total_doctors': total_doctors,
        'total_patients': total_patients,
        'total_appointments': total_appointments,
        'booked': booked,
        'cancelled': cancelled
    })