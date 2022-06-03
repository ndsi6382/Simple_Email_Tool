#!/usr/bin/env python3
import os, sys, argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
import markdown2
import config

class Email:
    Username = config.Username
    Password = config.Password
    Name = config.Name
    SMTPServerAddress = config.SMTPServerAddress

    def __init__(self, to, subject, body, cc=[], bcc=[], md=False):
        self.msg = MIMEMultipart()
        self.msg['From'] = f"{Email.Name} <{Email.Username}>"
        self.msg['To'] = ', '.join(to)
        self.msg['Cc'] = ', '.join(cc)
        self.msg['Subject'] = subject
        self.bcc = ", ".join(bcc)
        self.body = body if not md else f"  <{body}>"
        if md:
            with open(body, 'r') as file:
                html = markdown2.markdown(file.read())
                self.msg.attach(MIMEText(html, 'html'))
        else:
            self.msg.attach(MIMEText(self.body, 'plain'))
        self.attachments = []
    
    def attach(self, filename):
        with open(filename, 'rb') as file:
            self.msg.attach(MIMEApplication(file.read(), Name=os.path.basename(filename)))
        self.attachments.append(filename)
    
    def __str__(self):
        return  (f"To: {self.msg['To']}\n" + 
                 f"Cc: {self.msg['Cc']}\n" + 
                 f"Bcc: {self.bcc}\n" + 
                 f"Subject: {self.msg['Subject']}\n" + 
                 f"Attachments: {self.attachments}\n" +
                 f"Body:\n------------\n{self.body}\n------------")

    def send(self):
        if self.bcc: allRecipients = f"{self.msg['To']}, {self.bcc}"
        else: allRecipients = self.msg['To']
        try:
            server = smtplib.SMTP(Email.SMTPServerAddress, 587)
            server.ehlo()
            server.starttls()
            server.login(Email.Username, Email.Password)
            server.sendmail(self.msg['From'], allRecipients, self.msg.as_string())
            server.close()
        except:
            print("An error occured. The email was not sent successfully.")
            print("Exiting...")
            sys.exit(1)

def main():
    print("Simple Email Tool\n")
    # Parse Arguments
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-to', type=str, nargs='+', metavar='ADDRESS', help='Recipient addresses')
    argparser.add_argument('-cc', type=str, nargs='+', metavar='ADDRESS', help='Cc addresses')
    argparser.add_argument('-bcc', type=str, nargs='+', metavar='ADDRESS',help='Bcc addresses')
    argparser.add_argument('-s', '--subject', type=str, nargs=1, help='Subject text')
    bodygroup = argparser.add_mutually_exclusive_group()
    bodygroup.add_argument('-b', '--body', type=str, nargs=1, help='Body (as plaintext - suitable for quick/short messages)')
    bodygroup.add_argument('-bt', '--bodytextfile', type=str, nargs=1, metavar='FILE',help='Write email body from a text file')
    bodygroup.add_argument('-bm', '--bodymarkdown', type=str, nargs=1, metavar='FILE',help='Write email body from a markdown file')
    argparser.add_argument('-a', '--attachments', type=str, nargs='+', metavar='FILE',help='Attachment filenames/paths')
    argparser.add_argument('-y', '--yes', action='store_true', help='Skip the confirmation prompt')
    args = argparser.parse_args()
    # Ensure Configurations
    if not Email.Username: Email.Username = input("Email Username/Address: ")
    if not Email.Password:
        try: Email.Password = os.environ['EMAILPASS']
        except KeyError: Email.Password = input("Email Password: ")
    if not Email.SMTPServerAddress: Email.SMTPServerAddress = input("SMTP Server Address: ")
        
    if not args.to:
        # Create Email from Prompts
        e = prompt()
    else:
        # Create Email from Arguments
        to = args.to
        cc = args.cc if args.cc else []
        bcc = args.bcc if args.bcc else []
        subject = args.subject[0] if args.subject else ""
        body = ""
        md = False
        if args.body:
            body = args.body[0]
        elif args.bodytextfile:
            with open(args.bodytextfile[0], 'r') as file:
                body = file.read()
        elif args.bodymarkdown:
            body = args.bodymarkdown[0]
            md = True
        e = Email(to, subject, body, cc=cc, bcc=bcc, md=md)
        if args.attachments:
            for a in args.attachments:
                e.attach(a)
    # Confirmation
    print(f"From: {e.msg['From']}")
    print(e, '\n')
    if not args.yes:
        proceed = input("Proceed? [Yy/Nn]: ")
        if 'y' not in proceed.lower():
            print("Exiting...")
            sys.exit()
    # Send / Exit
    print("Sending... ")
    e.send()
    print("Sent!")
    print("Thank you for using Simple Email Tool!")

def prompt():
    print("Creating email by prompt. ", end="") 
    print("If you did not intend to do this, provide arguments at the command line, ", end="")
    print("see README.md, or give '-h' to see the help.\n")
    print("To include multiple addresses/paths/filenames, separate by a space.")
    print("To ignore any fields (other than 'To:'), press Enter to move to the next prompt.\n")
    to = []
    while True:
        to = input("To: ").split()
        if to: break
    cc = input("Cc: ").split()
    bcc = input("Bcc: ").split()
    subject = input("Subject: ")
    body = input("Body: ")
    attachments = input("Attachment(s): ").split()
    e = Email(to, subject, body, cc=cc, bcc=bcc)
    if attachments:
        for a in attachments:
            e.attach(a)
    print(f"====================\n")
    return e

if __name__ == "__main__":
    main()
