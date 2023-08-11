from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_templated_email(template, context, title, receiver):
    html_content = render_to_string(template, context=context)
    text_content = strip_tags(html_content)
    msg = EmailMultiAlternatives(
        title,
        text_content,
        settings.EMAIL_HOST_USER,
        [receiver],
        headers={},
    )
    msg.attach_alternative(html_content, "text/html")
    return msg.send()
