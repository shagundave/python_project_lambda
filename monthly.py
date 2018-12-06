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
cur.execute('''SELECT
public.projects.name As "Project Name",
TO_CHAR(
        sum(public.timelogs.time_spent) * '1 second'::interval,
        'HH24:MI:SS'
    ) As "TotalHours"
FROM 
public.timelogs, public.issues, public.users ,public.projects WHERE public.timelogs.trackable_id = public.issues.ID and public.projects.id =  public.issues.project_id
and public.users.id = public.timelogs.user_id 
and public.issues.project_id in
(select project_id  
     from public.users  u, public.project_authorizations pa 
         where  pa.user_id = u.id and pa.access_level=40 and u.username like 'nilay.d')
and public.timelogs.created_at >=  now() 
group by public.projects.name
order by sum(public.timelogs.time_spent * '1 second'::interval) desc
    ''')
##Fetch the all data from database
data=cur.fetchall()
#emailbody=""
emailbody= '''<h2 style="text-align:center;">Monthly Report</h2>
 <p style="text-align:center;">Employee Monthly Total Time Spent Report</p>
  </br><table border='1'>'''
emailbody= emailbody + "<tr> <td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Name</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Total Time Spent</b></td></tr>"
for row in data:
    emailbody = emailbody + "<tr>"
    for x in range(0, 2):
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
user = 'production.c@intuz.com'
TEXT = "Monthly Report "  + fromdate +  ' -nilay.d'
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
