from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@shared_task
def send_user_update_email(first_name, email):
    """
        Sends an email to the user after updating their profile with the new information.
    """

    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)

    logger.info(f"Enviando email para {email}...")

    try:
        subject = "Perfil Atualizado com Sucesso"
        from_email = "no-reply@swapp.com"

        # Rende the email templates
        html_content = render_to_string("emails/user_updated.html", {"first_name": first_name})
        text_content = render_to_string("emails/user_updated.txt", {"first_name": first_name})

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        msg.send()

        logger.info(f"Email enviado para {email} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {email}. {str(e)}")

@shared_task
def send_user_delete_email(first_name, email):
    """
        Sends an email to the user after deleting their account.
    """

    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)

    logger.info(f"Enviando email para {email}...")

    try:
        subject = "Conta Deletada com Sucesso"
        from_email = "no-reply@swapp.com"

        # Rende the email templates
        html_content = render_to_string("emails/user_deleted.html", {"first_name": first_name})
        text_content = render_to_string("emails/user_deleted.txt", {"first_name": first_name})

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        msg.send()

        logger.info(f"Email enviado para {email} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {email}. {str(e)}")

@shared_task
def send_user_register_email(first_name, email):
    """
        Sends an email to the user after registering their account.
    """

    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)

    logger.info(f"Enviando email para {email}...")

    try:
        subject = "Cadastro Efetuado com Sucesso"
        from_email = "no-reply@swapp.com"

        # Rende the email templates
        html_content = render_to_string("emails/user_registered.html", {"first_name": first_name})
        text_content = render_to_string("emails/user_registered.txt", {"first_name": first_name})

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        msg.send()

        logger.info(f"Email enviado para {email} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {email}. {str(e)}")

@shared_task
def send_user_change_password_email(first_name, email):
    """
        Sends an email to the user after changing their password.
    """

    from celery.utils.log import get_task_logger
    logger = get_task_logger(__name__)

    logger.info(f"Enviando email para {email}...")

    try:
        subject = "Senha Alterada com Sucesso"
        from_email = "no-reply@swapp.com"

        # Rende the email templates
        html_content = render_to_string("emails/user_password_changed.html", {"first_name": first_name})
        text_content = render_to_string("emails/user_password_changed.txt", {"first_name": first_name})

        # Create the email
        msg = EmailMultiAlternatives(subject, text_content, from_email, [email])
        msg.attach_alternative(html_content, "text/html")

        # Send the email
        msg.send()

        logger.info(f"Email enviado para {email} com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao enviar email para {email}. {str(e)}")
