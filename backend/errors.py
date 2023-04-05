from django.utils.translation import gettext_lazy as _

# 100xxx - General errors
INTERNAL_ERROR = {
    "code": 100001,
    "message": _("Internal error"),
}
INVALID_INPUT_ERROR = {"code": 100002, "message": _("Invalid input error")}

# 101xxx - Authentication errors
AUTHENTICATION_ERROR = {
    "code": 101001,
    "message": _("Authentication error"),
}

# 102xxx - Registration errors
USERNAME_ALREADY_TAKEN = {
    "code": 102001,
    "message": _("Username is already taken."),
}
INACCESSIBLE_REGISTRATION_STEP = {
    "code": 102002,
    "message": _("Registration step is not accessible to user."),
}
