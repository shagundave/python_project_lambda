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
curOuter = myConnection.cursor()
curInner = myConnection.cursor()
curInner.execute(''' SELECT 
public.users.username,
TO_CHAR(
        sum(public.timelogs.time_spent) * '1 second'::interval,
        'HH24:MI:SS'
    ) As "TotalHours"
FROM
public.users, public.issues, public.timelogs WHERE public.users.id = public.timelogs.user_id
and public.timelogs.trackable_id  = public.issues.ID
and public.issues.project_id in
(select project_id  
     from public.users  u, public.project_authorizations pa 
         where  pa.user_id = u.id and pa.access_level=40  and u.username like 'nirav.s')
and public.timelogs.created_at >=  now() - interval '1 day'
group by public.users.username
order by public.users.username 
    ''')
user_name=curInner.fetchall()
if len(user_name) > 0:
    print('data fetch')
    emailbody = '''<h2 style="text-align:center;">Daily Report</h2>
    <p style="text-align:center;"> Employee Daily worked hours Report </p>
    </br><table align="center" width="50%" border="1" cellpadding="1" cellspacing="1">'''
    emailbody = emailbody + "<tr> <td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Username</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Work Hours</b></td></tr>"
    for row_u in user_name:
        emailbody = emailbody + "<tr>"
        for y in range(0, 2):
        #    print(row[x])
        #    emailbody += str(row[x])
        #    emailbody += ','
            emailbody = emailbody + "<td style='padding:5px; font-size:14px; background-color:#fff; border:#ccc solid 1px; border-top:0; border-right:0;'>" + str(row_u[y]) + "</td>"
        
        emailbody = emailbody + "</tr>"
    emailbody = emailbody + "</table>"
    emailbody += "<br><br>"
curOuter.execute('''SELECT 
public.users.username,
public.projects.name as ProjectName,
public.issues.title as Task,
TO_CHAR(
        max(public.issues.time_estimate) * '1 second'::interval,
        'HH24:MI:SS'
    ) As TimeEtimate,
TO_CHAR(
        sum(public.timelogs.time_spent) * '1 second'::interval,
        'HH24:MI:SS'
    ) As WorkHours, 
public.issues.description, 
public.issues.state, 
public.issues.due_date   
FROM 
public.timelogs, public.issues, public.users ,public.projects
WHERE  public.timelogs.trackable_id  = public.issues.ID and public.projects.id =  public.issues.project_id
and public.users.id = public.timelogs.user_id
and public.issues.project_id in
(select project_id  
    from public.users  u, public.project_authorizations pa 
        where  pa.user_id = u.id and pa.access_level=40  and u.username like 'nirav.s')
and public.timelogs.created_at >=  now() - interval '1 day'
group by public.users.username, public.projects.name, public.issues.title, public.issues.description, public.issues.state, public.issues.due_date
Order by public.users.username
    ''')
data=curOuter.fetchall()
if len(data)> 0:
    print("data fetch")
    
    ##Fetch the all data from database
    #emailbody=""
    emailbody+= '''
    <p style="text-align:center;">Employee Daily Task Report </p>
    </br><table width="100%" border="1" cellpadding="1" cellspacing="1">'''
    emailbody= emailbody + "<tr> <td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Username</b></td><td style='text-align:center; background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Project Name</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Task</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Estimate Time</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Work Hours</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Description</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>State</b></td><td style='background-color:#f7f7f7; padding:5px; font-size:15px; border:#ccc solid 1px;'><b>Due Date</b></td></tr>"
    for row in data:
        emailbody = emailbody + "<tr>"
        for x in range(0, 8):
        #    print(row[x])
        #    emailbody += str(row[x])
        #    emailbody += ','
            emailbody = emailbody + "<td style='padding:5px; font-size:14px; background-color:#fff; border:#ccc solid 1px; border-top:0; border-right:0;'>" + str(row[x]) + "</td>"
        
        emailbody = emailbody + "</tr>"
    emailbody = emailbody + "</table>"
    # email send to 
    #body= emailbody
    emailbody = emailbody.format(table=tabulate(user_name, headers="firstrow", tablefmt="html"))
    emailbody = emailbody.format(table=tabulate(data, headers="firstrow", tablefmt="html"))
    gmail_user = 'intuzsolutions@gmail.com'
    gmail_pwd = '2XBaUBXWJOZ4yMfE'
    user = 'production.g@intuz.com'
    TEXT = "Daily Report" " " + fromdate
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
