###Connection postgresql database
import psycopg2
import datetime
import csv

myConnection = psycopg2.connect(database="testdb",user="sammy",password="test@123",host="xx.xxx.xxx.xxx",port="5432")

print("Database is now connect")

cur = myConnection.cursor()
cur.execute("select * from task natural join time;")
#ver = list(cur.fetchone())

with open("out.csv", "w", newline='') as csv_file:  # Python 3 version
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cur.description]) # write headers
    csv_writer.writerows(cur)

print("Writing complete")