##Create Git_Lab report for TL
##Install psycopg2 module using pip
import psycopg2
import sys
import smtplib
from datetime import datetime
fromdate = datetime.today().strftime("%m/%d/%y")
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
## Try to connect database
myConnection = psycopg2.connect(dbname="gitlabhq_production",user="gitlab",password="YntN5#fDN6bDEjZuqeg",host="192.168.10.123",port="5432")
print("Opened database successfully")
cur = myConnection.cursor()
cur.execute('''select public."lastweeProjecthrs"."ProjectName","totalhours","lastweek"  from public.projecthours , public."lastweeProjecthrs"
where public."lastweeProjecthrs".id=public.projecthours.id
and public."lastweeProjecthrs".id in
(select project_id  
     from public.users  u, public.project_authorizations pa 
         where  pa.user_id = u.id  and pa.access_level=40 and u.username like 'deven.m')
    ''')
##Fetch the all data from database
data=cur.fetchall()
#emailbody=""
emailbody= '''<h2 style="text-align:center;">Project Summary Report</h2>
 <p style="text-align:center;">Weekly Project Time Spent Report</p>
  </br><table align="center" width="50%" border="1" cellpadding="1" cellspacing="1">'''
emailbody= emailbody + "<tr> <td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>ProjectName</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>TotalHours</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>LastWeekHours</b></td></tr>"
for row in data:
    emailbody = emailbody + "<tr>"
    for x in range(0, 3):
       #    print(row[x])
    #    emailbody += str(row[x])
    #    emailbody += ','
       emailbody = emailbody + "<td style='padding:5px; font-size:14px; background-color:#fff; border:#ccc solid 1px; border-top:0; border-right:0;'>" + str(row[x]) + "</td>"
    
    emailbody = emailbody + "</tr>"
emailbody = emailbody + "</table>"
# send_email(emailbody)    
#print(emailbody)
#f = open('temp.html','w')
#f.write(emailbody)
#f.close()
# email send to 
#body= emailbody
emailbody = emailbody.format(table=tabulate(data, headers="firstrow", tablefmt="html"))
gmail_user = 'intuzsolutions@gmail.com'
gmail_pwd = '2XBaUBXWJOZ4yMfE'
user = 'production.b@intuz.com'
TEXT = "Weekly Report" " " + fromdate
    # Prepare actual message
message = MIMEMultipart(
    "alternative", None, [MIMEText(TEXT), MIMEText(emailbody,'html')])
message['FROM'] = gmail_user
message['TO'] = user
message['SUBJECT'] = TEXT
server = smtplib.SMTP('smtp.gmail.com:587')
server.ehlo()
server.starttls()
server.login(gmail_user, gmail_pwd)
server.sendmail(gmail_user, user, message.as_string())
server.close()
myConnection.close()
print("Connection is now closed")
