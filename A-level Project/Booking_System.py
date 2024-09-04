import tkinter as tk
import time
import datetime
from Period_selection import *
from H8_Classroom_layout_student import *
import csv
import os

# Goes in date.csv and updates it with the current date
def resetDate(currentMonth, currentDay):
    with open('date.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Month', 'Day'])
        # Writes a header
        writer.writeheader()
        writer.writerow({'Month': currentMonth, 'Day': currentDay})


def checkDate(roomList):
    # This function checks the date for date.csv and updates it accordingly to the actual date
    # It then initialises the rooms accordingly if the day/month has changed
    currentDate = datetime.datetime.now()
    currentMonth = str(currentDate.month)
    currentDay = str(currentDate.day)
    # Presence check else reset since does not exist
    if os.path.exists('date.csv'):
        with open('date.csv', 'r') as file:
            reader = csv.DictReader(file)
            dateDict = list(reader)[0]
            csvMonth = dateDict['Month']
            csvDay = dateDict['Day']
            # reset is a flag for the date.csv to be reset
            # it is done after the checks to allow the correct files to be reset
            # # (checks if month or day has changed first)
            reset = False
            if csvMonth != currentMonth:
                reset = True
                # If a new month reset all the teacher and student bookings
                for room in roomList:
                    initialiseDb(room)
                for room in roomList:
                    initialiseCsv(room)
            if csvDay != currentDay:
                # If the csv day does not match the current day then reset it
                reset = True
                for room in roomList:
                    initialiseCsv(room)

            if reset:
                # Day reset
                resetDate(currentMonth, currentDay)
    else:
        resetDate(currentMonth, currentDay)


def BookingSystem(username, rank, SEND):
    roomList = ["H8", "RC6", "H7"]

    checkDate(roomList)

    # Close the window which forces them to logout

    def logout():
        root.destroy()

    root = tk.Tk()
    root.title("Room Selection")
    root.geometry("1200x800")

    # Hidden frame for title and button
    topFrame = tk.Frame(root)
    topFrame.pack(side="top", fill="both", padx=10, pady=10)

    selectRoom = tk.Label(topFrame, text="Select room:", font=("Arial", 14))
    selectRoom.pack(side="left")

    logoutButton = tk.Button(topFrame, text="Logout", command=logout)
    logoutButton.pack(side="right")

    # Frame and button creation for each room (just repetitive buttons)
    # As a post condition I will make these classes so i can make instances of them to cut the lines of code
    centerFrame = tk.Frame(root, bg="light gray")
    centerFrame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    H8Button = tk.Button(centerFrame, text="H8", bg="dark gray", fg="white", width=10, height=2,
                         command=lambda r="H8", u=username, ra=rank, s=SEND: periodSelection(r, u, ra, s))
    H8Button.grid(row=0, column=0, padx=10, pady=10)

    RC6Button = tk.Button(centerFrame, text="RC6", bg="dark gray", fg="white", width=10, height=2,
                          command=lambda r="RC6", u=username, ra=rank, s=SEND: periodSelection(r, u, ra, s))
    RC6Button.grid(row=0, column=1, padx=10, pady=10)

    H7Button = tk.Button(centerFrame, text="H7", bg="dark gray", fg="white", width=10, height=2,
                         command=lambda r="H7", u=username, ra=rank, s=SEND: periodSelection(r, u, ra, s))
    H7Button.grid(row=0, column=2, padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    BookingSystem("bill", "Teacher", 0)
