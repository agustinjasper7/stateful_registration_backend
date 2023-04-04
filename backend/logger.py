import json
import logging

from django.conf import settings


def debug(*messages, **kwargs):
    log(*messages, log_level="debug", **kwargs)


def info(*messages, **kwargs):
    log(*messages, log_level="info", **kwargs)


def warn(*messages, **kwargs):
    log(*messages, log_level="warning", **kwargs)


def error(*messages, **kwargs):
    log(*messages, log_level="error", **kwargs)


def fatal(*messages, **kwargs):
    log(*messages, log_level="fatal", **kwargs)


class StringEncoder(json.JSONEncoder):
    def default(self, o):
        return str(o)


def get_client_ip(request):
    if hasattr(request, "META"):
        collection = request.META
    else:
        try:
            collection = request.transport.req
        except Exception:
            return "127.0.0.1"

    x_forwarded_for = collection.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return collection.get("REMOTE_ADDR")


def log(
    *messages,
    label=None,
    log_level="debug",
    request=None,
    context=None,
    logger=None,
):
    if log_level == "debug" and not settings.DEBUG:
        return

    if not logger:
        logger = logging.getLogger("default")

    full_message = ""
    if request:
        full_message += f"[{get_client_ip(request)}] "

        user = request.user
        if user and user.is_authenticated:
            full_message += f"[{user.email}] "

    if label:
        full_message += f"{label}: "

    for message in messages:
        full_message += message

    if context:
        context_data = json.dumps(
            context,
            cls=StringEncoder,
            indent=2,
        )
        full_message += f"\nContext={context_data}"

    logging_method = getattr(logger, log_level, None)
    logging_method(full_message)
