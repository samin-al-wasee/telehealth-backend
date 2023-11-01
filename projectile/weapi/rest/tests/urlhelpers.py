from django.urls import reverse


def user_token_login_url():
    return reverse("token_obtain_pair")


def we_detail_url():
    return reverse("we.detail")


def we_doctor_list_url():
    return reverse("we.doctor-list")


def we_doctor_detail_url(uid):
    return reverse("we.doctor-detail", args=[uid])


def we_patient_list_url():
    return reverse("we.patient-list")


def we_patient_detail_url(patient_uid):
    return reverse("we.patient-detail", args=[patient_uid])


def we_patient_appointment_list_url(patient_uid):
    return reverse("we.patient-appointment-list", args=[patient_uid])


def we_patient_upcoming_appointment_list_url(patient_uid):
    return reverse("we.patient-upcoming-appointment-list", args=[patient_uid])


def we_patient_completed_appointment_list_url(patient_uid):
    return reverse("we.patient-completed-appointment-list", args=[patient_uid])


def we_appointment_list_url():
    return reverse("we.appointment-list")


def we_appointment_detail_url(appointment_uid):
    return reverse("we.appointment-detail", args=[appointment_uid])


def we_organization_list_url():
    return reverse("we.organization-list")


def we_organization_refill_list_url():
    return reverse("we.refill-list")


def we_organization_refill_detail_url(refill_uid):
    return reverse("we.refill-detail", args=[refill_uid])


def we_organization_department_list_url():
    return reverse("we.organization-department-list")


def we_organization_department_detail_url(uid):
    return reverse("we.organization-department-detail", args=[uid])


def we_appointment_schedule_create_url():
    return reverse("we.appointment-schedule-list")


def we_appointment_time_slot_list_url():
    date = "2023-07-21"
    return reverse("we.appointment-time-slot-list")+f"?date={date}"


def we_doctor_appointment_list_url(doctor_uid):
    return reverse("we.doctor-appointments-list", args=[doctor_uid])


def we_doctor_appointment_detail_url(doctor_uid, appointment_uid):
    return reverse("we.doctor-appointment-detail", args=[doctor_uid, appointment_uid])


def we_doctor_appointment_prescription_list_url(doctor_uid, appointment_uid):
    return reverse(
        "we.doctor-appointment-prescription-list", args=[doctor_uid, appointment_uid]
    )


def we_doctor_appointment_prescription_detail_url(
        doctor_uid, appointment_uid, prescription_uid
):
    return reverse(
        "we.doctor-appointment-prescription-detail",
        args=[doctor_uid, appointment_uid, prescription_uid],
    )
