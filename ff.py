"""#from datetime import datetime, timedelta, date
datestring = input("Enter date:")
kk = datestring.split("-")
#print(date(int(kk[0]), int(kk[1]), int(kk[2])))


#print("Today's Date:", date.today())

from datetime import date
#defining the function for subtracting 
def get_difference(startdate, enddate):
    diff = abs(enddate - startdate)
    return diff.days
Date_Today = date.today()
Date_Arrived = date(int(kk[0]), int(kk[1]), int(kk[2]))
days = get_difference(Date_Today, Date_Arrived)
print(f'Difference is {days} days')"""


Sent_Mail = int(input("Enter 0 if mail not sent and 1 if mail is sent:\n"))
if(Sent_Mail == 0 or Sent_Mail == 1):
    Sent_Mail1 = bool(Sent_Mail)
    print(Sent_Mail1)
else:
    print("Invalid input for the column 'Sent_Mail'")
    Sent_Mail1 = None
    print(Sent_Mail1)