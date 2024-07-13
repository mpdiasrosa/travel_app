import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_addrs, body):
    from_addr = "rqc5xnhh2drd6rt7@ethereal.email"
    login = "rqc5xnhh2drd6rt7@ethereal.email"
    password = "ryk7B9sg7zzy2vWbJ1"

    msg = MIMEMultipart()
    msg["from"] = "lilly@trip.com"
    msg["to"] = ', '.join(to_addrs)

    msg["Subject"] = "Trip created!"
    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP("smtp.ethereal.email", 587)
    server.starttls()
    server.login(login, password)
    text = msg.as_string()

    for email in to_addrs:
        server.sendmail(from_addr, email, text)

    server.quit()