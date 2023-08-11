import logging

from django.conf import settings
from kavenegar import KavenegarAPI, APIException, HTTPException


def send_sms():
    pass


def sms_character_replace(text):
    """
        replace space in text to send by kavenegar
    :param text: text
    :type text: str
    :return: replaced space text
    :rtype: str
    """
    return str(text).replace(" ", "‌").replace("_", "-").replace("_", "‌")  # kavenegar error 431


def send_sms_template(phone_number, template, **kwargs):
    api = KavenegarAPI(settings.KAVENEGAR_AUTH_TOKEN)

    logger = logging.getLogger("django")

    for key, value in kwargs.items():
        if key.startswith("token"):
            kwargs[key] = sms_character_replace(value)

    params = {
        **kwargs,
        "receptor": phone_number,
        "template": template,
        "sender": settings.KAVENEGAR_SENDER_LINE,
    }
    try:
        response = api.verify_lookup(params)
        logger.info(str(response))
        return response
    except APIException as api_exception:
        logger.error(api_exception.args[0].decode("utf-8"))
        raise api_exception
    except HTTPException as http_exception:
        logger.error(http_exception.args[0].decode("utf-8"))
        raise http_exception
