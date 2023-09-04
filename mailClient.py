############################################################
# Author:       Aravind Potluri <aravindswami135@gmail.com>
# Description:  Python based Simple Mail Transfer Protocol,
#               mail client.
############################################################

# Libraries
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Email configuration
smtpServer = 'mmtp.iitk.ac.in' # IITK's Server
smtpPort = 25  # Default SMTP port
# smtpServer = '127.0.0.1' # Testing server
# smtpPort = 25  # Testing SMTP port

def genrateMIME(sMail, rMail, cc, bcc, sub, body):
    """Generate MIME message"""
    mimeMsg = MIMEMultipart()
    mimeMsg['From'] = sMail
    mimeMsg['To'] = rMail
    mimeMsg['Cc'] = cc
    mimeMsg['Bcc'] = bcc
    mimeMsg['Subject'] = sub
    mimeMsg.attach(MIMEText(body, 'plain'))
    return mimeMsg

# Connect to the SMTP server
try:
    # """Login details"""
    server = smtplib.SMTP(smtpServer, smtpPort)
    server.starttls()  # Use TLS encryption if supported
    while True:
        try:
            print("################## IITK Mail Client ########################")
            senderMail = input("[#] IITK Mail ID: ")
            senderPasswd = input("[#] Password: ")
            server.login(senderMail, senderPasswd)
            break
        except:
            os.system('clear')
            print("[!] Wrong Creds, Try again !\n\n")
except Exception as err:
    print(f"[!] {err}")
    exit()
finally:
    # """Get recipient's details"""
    recipientMail = input("[#] Recipient Mail ID: ")
    ccMail = input("[#] cc Mail (if any): ")
    bccMail = input("[#] bcc Mail (if any): ")

    # """Get contents of mail"""
    subject = input("\n[#] Subject: ")
    body = input("\n[#] Body: ")
    msg = genrateMIME(senderMail, recipientMail, ccMail, bccMail, subject, body)
    while True:
        attachmentPath = input("\n[#] Path to Attachment (if any): ")
        if attachmentPath != "":
            try:
                with open(attachmentPath, 'rb') as attachmentFile:
                    attachment = MIMEApplication(attachmentFile.read())
                    attachment['Content-Disposition'] = f'attachment; filename="{attachmentPath}"'
                    msg.attach(attachment)
                    break
            except FileNotFoundError:
                print("[!] File not found\n")
        else:
            break
    server.sendmail(senderMail, [recipientMail, ccMail, bccMail], msg.as_string())
    server.quit()
