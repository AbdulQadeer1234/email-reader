import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime

def fetch_emails(user, password, unread_only=True):
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(user, password)
    imap.select("inbox")

    search_criteria = "UNSEEN" if unread_only else "ALL"
    status, messages = imap.search(None, search_criteria)

    emails = []
    attachment_paths = []

    for num in messages[0].split():
        _, msg_data = imap.fetch(num, "(RFC822)")
        for response in msg_data:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                subject = decode_header(msg["Subject"])[0][0]
                subject = subject.decode() if isinstance(subject, bytes) else subject
                sender = msg.get("From")
                date_str = msg.get("Date")
                parsed_date = email.utils.parsedate_to_datetime(date_str)
                date = parsed_date.strftime("%Y-%m-%d")
                time = parsed_date.strftime("%H:%M:%S")

                body = ""
                attachments = []
                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        disposition = str(part.get("Content-Disposition"))

                        if "attachment" in disposition:
                            filename = part.get_filename()
                            if filename:
                                folder = "downloads"
                                os.makedirs(folder, exist_ok=True)
                                filepath = os.path.join(folder, filename)
                                with open(filepath, "wb") as f:
                                    f.write(part.get_payload(decode=True))
                                attachments.append(filepath)
                                attachment_paths.append(filepath)
                        elif content_type == "text/plain":
                            body += part.get_payload(decode=True).decode(errors="ignore")
                else:
                    body = msg.get_payload(decode=True).decode(errors="ignore")

                emails.append({
                    "User Name": sender.split("<")[0].strip(),
                    "Mail ID": sender.split("<")[-1].replace(">", ""),
                    "Date": date,
                    "Time": time,
                    "Subject": subject,
                    "Body": body,
                    "Attachments": ", ".join(os.path.basename(a) for a in attachments)
                })

    imap.logout()
    return emails, attachment_paths
