from django.conf import settings

# Log Configuration
DEBUG = getattr(settings, "DEBUG", False)
SENSITIVE_DATA_TAGS = getattr(settings, "SENSITIVE_DATA_TAGS", [])
