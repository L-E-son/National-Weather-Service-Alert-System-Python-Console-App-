import feedparser, datetime, os, time, math, cgitb
from datetime import date, timedelta, datetime

cgitb.enable()

while True:
    print("Content-Type: text/html") 
    print()   
    os.system("cls")
    requests = feedparser.parse("http://alerts.weather.gov/cap/wwaatmget.php?x=GAC067&y=0") #ATOM feed for Cobb County
    plusHour = timedelta(minutes = 60)
    currentTime = datetime.today()
    future45 = datetime(currentTime.year,currentTime.month,currentTime.day,currentTime.hour,45)
    waitTime = future45 - currentTime

    if waitTime.total_seconds() < 0: #error handling. the calculation to change the time results in the current hour as XX:45, so if the time is past XX:45 and before XX:00, then there will need to be an exception
        waitinSeconds = waitTime.total_seconds() + plusHour.total_seconds()
    else:
        waitinSeconds = waitTime.total_seconds()

    if requests.entries[0].title == "There are no active watches, warnings or advisories":
        print("Entries: 0")
    else:
        print("Entries: " + str(len(requests.entries)))

    print("")
    for entry in requests.entries:
        #print(entry)
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
            #print("Current Time: " + str(datetime.now()))
            #print("Time Since Published: " + entry.published - datetime.datetime.now)
        except AttributeError:
            #print("AttributeError")
            break
        print("--------------------")
    print("End of reports.")
    #print("Waiting until " + str(future45)) #not future45, needs updated logic // add waitinSeconds/60 to currentTime
    #print("Debug: " + str(round(waitinSeconds,0)) + " seconds // (Minutes: " + str(round(waitinSeconds/60,0)) + ")")
    time.sleep(waitinSeconds)