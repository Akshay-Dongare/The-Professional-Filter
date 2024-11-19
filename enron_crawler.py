import os
import csv

def extract_sent_items_to_csv(dataset_path, output_csv):
    # temp list to store email data
    email_data = []

    # folders to ignore
    folders = []
    counter = 0

    # Traverse the dataset directory
    for root, dirs, files in os.walk(dataset_path):
        # Check if the current directory is to be ignored
        if os.path.basename(root).lower() not in folders:
            print(f"Accessing folder: /{root.split(os.sep)[-2]}/{os.path.basename(root).lower()}")

            # Process each file in the sent_items folder
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        email_content = f.read()
                        # Append to email_data (e.g., folder owner and content)
                        email_data.append([root.split(os.sep)[-2], email_content])
                        counter += 1
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
        
    print(f"Total number of emails: {counter}")

    # Write the collected email data to a CSV file
    with open(output_csv, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write the header
        writer.writerow(['Employee', 'message'])
        # Write the email data
        writer.writerows(email_data)

    print(f"Data successfully written to {output_csv}")

# source paths
dataset_path = "data/raw/maildir/"
output_csv = "data/crawled/emails.csv"

extract_sent_items_to_csv(dataset_path, output_csv)
