import json
from collections.abc import Sequence

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.template import Template

from github import Github


def build_send_mail_json(send_to,
                         template: str,
                         subject: str,
                         template_data: dict = None):
    if not isinstance(send_to, Sequence) and not isinstance(send_to, str):
        raise TypeError('send_to must be a sequence of email addresses '
                        'or one email address as str!')
    return json.dumps(locals())


def build_send_reminder_json(send_to,
                             object_pk,
                             template: str,
                             subject: str,
                             template_data: dict = None):
    if not isinstance(send_to, Sequence) and not isinstance(send_to, str):
        raise TypeError('send_to must be a sequence of email addresses '
                        'or one email address as str!')
    return json.dumps(locals())


def send_mail(send_to, subject, template, context={}):
    try:
        template = get_template(f'email/{template}')
    except TemplateDoesNotExist:
        template = Template(template)

    content = template.render(context)
    if isinstance(send_to, str):
        send_to = [send_to]

    send_email = EmailMessage(
        body=content,
        subject=settings.EMAIL_SUBJECT_PREFIX + subject,
        from_email=settings.SERVER_EMAIL,
        reply_to=settings.REPLY_EMAIL,
        to=send_to,
        )
    send_email.content_subtype = "html"
    send_email.send()


def render_site_template(template, context):
    try:
        template = get_template(f'site/{template}')
    except TemplateDoesNotExist:
        template = Template(template)

    return template.render(context)


def push_site_template(file_path, content):
    content = content.encode()
    g = Github(settings.GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(settings.STATIC_SITE_REPO)
    f = repo.get_contents(file_path)
    repo.update_file(f.path, f'Update {file_path}', content, f.sha)
