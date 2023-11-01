from django.urls import reverse


def user_token_login_url():
    return reverse("token_obtain_pair")


def patient_appointment_list_url():
    return reverse("patient.appointment-list")


def patient_appointment_detail_url(appointment_uid):
    return reverse("patient.appointment-detail", args=[appointment_uid])


def prescription_list_url():
    return reverse("patient.prescription-list")


def prescription_detail_url(prescription_uid):
    return reverse("patient.prescription-detail", args=[prescription_uid])


def patient_appointment_refill_url(appointment_uid):
    return reverse("patient.appointment-refill-list", args=[appointment_uid])


def patient_appointment_refill_detail_url(appointment_uid, uid):
    return reverse("patient.appointment-refill-detail", args=[appointment_uid, uid])


def patient_detail_url(uid):
    return reverse("patient.detail", args=[uid])


def patient_doctor_medicine_list_url():
    return reverse("patient.doctor-medicine-list")


def patient_seek_help_list_url():
    return reverse("patient.seek-help-list")


def patient_completed_appointment_list_url():
    return reverse("patient.completed-appointment-list")


def patient_appointment_time_slot_list_url():
    return reverse("patient.appointment-slot-list")


def patient_appointment_prescription_list_url(appointment_uid):
    return reverse("patient.appointment-prescription-list", args=[appointment_uid])


def patient_appointment_prescription_detail_url(appointment_uid, prescription_uid):
    return reverse(
        "patient.appointment-prescription-detail",
        args=[appointment_uid, prescription_uid],
    )


def patient_appointment_feedback_url(appointment_uid):
    return reverse("patient.appointment-feedback", args=[appointment_uid])
