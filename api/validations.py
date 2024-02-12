from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


UserModel = get_user_model()


def custom_validation(data):
    email = data["email"].strip()
    username = data["username"].strip()
    password = data["password"].strip()

    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError("Email already exists!")

    if not password or len(password) < 8:
        raise ValidationError("Password must have min 8 characters!")

    if not username:
        raise ValidationError("Username Invalid!")
    return data


def validate_username(data):
    username = data["username"].strip()
    if not username:
        raise ValidationError("Username Invalid!")
    return True


def validate_password(data):
    password = data["password"].strip()
    if not password:
        raise ValidationError("Password Invalid!")
    return True
