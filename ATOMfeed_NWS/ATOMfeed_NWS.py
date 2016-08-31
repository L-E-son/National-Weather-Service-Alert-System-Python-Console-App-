'''
Made by John Ellison
for personal use as well for the use of anyone who can benefit from it
February 2015
'''

import feedparser, datetime, os, time, math
from datetime import date, timedelta, datetime

#HEAD NOTE: the NWS ATOM feed specifies that the feed will update every hour after 45 minutes (XX:45), so it will execute when it is run and again at the next 45th minute on the hour

while True:
    print("Content-Type: text/html") 
    print()   
    os.system("cls")
    requests = feedparser.parse("http://alerts.weather.gov/cap/wwaatmget.php?x=GAC067&y=0") #ATOM feed for Cobb County this can be any NWS ATOM feed
    plusHour = timedelta(minutes = 60)
    currentTime = datetime.today()
    future45 = datetime(currentTime.year,currentTime.month,currentTime.day,currentTime.hour,45)
    waitTime = future45 - currentTime

    if waitTime.total_seconds() < 0: #exception handling. the calculation to change the time results in the current hour as XX:45, so if the time is past XX:45 and before XX:00, then there will need to be an exception. this conditional st atement prevents that
        waitinSeconds = waitTime.total_seconds() + plusHour.total_seconds() #add an hour if the above statement is true
    else:
        waitinSeconds = waitTime.total_seconds()

    if requests.entries[0].title == "There are no active watches, warnings or advisories": #if there are no entries, print 0
        print("Entries: 0")
    else:
        print("Entries: " + str(len(requests.entries))) #print number of entries

    print("")
    for entry in requests.entries:
        print(entry.title)
        try:
            print("Severity: " + entry.cap_severity)
            print("Type: " + entry.cap_msgtype)
            print("Last Updated: " + entry.updated)
            print("Effective: " + entry.cap_effective)
            print("Current Time: " + str(datetime.now()))
            print("")
            print(entry.summary)
            print("")
            print("Urgency: " + entry.cap_urgency)
            print("Certainty: " + entry.cap_certainty)
            print(entry.cap_areadesc)
            print("Published: " + entry.published)
            #print("Time Since Published: " + entry.published - datetime.datetime.now) #feature to calculate time since last update
        except AttributeError: #if there are no entries
            break
        print("--------------------")
    print("End of reports.")
    #print("Waiting until " + str(future45)) #not future45, needs updated logic // add waitinSeconds/60 to currentTime #previous feature to show the user how the update system works
    #print("Debug: " + str(round(waitinSeconds,0)) + " seconds // (Minutes: " + str(round(waitinSeconds/60,0)) + ")")
    time.sleep(waitinSeconds)
