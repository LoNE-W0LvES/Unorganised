import smtplib, ssl

from email.message import EmailMessage


def send_mail(receiver_email, exp_date):
    sender_email = "w3961500@gmail.com"
    password = "cjorlgqsjqpumwqk"

    message = EmailMessage()
    message["Subject"] = "Renew safe deposit box renting time."
    message["From"] = sender_email
    message["To"] = receiver_email
    message.set_content(f'Hi,\nYour safe deposit box renting time is almost over.\nYou have {exp_date} days left. \nWe hope you renew the subscription and stay with us.')
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
