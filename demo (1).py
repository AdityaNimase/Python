import pyodbc
import csv
from datetime import datetime, timedelta, date

def read(conn, output_csv):
    print("Read")
    cursor = conn.cursor()

    # Fetch the column names
    cursor.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'discrepancy'")
    columns = [column[0] for column in cursor.fetchall()]

    # Fetch and print the data
    cursor.execute("SELECT * FROM discrepancy")
    rows = cursor.fetchall()

    # Print column names
    print(" | ".join(columns))

    # Print rows
    for row in rows:
        print(" | ".join(map(str, row)))

    print()

    with open(output_csv, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        # Write column names
        csv_writer.writerow(columns)

        # Write rows
        csv_writer.writerows(rows)

    print(f"Data written to {output_csv}")

# Specify the CSV file path
output_csv_path = r"C:\Users\91359210_t2\New folder\project mail automator python\output.csv"

def create(conn):
    print("Create")
    cursor = conn.cursor()
    Name = input("Enter Name of the client(buyer):")
    Name1 = f"'{Name}'"
    email = input("Enter E-mail id of the client(buyer):")
    email1 = f"'{email}'"
    dd = input("Enter Discrepancy Status of the Product:\nEnter 1 for'Discrepancy Raised by Stores' and any other key for NULL")
    if(dd == "1"):
        Discrepancy_Status = input("Enter Discrepancy Status of the Product:")
    else:
        Discrepancy_Status = None

    Discrepancy_Status1 = f"'{Discrepancy_Status}'"
    datestring = input("Enter date:")
    datedata = datestring.split("-")
    Date_Arrived = date(int(datedata[0]), int(datedata[1]), int(datedata[2]))
    Date_Arrived1 = f"'{Date_Arrived}'"
    Days_since_recieved = (date.today() - Date_Arrived).days
    Sent_Mail = int(input("Enter 0 if mail not sent and 1 if mail is sent:\n"))
    if(Sent_Mail == 0 or Sent_Mail == 1):
        Sent_Mail1 = Sent_Mail
    else:
        print("Invalid input for the column 'Sent_Mail'")
        Sent_Mail1 = None

    cursor = conn.cursor()
    cursor.execute(
        f'INSERT INTO discrepancy(Name, email, Discrepancy_Status, Date_Arrived, Days_since_recieved, Sent_Mail) VALUES ({Name1}, {email1}, {Discrepancy_Status1}, {Date_Arrived1}, {Days_since_recieved}, {Sent_Mail1});'
    )
    
    conn.commit()
    read(conn, output_csv_path)


def update(conn):
    print("Update")
    column_name = input("Enter the column name to be updated:")
    condition_col = input("Enter the column for the condition(for identifying the row):")
    condition_val = input("Enter the column value for the condition(for identifying the row):")
    condition_val1= f"'{condition_val}'"
    print("Enter the datatype of the data to be updated")
    updtype = int(input("The following are the options to access the datatype needed to be accessed:\n1.Integer\n2.String\n3.Date\n"))
    if(updtype == 1):
        updata = int(input("Enter the integer data to be updated:"))
        updata1 = f"'{updata}'"
    elif(updtype == 2):
        updata = input("Enter the string data to be updated:")
        updata1 = f"'{updata}'"
    elif(updtype == 3):
        print("Enter the date data to be updated:\nEnter year, then press enter, then month, then enter again, then day, then press enter\nFormat for date: YYYY-MM-DD")
        datestring = input("Enter the date in the above mentioned format")
        datedata = datestring.split("-")
        updata = date(int(datedata[0]), int(datedata[1]), int(datedata[2])) #datedata[0] = year datedata[1] = month datedata[2] = day
        updata1 = f"'{updata}'"
    else:
        print("Invalid input for updation of the record")

    cursor = conn.cursor()
    cursor.execute(
        f'update discrepancy set {column_name} = {updata1} where {condition_col} = {condition_val1};',
    )
    conn.commit()
    read(conn, output_csv_path)


def delete(conn):
    print("Delete")
    condition_col = input("Enter the column for the condition(for identifying the row):")
    n = int(input("Is the datatype of the column used integer??\nIf the datatype is integer Press 1:\n"))
    if(n==1):
        condition_val = int(input("Enter the column value for the condition(for identifying the row):"))
        condition_val1 = condition_val
    else:
        condition_val = input("Enter the column value for the condition(for identifying the row):")
        condition_val1 = f"'{condition_val}'"
    cursor = conn.cursor()
    cursor.execute(
        f'delete from discrepancy where {condition_col} = {condition_val1};'
    )
    conn.commit()
    read(conn, output_csv_path)


conn = pyodbc.connect(
    "DRIVER={SQL Server};"
    r"SERVER=DE-TEW-LPT-0109\SQLEXPRESS01;"
    "DATABASE=project;"
    "Trusted_Connection=yes;"
)
read(conn, output_csv_path)

k=0
while (k==0):
    print("Operation needed to be performed:\n1. Create(Insert Into)\n2.Update \n3.Delete \n")
    p = int(input("Enter your choice:"))

    if(p==1):
        create(conn)

    elif(p==2):
        update(conn)

    elif(p==3):
        delete(conn)

    else:
        print("Invalid Input!")

    print("Do you want to continue??")
    l = int(input("Press 0 to continue"))
    if(l != 0):
        k=k+1
        print("Process Terminated!")

conn.close()