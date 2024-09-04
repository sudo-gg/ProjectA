import tkinter as tk
import datetime
from H8_Classroom_layout_student import *
from Teacher_Calendar import *
from tkinter import messagebox
import os

periodStartTimes = [("Period 1", "08:45:00"), ("Period 2", "09:50:00"), ("Period 3", "11:05:00"),
                    ("Period 4", "12:10:00"), ("Period 5", "14:20:00")]
# Used for testing
#periodStartTimes = [("Period 1", "18:45:00"), ("Period 2", "20:04:00"), ("Period 3", "20:07:00"),
#                    ("Period 4", "22:10:00"), ("Period 5", "23:20:00")]


def periodSelection(room, username, rank, SEND):
    # Back button handler...
    def Back():
        periodMenu.destroy()

    def periodDisabledCheck(periodNum, periodStart):
        # Period check
        currentTime = datetime.datetime.now().strftime("%H:%M:%S")

        # Teacher booked check
        currentDaysElapsed = datetime.datetime.now().date().day - 1
        firstPeriodId = currentDaysElapsed * 5
        db = sqlite3.connect("User_Data.db")
        c = db.cursor()
        periodId = firstPeriodId + int(periodNum)
        try:
            c.execute(
                f'''SELECT Username FROM Teacher_Bookings_{room} WHERE PeriodID = {periodId} AND Username IS NOT NULL''')
            if c.fetchone() is None:
                # If not booked return the result of the time check
                return currentTime < periodStart
            else:
                # Booked so false
                return False
        # Error handler if no table initialise the database
        except sqlite3.OperationalError as e:
            if e.args[0][:13] == 'no such table':
                initialiseDb(room)
            else:
                print(
                    "Sqlite3 error, This is likely due to the database being open, Please close it before trying again")

    def nextMenu(room, period, username, rank):
        # Gives the next menu from the period selection depending on rank
        # Also a secondary time check to ensure not got past the system (explained in development)
        currentTime = datetime.datetime.now().strftime("%H:%M:%S")
        if currentTime < periodStartTimes[period - 1][1]:
            if rank == "Teacher":
                teacherCalendar(period, username, room)
            elif rank == "Student":
                Classroom(room, username, period, SEND)
        else:
            teacherCalendar(period, username, room, True)

    periodMenu = tk.Toplevel(bg="#E5E1DA")
    periodMenu.title(room)
    periodMenu.geometry("800x600")

    roomLabel = tk.Label(periodMenu, text=room, font=("Arial", 20))
    roomLabel.grid(row=0, column=0, padx=10, pady=10)

    backButton = tk.Button(periodMenu, text="Back", command=Back)
    backButton.grid(row=0, column=2, padx=50, pady=10, sticky="E")
    # This just loops through a count variable and names the fields in periodStartTimes to iteratively create the buttons
    for x, (periodName, periodStart) in enumerate(periodStartTimes):
        periodButton = tk.Button(periodMenu, text=periodName, width=80, height=2,
                                 command=lambda ro=room, p=x + 1, u=username, r=rank: nextMenu(ro, p, u, r),
                                 state=tk.NORMAL if periodDisabledCheck(periodName[7],
                                                                        periodStart) or rank == "Teacher" else tk.DISABLED)
        # 'button comprehension?'
        periodButton.grid(row=x + 1, column=1, padx=10, pady=10)

    periodMenu.mainloop()


if __name__ == "__main__":
    roomName = "H8"
    userName = "John"
    userRank = "Student"
    periodSelection(roomName, userName, userRank, 1)
