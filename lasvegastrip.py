from calendar import Calendar
import subprocess 


class Expedia(object):

    def __init__(self):
        self.url_begin = ("\"https://www.expedia.ca/Flights-Search?"
        "trip=oneway&leg1=from:YYZ,to:LAS,departure:")
        self.url_ending = ("TANYT&passengers=children:0,adults:1,seniors:0,"  
        "infantinlap:Y&options=maxhops%3A0&mode=search\"")

    def __str__(self):
        return "Expedia"

    @staticmethod 
    def date_fmt(a_date):
        return a_date.strftime("%d/%m/%y")       
    
    def get_url_date(self, a_date):
        date_fmt = self.date_fmt(a_date)
        return self.url_begin + date_fmt + self.url_ending
    
class SelectionDay(object):

    def __init__(self):
        self.begin_day = 1
        self.year = 2016
        self.month = 9
        c = Calendar(firstweekday=self.begin_day)
        self.cal = c.monthdatescalendar(self.year, self.month)
        
        thursday = 4 - self.begin_day
        friday = 5 - self.begin_day
        sunday = 6 - self.begin_day 
        monday = 1 - self.begin_day
        self.weekday_select = [thursday, friday]
    
    def get_no_weeks(self):
        return len(self.cal) 
        
    def get_dates(self, no_week):
        lst = []
        for weekday in self.weekday_select:
            lst.append(self.cal[no_week][weekday])
        return lst
         
class Command(object):
    def __init__(self):
        self.command = "" 
        self.phantom_command = ""
        self.montage_command = ""
        self.website = None
    
    def create_phantom(self, date):
        url = self.website.get_url_date(date)
        self.phantom_command += " <(phantomjs getimage.js {})".format(url)
        
    def create_montage(self, days):
        self.montage_command += " <(montage{} " \
            "-tile {}x1 -geometry +0+0)".format(self.phantom_command, days)

    def convert_pdf(self):
        self.command = "convert{} some.pdf".format(self.montage_command)

    def create_no_montage(self):
        self.montage_command = self.phantom_command
    
    def execute(self):
        subprocess.call(self.command, shell=True, executable="/bin/bash")

if __name__ == "__main__":
    selection = SelectionDay()
    weeks = selection.get_no_weeks() 
    com = Command()
    websites = [Expedia()]
    for week in range(weeks):
        for website in websites:
            com.website = website
            days = selection.get_dates(week) 

            for date in days:
                com.create_phantom(date) 

            if len(days) > 1:
                com.create_montage(len(days))
            else:
                com.create_no_montage()
            
    com.convert_pdf()
    com.execute()

