import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_verification_email(email, token):

    # NOTE replace with env from this hardcoded part
    sender_email = 'samiricium2024@gmail.com'  # Your email address
    password = "eegd ehsz hokh kiyf"  # Your email password
    domain = "http://192.168.11.230:5000"

    subject = "Verify Your Colab Account"
    message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2 style="color: #007bff;">Welcome to Colab!</h2>
            <p style="color: #333;">Thank you for signing up for Colab. To complete your registration, please click the link below to verify your email address:</p>
            <p style="margin-bottom: 30px;"><a href='{domain}/verify_email?token={token}' style="padding: 10px 20px; background-color: #007bff; color: #fff; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
            <p style="color: #333;">If you did not create an account on Colab, you can safely ignore this email.</p>
            <p style="color: #777; font-size: 12px; margin-top: 20px;">This email was sent by Colab. Please do not reply to this email.</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except Exception as e:
        raise e
