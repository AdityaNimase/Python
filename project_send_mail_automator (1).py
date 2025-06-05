import pandas as pd
import smtplib
import pyodbc
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import schedule
import time

# Define the database connection
conn_str = r"DRIVER={SQL Server};SERVER=DE-TEW-LPT-0109\SQLEXPRESS01;DATABASE=project;Trusted_Connection=yes;"
conn = pyodbc.connect(conn_str)

def send_email(subject, receiver_email, body):
    # Your email credentials
    #sender_email = 
    #password = 
    # Create the email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Establish a connection to the SMTP server
    try:
        with smtplib.SMTP("smtp-mail.outlook.com", 587, timeout=30) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print(f"Email sent successfully to {receiver_email}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def update_sql_table(name):
    cursor = conn.cursor()
    update_query = f"UPDATE discrepancy SET Sent_Mail = 1, Discrepancy_Status = NULL WHERE Name = ?"
    cursor.execute(update_query, name)
    conn.commit()

def send_scheduled_email():
    print("Running scheduled task...")
    # Load the CSV file into a DataFrame
    csv_path = r"C:\Users\91359210_t2\New folder\project mail automator python\output.csv"
    df = pd.read_csv(csv_path)

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        name = row["Name"]
        email = row["email"]
        discrepancy_status = row["Discrepancy_Status"]
        days_since_received = row["Days_since_recieved"]
        sent_mail = row["Sent_Mail"]

        # Add conditions to send email
        if sent_mail == 0 and discrepancy_status == "Discrepancy Raised by Stores" and days_since_received > 5:
            subject = f"Discrepancy Reminder for {name}"
            body = f"Hi {name},\n\nThis is a reminder regarding the discrepancy raised by stores. Please review and take necessary actions.\n\nBest regards,\nL&T"

            # If email sent successfully, update the SQL table
            if send_email(subject, email, body):
                update_sql_table(name)

# Schedule the job to run every day at 10:30 AM
#schedule.every().day.at("11:48").do(send_scheduled_email)

print("Options:\n1. Send Scheduled Email\n Press any key to keep the process going the same way it is")
choice = input("Enter your choice: ")
if choice == "1":
    # Trigger scheduled email manually
    send_scheduled_email()

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
