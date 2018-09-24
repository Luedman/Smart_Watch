from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import calendar

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'


def Google_update():

    now = (datetime.datetime.utcnow() + datetime.timedelta(hours = 2)).isoformat("T") + "Z"
    end_of_period = (datetime.datetime.utcnow() + datetime.timedelta(hours = 12)).isoformat("T") + "Z"

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('calendar', 'v3', http=creds.authorize(Http()))

    # Get the API data
    events_result = service.events().list(calendarId='primary',
                                            timeMax = end_of_period,
                                            timeMin = now,
                                            singleEvents=True,
                                            orderBy='startTime').execute()

    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')

    # Initialize the list
    next_hours_blocked = [False]*12
    screen_output = []

    for event in events:
        start_date = event['start'].get('dateTime', event['start'].get('date'))
        end_date = event['end'].get('dateTime', event['end'].get('date'))

        start_datetime = datetime.datetime.strptime(start_date[0:-6], "%Y-%m-%dT%H:%M:%S")
        end_datetime = datetime.datetime.strptime(start_date[0:-6], "%Y-%m-%dT%H:%M:%S")

        now_hour = int(now[11:13]) % 12
        start_hour = int(start_date[11:13]) % 12
        end_hour = int(end_date[11:13]) % 12


        for i in range(start_hour, end_hour ):
            next_hours_blocked[i] = True


        output = (str(calendar.day_name[start_datetime.weekday()]) + "  " +
                        str(start_date[11:16]) + "  " +
                        str(event['summary']))

        screen_output.append(output)

    return next_hours_blocked, screen_output




# Standard-library imports
import time       # utilities to measure time
import gpiozero   # hardware abstraction of RaspberryPi's GPIOs and common connected periphera


class Watsch:

    def __init__(self):

        self._keep_running = True   # signals the main loop to keep running
        self._setup_hardware()

    def _setup_hardware(self):

        self._zero_a_un = gpiozero.LED(2)
        self._un_a_deux = gpiozero.LED(3)
        self._deux_a_trois = gpiozero.LED(4)
        self._trois_a_quatre = gpiozero.LED(5)
        self._quatre_a_cinq = gpiozero.LED(6)
        self._cinq_a_six = gpiozero.LED(13)
        self._six_a_sept = gpiozero.LED(14)
        self._sept_a_huit = gpiozero.LED(15)
        self._huit_a_neuf = gpiozero.LED(18)
        self._neuf_a_dix = gpiozero.LED(16)
        self._dix_a_onze = gpiozero.LED(20)
        self._onze_a_douze = gpiozero.LED(21)

    #def Google_update():
        #print("Google Calendar Update")
        #a_time = "12:00 - 14:00"
        #a_description = "Babysitting"
        #a_clock = [False,False,True, True, False, False, True, False, True, True, False, False]
        #return a_clock, a_time, a_description


    def run(self):
        print("Entered main loop")
        last_run = time.monotonic()
        while self._keep_running:
            # make this loop run once every 0.25 s
            now = time.monotonic()
            next_run = last_run + 2.0
            wait = max(0, next_run - now)
            time.sleep(wait)
            last_run = now + wait

            # Update Google
            a_clock, screen_output = Google_update()
            print(a_clock)

            # Turn on LEDs
            if a_clock[0] == True:
                self._zero_a_un.on()
            else:
                self._zero_a_un.off()

            if a_clock[1] == True:
                self._un_a_deux.on()
            else:
                self._un_a_deux_.off()

            if a_clock[2] == True:
                self._deux_a_trois.on()
            else:
                self._deux_a_trois.off()

            if a_clock[3] == True:
                self._trois_a_quatre.on()
            else:
                self._trois_a_quatre.off()

            if a_clock[4] == True:
                self._quatre_a_cinq.on()
            else:
                self._quatre_a_cinq.off()

            if a_clock[5] == True:
                self._cinq_a_six.on()
            else:
                self._cinq_a_six.off()

            if a_clock[6] == True:
                self._six_a_sept.on()
            else:
                self._six_a_sept.off()

            if a_clock[7] == True:
                self._sept_a_huit.on()
            else:
                self._sept_a_huit.off()

            if a_clock[8] == True:
                self._huit_a_neuf.on()
            else:
                self._huit_a_neuf.off()

            if a_clock[9] == True:
                self._neuf_a_dix.on()
            else:
                self._neuf_a_dix.off()

            if a_clock[10] == True:
                self._dix_a_onze.on()
            else:
                self._dix_a_onze.off()

            if a_clock[11] == True:
                self._onze_a_douze.on()
            else:
                self._onze_a_douze.off()

        print("Leaving main loop")

# Main entry point
if __name__ == "__main__":

    watsch = Watsch()
    watsch.run()