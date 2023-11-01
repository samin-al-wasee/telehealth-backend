from appointmentio.choices import AppointmentType, MedicineStatus
from appointmentio.models import Ingredient


def doctor_login_payload():
    return {"phone": "+8801999999999", "password": "123456"}


def doctor_payload(department):
    return {
        "first_name": "Dr.",
        "last_name": "Dipu",
        "phone": "+8801999999999",
        "email": "doctor.dipu@example.com",
        "registration_no": "12233",
        "experience": 5,
        "consultation_fee": 100.00,
        "follow_up_fee": 500.00,
        "check_up_fee": 500.00,
        "password": "123456",
        "departments": department,
        "ssn": "376283",
    }


def doctor_appointment_payload(doctor):
    return {
        "appointment_type": AppointmentType.CONSULTATION,
        "complication": "Headache",
        "doctor": doctor,
    }


def doctor_password_reset():
    return {
        "password": "123456",
        "new_password": "asma1234567",
        "confirm_password": "asma1234567",
    }


def prescription_payload(medicine):
    return {
        "medicine_doses": medicine,
    }


def medicine_payload():
    return {
        "name": "Napa",
        "status": MedicineStatus.ACTIVE,
        "expiration_date": "2024-07-12",
        "ingredient": Ingredient,
    }


def doctor_appointment_feedback_payload():
    return {
        "rating": 2,
        "comment": "decent patient",
    }
