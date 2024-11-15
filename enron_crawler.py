import os
import re

def extract_sender_subject_from_emails(directory):
    email_data = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt'):  # Assuming emails are stored as text files
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as email_file:
                    content = email_file.read()
                    sender = re.search(r'From: (.+)', content)
                    subject = re.search(r'Subject: (.+)', content)
                    if sender and subject:
                        email_data.append((sender.group(1).strip(), subject.group(1).strip()))
    return email_data


email_info = extract_sender_subject_from_emails('.\data\raw\maildir')
print(email_info)
