import bs4 as bs
import requests
import datetime
import os
import smtplib
import hashlib

source = requests.get("https://secure.kentucky.gov/booking.web/Event/Book/209")
soup = bs.BeautifulSoup(source.content, 'lxml')
days=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
spotsAvailable = 0
numofdays = 0
numoftimeslots = 0

#Count for List of List
for medias in (soup.find_all(class_="media")):
        for potentialdays in (medias.find_all(class_="media-left")):
                datetime_object = ((potentialdays.find("time", class_="icon")["datetime"]).split(" ")[0])
                downum = datetime.datetime.strptime(datetime_object, '%m/%d/%Y').weekday()
                dayofweek = (days[downum])
                numofdays += 1
                tempnumoftimeslots = 0
        for potentialtimes in (medias.find_all(class_="row")):
                for individualTimes in (potentialtimes.find_all(class_="instanceSelector")):
                        spotsAvailable = (individualTimes["data-capacity"])
                        tempnumoftimeslots += 1
                        if tempnumoftimeslots > numoftimeslots:
                                numoftimeslots = tempnumoftimeslots

#Create multidimentional List
ListOfTimeslots = [[0 for y in range(5)] for y in range(numoftimeslots * numofdays)]

DayCounter = 0
TimeslotCounter = 0

for medias in (soup.find_all(class_="media")):
        for potentialdays in (medias.find_all(class_="media-left")):
                datetime_object = ((potentialdays.find("time", class_="icon")["datetime"]).split(" ")[0])
                downum = datetime.datetime.strptime(datetime_object, '%m/%d/%Y').weekday()
                dayofweek = (days[downum])
        for potentialtimes in (medias.find_all(class_="row")):
                for individualTimes in (potentialtimes.find_all(class_="instanceSelector")):
                        spotsAvailable = (individualTimes["data-capacity"])
                        timeslotvalue = individualTimes.text
                        ListOfTimeslots[TimeslotCounter][0] = dayofweek
                        ListOfTimeslots[TimeslotCounter][1] = datetime_object #mm/dd/yyyy
                        ListOfTimeslots[TimeslotCounter][2] = timeslotvalue
                        ListOfTimeslots[TimeslotCounter][3] = spotsAvailable
                        if (((dayofweek == "Monday") or (dayofweek == "Friday")) and (datetime_object != "09/28/2020")):
                                ListOfTimeslots[TimeslotCounter][4] = "Good"
                        else:
                                ListOfTimeslots[TimeslotCounter][4] = " "
                        TimeslotCounter += 1
        DayCounter += 1

if os.path.exists("/home/dgarrison/DrivingTest/Jess-Permit-temp.txt"):
        os.remove("/home/dgarrison/DrivingTest/Jess-Permit-temp.txt")
f = open("/home/dgarrison/DrivingTest/Jess-Permit-temp.txt","a")
f.write("\n\n")
f.write("Jessamine County - Permit Registrations Available!!! \n")
f.write("\n")
f.write("URL to register: https://secure.kentucky.gov/booking.web/Event/Book/209 \n")
f.write("\n")
f.write("Total number of days visible on the website: "+ str(numofdays))
f.write("\n\n")

f.write("DATE\t\tDAY\t\tTIMESLOT\tSEATS AVAIL\n")
f.write("-------------------------------------------------------------\n")

AreSpotsAvailable = "No"

for i in range(numoftimeslots * numofdays):
        if ((ListOfTimeslots[i][4] == "Good") and ((ListOfTimeslots[i][3] == "1") or (ListOfTimeslots[i][3] == "2"))):
                TableOfGoodTimeslots = (ListOfTimeslots[i][1] + "\t" + ListOfTimeslots[i][0] + "\t" + ListOfTimeslots[i][2] + "\t" + ListOfTimeslots[i][3] + "\n")
                f.write(TableOfGoodTimeslots)
                AreSpotsAvailable = "Yes"
f.close()

EmailEnabled = "No"

Recipients = ["DestEmail1@test.com", "DestEmail2@test.com"]

if AreSpotsAvailable == "Yes" and EmailEnabled == "Yes":
        for dest in Recipients:
                f = open("~/DrivingTest/Jess-Permit-temp.txt","r")
                message = f.read()
                print ("Spots available")
                #email
                s = smtplib.SMTP('smtp.gmail.com', 587)
                s.starttls()
                s.login("SendingEmailAccount@TEST.COM", "SENDINGAPIPASSWORD")
                s.sendmail("SendingEmailAccount@TEST.COM", dest, message)
                s.quit()

print (str(datetime.datetime.now())+ "\tAvailable spots?: " + AreSpotsAvailable + "\tEmail Enabled?: " + EmailEnabled)


f.close()
g = open("~/DrivingTest/log.txt","a")
g.write("Jessamine Co Permit - Run at: "+ str(datetime.datetime.now()) + "     - Any Spots Available?: " + AreSpotsAvailable + "\n")
g.close()
#print ("Total Number of Days visible on Website: "+ str(numofdays))
