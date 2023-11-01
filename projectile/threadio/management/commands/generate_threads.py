from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from accountio.models import Organization, OrganizationUser

from appointmentio.choices import AppointmentStatus
from appointmentio.models import Appointment

from doctorio.models import Doctor

from patientio.models import Patient

from threadio.choices import InboxKind, ThreadKind
from threadio.models import Thread, Inbox


class Command(BaseCommand):
    help = "Sending message from doctor and patient side to organization and vice versa"

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            try:
                organization = Organization.objects.get(name="CardiCheck")
            except Organization.DoesNotExist:
                raise CommandError("Organization not found!")

            organization_user = OrganizationUser.objects.first().user

            # Get doctor
            doctor = (
                Doctor.objects.select_related("user")
                .filter(organization=organization)
                .first()
            )

            # Get patients
            patient = (
                Patient.objects.select_related("user")
                .filter(organization=organization)
                .first()
            )

            # Patient sending message to Organization
            patient_thread_parent = None

            try:
                patient_thread_parent = Thread.objects.get(
                    kind=ThreadKind.PARENT, participant=patient.user
                )
            except Thread.DoesNotExist:
                pass

            if not patient_thread_parent:
                patient_thread = Thread.objects.create(
                    author=patient.user,
                    participant=patient.user,
                    kind=ThreadKind.PARENT,
                    content="Hello organization I need help. I am injured",
                )
                Inbox.objects.create(
                    thread=patient_thread,
                    kind=InboxKind.PRIVATE,
                    organization=organization,
                    unread_count=1,
                    user=patient.user,
                )
                # organization_reply
                thread = Thread.objects.create(
                    parent=patient_thread,
                    kind=ThreadKind.CHILD,
                    author=organization_user,
                    participant=patient.user,
                    content="Ok dear patient we are sending an Ambulance for you.",
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Threads between patient and organization are created successfully!"
                    )
                )

            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Threads between patient and organization are already created!"
                    )
                )

            # Doctor sending message to Organization
            doctor_thread_parent = None

            try:
                doctor_thread_parent = Thread.objects.get(
                    kind=ThreadKind.PARENT, participant=doctor.user
                )
            except:
                pass

            if not doctor_thread_parent:
                doctor_thread = Thread.objects.create(
                    author=doctor.user,
                    participant=doctor.user,
                    kind=ThreadKind.PARENT,
                    content="Hello organization I am free to recieve appointments",
                )
                Inbox.objects.create(
                    thread=doctor_thread,
                    kind=InboxKind.PRIVATE,
                    organization=organization,
                    unread_count=1,
                    user=doctor.user,
                )
                # organization_reply
                thread = Thread.objects.create(
                    parent=doctor_thread,
                    kind=ThreadKind.CHILD,
                    author=organization_user,
                    participant=doctor.user,
                    content="Ok dear sir we are sending a patient for you.",
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Threads between doctor and organization are created successfully!"
                    )
                )

            else:
                self.stdout.write(
                    self.style.SUCCESS(
                       "Threads between doctor and organization are already created!"
                    )
                )

            # organization sending message to Patient
            # Get doctor
            doctor2 = Doctor.objects.select_related("user").get(
                organization=organization, slug="sahir-jaman-cardicheck"
            )

            # Get patients
            patient2 = Patient.objects.select_related("user").get(
                organization=organization, slug="osman-goni"
            )
            
            org_thread_parent = None

            try:
                org_thread_parent = Thread.objects.get(
                    kind=ThreadKind.PARENT, author=organization_user, participant=patient2.user
                )
            except:
                pass

            if not org_thread_parent:
                org_thread = Thread.objects.create(
                    author=organization_user,
                    participant=patient2.user,
                    kind=ThreadKind.PARENT,
                    content="Hello dear patient, Your appointment with Dr.Shakil has been scheduled",
                )
                Inbox.objects.create(
                    thread=org_thread,
                    kind=InboxKind.PRIVATE,
                    organization=organization,
                    unread_count=1,
                    user=patient2.user,
                )
                patient_reply = Thread.objects.create(
                    parent=org_thread,
                    author=patient2.user,
                    participant=patient2.user,
                    kind=ThreadKind.CHILD,
                    content="I don't want any doctor any more. Bye",
                )

                # organization sending message to Doctor
                org_thread = Thread.objects.create(
                    author=organization_user,
                    participant=doctor2.user,
                    kind=ThreadKind.PARENT,
                    content="Hello dear doctor, 10 patients have appointments with you. Please come as early as possible",
                )
                Inbox.objects.create(
                    thread=org_thread,
                    kind=InboxKind.PRIVATE,
                    organization=organization,
                    unread_count=1,
                    user=doctor2.user,
                )
                doctor_reply = Thread.objects.create(
                    parent=org_thread,
                    author=doctor2.user,
                    participant=doctor2.user,
                    kind=ThreadKind.CHILD,
                    content="Ok, I am coming soon",
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        "Threads between organization to doctor and patient are created successfully!"
                    )
                )

            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Threads between organization to doctor and patient are already created!"
                    )
                )
                
                
            #  Creating appointment threads between doctor and patient
            appointment = Appointment.objects.filter(patient=patient, doctor=doctor, status=AppointmentStatus.SCHEDULED).first()
            
            appointment_thread = Thread.objects.filter(appointment=appointment)
            
            if not appointment_thread:
                # Patient sending message
                Thread.objects.create(
                    appointment= appointment,
                    author = patient.user,
                    content = "Hello doctor, I have a personal question to you."
                )
                
                # Doctor sending message 
                Thread.objects.create(
                appointment=appointment,
                author=doctor.user,
                content = "Hello patient, Yeah sure. Ask me anything.",
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        "Appointment threads between doctor and patient are created Successfully!"
                    )
                )
                
                
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        "Appointment threads between doctor and patient are already created!"
                    )
                )
                
                
