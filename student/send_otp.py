import smtplib


def send_mail(name,email_address,code):
    sender = 'random.om.ok@gmail.com'
    password = 'Om18012001'

    to = [email_address]
    subject = name + "your OTP for Attendance System registeration"
    body = code

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sender, ", ".join(to), subject, body)

    print(email_text)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)