def mail_sender(email, mail):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "mohamed99elsokary@gmail.com"
    password = "01111155856"
    receiver_email = email

    message = MIMEMultipart("alternative")
    message["subject"] = "Reset Password"
    message["From"] = "ACASA"
    message["to"] = receiver_email

    # Create the plain-text and HTML version of your message
    """   mail = ('''Acasa wants to tell you that :
    this is your reset password code is '''+random_code)"""

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(mail, "plain")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
