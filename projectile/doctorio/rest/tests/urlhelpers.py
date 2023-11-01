from django.urls import reverse


def user_token_login_url():
    return reverse("token_obtain_pair")


def doctor_detail_url():
    return reverse("doctor.profile")


def doctor_reset_password_url():
    return reverse("doctor.reset-password")


def doctor_update_name_url():
    return reverse("doctor.update-name")


def doctor_medicine_list_url():
    return reverse("doctor.medicine-list")


def doctor_medicine_detail_url(medicine_uid):
    return reverse("doctor.medicine-detail", args=[medicine_uid])


def doctor_appointment_list_url():
    return reverse("doctor.appointment-list")


def doctor_appointment_patient_list_url():
    return reverse("doctor.appointment-patient-list")


def doctor_appointment_patient_detail_url(uid):
    return reverse("doctor.appointment-patient-detail", args=[uid])


def doctor_appointment_prescription_list_url(appointment_uid):
    return reverse("doctor.appointment-prescription-list", args=[appointment_uid])


def doctor_appointment_prescription_detail_url(appointment_uid, prescription_uid):
    return reverse(
        "doctor.appointment-prescription-detail",
        args=[appointment_uid, prescription_uid],
    )


def doctor_appointment_detail_url(appointment_uid):
    return reverse("doctor.appointment-detail", args=[appointment_uid])


def doctor_patient_list_url():
    return reverse("doctor.appointment-patient-list")


def doctor_patient_detail_url(patient_uid):
    return reverse("doctor.appointment-patient-detail", args=[patient_uid])


def doctor_appointment_prescription_list_url(appointment_uid):
    return reverse("doctor.appointment-prescription-list", args=[appointment_uid])


def doctor_appointment_prescription_detail_url(appointment_uid, prescription_uid):
    return reverse(
        "doctor.appointment-prescription-detail",
        args=[appointment_uid, prescription_uid],
    )


def doctor_appointment_feedback_url(appointment_uid):
    return reverse("doctor.appointment-feedback", args=[appointment_uid])


def doctor_appointment_patient_medical_records(appointment_uid):
    return reverse("doctor.patient-medical-records", args=[appointment_uid])
