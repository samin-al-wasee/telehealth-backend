from appointmentio.choices import (
    AppointmentType,
    AppointmentFor,
    SymptomPeriod,
    AppointmentStatus,
)
from core.choices import BloodGroups, UserGender


def user_patient_payload(organization):
    return {
        "first_name": "john",
        "last_name": "doe",
        "email": "john@gmail.com",
        "phone": "+8802222222222",
        "weight": "19",
        "hight": "4.0",
        "gender": UserGender.MALE,
        "password": "test123pass",
        "blood_group": BloodGroups.O_POSITIVE,
        "date_of_birth": "2000-02-02",
        "organization_uid": organization.uid,
        "social_security_number": "983-23-5783",
    }


def patient_appointment_payload(organization):
    payload = {
        "appointment_type": AppointmentType.CONSULTATION,
        "complication": "Headache",
        "organization": organization,
        "appointment_date": "2023-07-06",
        "appointment_time": "08:30",
        "weight": 22,
        "height": 3.3,
        "age": 12,
    }

    return payload


def appointment_patient_payload(organization, date, time):
    payload = {
        "appointment_for": AppointmentFor.ME,
        "appointment_type": AppointmentType.CONSULTATION,
        "gender": UserGender.MALE,
        "blood_group": BloodGroups.O_POSITIVE,
        "symptom_period": SymptomPeriod.DAYS,
        "organization": organization.uid,
        "appointment_date": date,
        "appointment_time": time,
        "is_previous": True,
    }

    return payload


def appointment_patient_status_complete_payload(organization, date, time):
    payload = {
        "status": AppointmentStatus.COMPLETED,
        "organization": organization.uid,
        "appointment_date": date,
        "appointment_time": time,
    }

    return payload


def patient_appointment_refill_payload():
    payload = {"message": "This is a test refill."}
    return payload


def patient_login_payload():
    payload = {"phone": "+8802222222222", "password": "test123pass"}

    return payload


def patient_appointment_feedback_payload():
    payload = {
        "rating": 2,
        "comment": "Not too good",
    }
    return payload
