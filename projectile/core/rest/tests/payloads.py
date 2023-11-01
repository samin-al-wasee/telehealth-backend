from core.choices import UserGender, BloodGroups


def user_patient_payload(organization):
    return {
        "first_name": "sahir",
        "last_name": "jaman",
        "email": "sahir@gmail.com",
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


def user_login_payload():
    payload = {
        "phone": "+8802222222222",
        "password": "test123pass"
    }
    return payload
