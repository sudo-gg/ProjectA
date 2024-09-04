import tkinter as tk
import tkcalendar as tkcal
from tkinter import messagebox
import datetime
import sqlite3
import os


def dateSelected(cal, periodNum, room, username):
    db = sqlite3.connect("User_Data.db")
    c = db.cursor()
    selectedDate = str(cal.get_date())
    # little y = no century / big Y = century included
    selectedDatetime = datetime.datetime.strptime(selectedDate, "%m/%d/%y")
    daysElapsed = selectedDatetime.day - 1
    # Turn to english format
    selectedDateStr = selectedDatetime.strftime("%Y/%m/%d")
    periodId = daysElapsed * 5 + periodNum
    if selectedDate:  # Presence check
        if messagebox.askokcancel("Confirmation", f"Book room {room}, Period {periodNum} at {selectedDateStr}?"):
            try:
                c.execute(f"UPDATE Teacher_Bookings_{room} SET Username = (?) WHERE PeriodID = {periodId}", (username,))
                # Disable the button if successful
                # Uses the .get_date to get a string and converts it to a datetime object but just the date using .date()
                dateToDisable = datetime.datetime.strptime(cal.get_date(), "%m/%d/%y").date()
                i, j = cal._get_day_coords(dateToDisable)
                cal._calendar[i][j].state(['disabled'])
            except sqlite3.OperationalError as e:
                if e.args[0][:13] == 'no such table':
                    initialiseDb(room)
                    print("Table didn't exist, now Reinitialised. Please try again.")
                else:
                    print(
                        "Sqlite3 error, This is likely due to the database being open, Please close it before trying again")
            db.commit()
            db.close()
        else:
            pass
            # print("User chose cancel")
    else:
        print("This should be unreachable - No date selected.")


# Only to be used if the database is not working/not there or wanting a reset since drops the table
def initialiseDb(room):
    # Makes tables for rooms (for teachers)
    db = sqlite3.connect("User_Data.db")
    c = db.cursor()
    c.execute(f"DROP TABLE IF EXISTS Teacher_Bookings_{room}")
    c.execute(f'''CREATE TABLE IF NOT EXISTS Teacher_Bookings_{room} (
    PeriodID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT,
    FOREIGN KEY (Username) REFERENCES Login_Information(Username)
    );''')
    # Using code from before in the calendar to find the number of days in a month
    currentDate = datetime.datetime.now().date()
    if currentDate.day < 20:
        nextMonthDate = currentDate + datetime.timedelta(days=30)
    else:
        nextMonthDate = currentDate + datetime.timedelta(days=20)
    numDaysInMonth = (nextMonthDate.replace(day=1) - datetime.timedelta(days=1)).day
    # This goes to the number of days in a month-1 which is what is wanted starting from 0
    for x in range(numDaysInMonth * 5):
        c.execute(f"INSERT INTO Teacher_Bookings_{room} (Username) VALUES (?)", (None,))

    db.commit()
    db.close()


# Unused
def dateSelectedEventHandler(event, cal):
    selectedDate = cal.get_date()


def teacherCalendar(period, username, room, currentDateDisabled=False):
    if not os.path.exists("User_Data.db"):
        print("DB not detected")
        initialiseDb(room)

    # Disables dates which shouldn't be selected
    def configureAvailability(period, currentDay, numDaysInMonth, room):
        db = sqlite3.connect("User_Data.db")
        c = db.cursor()
        listOfPeriodInMonth = []
        # -1 since inclusive (and I want the number of days elapsed)
        for daysElapsed in range(currentDay - 1, numDaysInMonth):
            # This gets the Period ID's of days available
            listOfPeriodInMonth.append(daysElapsed * 5 + period)
        tupleOfPeriodInMonth = tuple(listOfPeriodInMonth)
        # Gets The PeriodID and Username from the bookings
        c.execute(f"SELECT PeriodID,Username FROM Teacher_Bookings_{room} WHERE PeriodID in {tupleOfPeriodInMonth}")
        listOfPeriodAndNamesInMonth = c.fetchall()
        # Now we have each day and a username in a tuple (or None if no booking)
        # And we iterate through these days and if the username is present disable it since booked
        for periodNameTuple in listOfPeriodAndNamesInMonth:
            if periodNameTuple[1] is not None:
                dayToDisable = (periodNameTuple[0] // 5) + 1
                dateToDisable = datetime.datetime(currentDate.year, currentDate.month, dayToDisable)
                # requires coordinates since the calendar library is hard to work with
                i, j = cal._get_day_coords(dateToDisable)
                cal._calendar[i][j].state(['disabled'])

    root = tk.Tk()
    root.title("Date picker")

    # To be used for limiting dates
    # Current date - allows for date=currentDate.year/month/day

    currentDate = datetime.datetime.now().date()

    if currentDate.day < 20:
        nextMonthDate = currentDate + datetime.timedelta(days=30)
    else:
        nextMonthDate = currentDate + datetime.timedelta(days=20)
    nextMonthDate = nextMonthDate.replace(day=1) - datetime.timedelta(days=1)

    # If the current period for the day is disabled, also disable it here
    if currentDateDisabled:
        # Calendar
        cal = tkcal.Calendar(root, selectmode="day", mindate=currentDate + datetime.timedelta(days=1),
                             maxdate=nextMonthDate, showothermonthdays=False,
                             disableddaybackground="red", disableddayforeground="black", normalbackground="green")
    else:
        cal = tkcal.Calendar(root, selectmode="day", mindate=currentDate,
                             maxdate=nextMonthDate, showothermonthdays=False,
                             disableddaybackground="red", disableddayforeground="black", normalbackground="green")
    cal.pack(padx=20, pady=20)

    # Button to select date
    selectDate = tk.Button(root, text="Select Date",
                           command=lambda c=cal, p=period, r=room, u=username: dateSelected(c, p, r,
                                                                                            u))  # Staying alive
    selectDate.pack()

    # Configures the calendar to disable booked spots
    configureAvailability(period, currentDate.day, nextMonthDate.day, room)

    root.mainloop()


if __name__ == "__main__":
    teacherCalendar(3, "John", "H7")
