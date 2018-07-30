import argparse
import pkg_resources
from pmail.attachment import Attachment
from pmail.recipient import Recipient
from pmail.screen import Screen
from pmail.sender import Sender
from pmail.configuration import Configuration
from pmail.message import Message


# Runs the program
def run(arguments):
    # Configure command-line argument parser
    parser = argparse.ArgumentParser(description="Sends e-mail messages from command line")
    parser.add_argument("details", nargs='*', help="Message details in the following sequence: [recipient] [subject] [body] [attachments] You can specify multiple recipients and multiple attachments using semicolon. Names from address book can be used instead of e-mail addresses. Use \\n to enter line breaks in the body. File paths can be relative, use ~to indicate home folder. ")
    parser.add_argument("-f", "--files", help="Ask for files to attach", action="store_true")
    parser.add_argument("--configure", help="Configure the SMTP server", default=False, action="store_true")
    parser.add_argument("--contacts", help="Edit address book", default=False, action="store_true")
    parser.add_argument("--silent", help="No output is printed in console", default=False, action="store_true")
    parser.add_argument("--test", help="Sends a test message to yourself", default=False, action="store_true")
    parser.add_argument("--version", help="Displays version number of the application", default=False, action="store_true")

    # Parse command-line arguments
    args = parser.parse_args(arguments)
    Screen.silent = args.silent

    # TAKE ACTION:
    # SHOW VERSION NUMBER
    if args.version:
        project = "pmail"
        version = pkg_resources.require(project)[0].version
        print("{} v.{}, (c) Tomasz Waraksa".format(project, version))
        exit()

    # EDIT CONFIGURATION:
    # when configuration if missing or invalid
    # when --configure option was specified
    configuration = Configuration()
    if not configuration.isvalid() or args.configure:
        if configuration.collect() and configuration.isvalid():
            print("Testing configuration ...")
            sender = Sender(configuration)
            result = sender.testmail()
            if result == "ok":
                print("Done. Please check the mailbox of {} to verify.".format(configuration.sender.address))
            else:
                print("The test message could not be sent.")
                print(result)
        exit()

    # EDIT ADDRESS BOOK:
    # when --contacts option was specified
    if args.contacts:
        configuration.editcontacts()
        exit()

    # SEND TEST MESSAGE:
    if args.test:
        print("Testing configuration ...")
        sender = Sender(configuration)
        result = sender.testmail()
        if result == "ok":
            print("Done. Please check the mailbox of {} to verify.".format(configuration.sender.address))
        else:
            print("The test message could not be sent.")
            print(result)
        exit()

    # SEND MESSAGE
    # Use whatever arguments provided in command line, ask the user to enter the rest
    message = Message.fromargs(args.details, configuration)
    if not message.iscomplete():
        Screen.print("Compose the message. Press CTRL+C to stop at any time:")
        Screen.print()
    Screen.print("    From: {}".format(configuration.sender.address))
    if message.recipients:
        Screen.print("    To: {}".format(';'.join(message.recipientaddresses())))
    else:
        recipients = Screen.input("    To: ")
        if recipients:
            message.recipients = Recipient.fromstring(recipients, configuration.contacts, configuration.sender)
        else:
            exit()
    if message.subject:
        Screen.print("    Subject: {}".format(message.subject))
    else:
        message.subject = Screen.input("    Subject: ")
    if message.body:
        Screen.print("    Body: {}".format(message.body))
        if message.attachments:
            Screen.print("    Files: {}".format(','.join(message.attachmentnames())))
    else:
        message.body = Screen.input("    Body: ")
    if args.files and not message.attachments:
        attachments = Screen.input("    Files: ")
        message.attachments = Attachment.fromstring(attachments)
    Screen.print()

    if message.isvalid():
        Screen.print("Sending message to {}...".format(', '.join(message.recipientaddresses())))
        sender = Sender(configuration)
        result = sender.sendmail(message)
        if result == "ok":
            Screen.print("Done.")
        else:
            Screen.print("The message could not be sent.")
            Screen.print(result)
    else:
        Screen.print("Invalid message, cannot send.")
    Screen.print()


