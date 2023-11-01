from appointmentio.choices import AppointmentType, AppointmentFor, AppointmentStatus


def user_login_payload():
    return {"phone": "+8801111111111", "password": "test123pass"}


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


def appointment_payload():
    return {
        "appointment_type": AppointmentType.CONSULTATION,
        "appointment_for": AppointmentFor.ME,
        "status": AppointmentStatus.REQUESTED,
        "is_visible": True,
        "phone": "+8802222222222",
    }


def appointment_with_doctor_payload(doctor, date, time):
    return {
        "appointment_type": AppointmentType.CONSULTATION,
        "appointment_for": AppointmentFor.SOMEONE_ELSE,
        "status": AppointmentStatus.SCHEDULED,
        "is_visible": True,
        "phone": "+8802222222222",
        "doctor_uid": doctor,
        "appointment_date": date,
        "appointment_time": time,
    }


def completed_appointment_payload():
    return {
        "appointment_type": AppointmentType.CONSULTATION,
        "appointment_for": AppointmentFor.ME,
        "status": AppointmentStatus.COMPLETED,
        "is_visible": True,
        "phone": "+8802222222222",
    }


def appointment_schedule_payload():
    return {
        "appointment_duration": "00:20:00",
        "appointment_interval": "00:10:00",
        "appointment_fee": 500.0,
        "consultation_fee": 300.0,
        "follow_up_fee": 200.0,
        "checkup_fee": 400.0,
        "week_days": [
            {
                "day": "SATURDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "SUNDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "MONDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "TUESDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "WEDNESDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "THURSDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "8:00:00",
                        "end_time": "12:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "12:00:00",
                        "end_time": "17:00:00",
                    },
                ],
            },
            {
                "day": "FRIDAY",
                "off_day": False,
                "shifts": [
                    {
                        "shift_label": "Morning",
                        "start_time": "9:00:00",
                        "end_time": "11:00:00",
                    },
                    {
                        "shift_label": "Afternoon",
                        "start_time": "2:00:00",
                        "end_time": "4:00:00",
                    },
                ],
            },
        ],
    }


def department_payload():
    return {"name": "Medicine"}


def prescription_payload(medicine_uid):
    return {
        "medicine_doses": [
            {
                "medicine_uid": medicine_uid,
                "interval": "Once daily",
                "duration": "7 days",
                "indication": "Take after meals",
            }
        ],
        "recommendation_list": "Recommendation_1",
        "diagnosis_list": "Diagnosis_1",
        "investigation_list": "Investigation_1",
        "examination_list": "Examination_1",
        "primary_disease_list": "Primary_1",
    }
