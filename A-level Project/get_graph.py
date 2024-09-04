import tkinter as tk
from tkinter import messagebox
import csv
import os
from Dijkstas_algorithm import *


# Loads the seating arrangement...
def loadSeatingArrangement(periodNum, numOfSeats, seatingArrangement,
                           roomname):
    try:
        with open(f"{roomname}.csv", mode='r') as file:
            reader = csv.reader(file)
            try:
                # This code will loop through the code to the correct section if period one should be no change
                try:
                    # Kept being 1 behind somehow so compensation
                    next(reader)
                    for _ in range((periodNum - 1) * numOfSeats):
                        next(reader)
                except StopIteration:
                    print("StopIteration")
                # This code should get the username and password off of each row for the period
                count = 0
                for row in reader:
                    count += 1
                    seatNumber, username = row
                    if username != '':
                        seatingArrangement[seatNumber] = username
                    if count == numOfSeats:
                        break
            except ValueError:
                print("ValueError")
                pass
    except FileNotFoundError:
        pass


# Event handler once seat is booked
def getUsernameForSeat(e, seatNum, canv, classroomRoot, seatingArrangement):
    def destroyText(canv, text):
        canv.delete(text)

    usernameToDisplay = seatingArrangement[str(seatNum)]
    text = canv.create_text(canv.coords(seatNum + 1)[0] + 10, canv.coords(seatNum + 1)[1] - 10,
                            text=usernameToDisplay)
    classroomRoot.after(9999, lambda c=canv, t=text: destroyText(c, t))


# Handles seat click events
def seatClicked(event, username, seatNumber, period, seatingArrangement, roomname, canvas, classroomRoot):
    clickedSeat = event.widget
    seatNumberTag = clickedSeat.gettags("current")
    for tag in seatNumberTag:
        if tag.startswith("Seat"):
            if seatNumber not in seatingArrangement:
                # Ask for confirmation before booking the seat
                if messagebox.askokcancel("Confirmation", f"Are you sure you want to book Seat {seatNumber}?"):
                    seatingArrangement[seatNumber] = username
                    clickedSeat.itemconfig(f"Seat{seatNumber}", fill="green")
                    writeToCsv(username, seatNumber, period, roomname)
                    seatingArrangement[str(seatNumber)] = username
            else:
                # Display a message if the seat is already booked (code should be unreachable but acts as a failsafe)
                getUsernameForSeat(None, seatNumber, canvas, classroomRoot, seatingArrangement)


# Initializes the CSV file
def initialiseCsv(roomname):
    if roomname == 'PC6':
        print("PC6")
    else:
        with open(f"{roomname}.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["SeatNumber", "Username"])
            for _ in range(5):
                for seatNumber in range(1, 31):
                    writer.writerow([seatNumber, ""])


# Writes new seat reservations to the CSV file
def writeToCsv(username, seatNumber, periodNum, roomname):
    # Reads the existing data from the CSV file
    with open(f"{roomname}.csv", 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)

    # Updates the username for the specified seat number
    count = 1
    for row in data:
        if row['SeatNumber'] == str(seatNumber):
            if count == periodNum:
                row['Username'] = username
                break
            else:
                count += 1

    # Writes the updated data back to the CSV file
    with open(f"{roomname}.csv", 'w', newline='') as file:
        fieldnames = ['SeatNumber', 'Username']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# Creates the classroom interface
def Classroom(room, username, period):
    def convToGraph(root, canv, numOfSeats, seatingArrangement, acceptableEdgeLen=70):
        classGraph = SimpleWeightedGraph()
        seatCoordDict = {}
        # Calculate the coordinates of nodes to allow a quicker check
        for seatNum in range(1, numOfSeats + 1):
            if str(seatNum) in seatingArrangement:
                pass
            else:
                x0, y0, x1, y1 = canv.coords(seatNum + 1)
                seatCoordDict[seatNum] = [(x0 + x1) / 2, (y0 + y1) / 2]
        for baseSeatNum in range(1, numOfSeats + 1):
            if str(baseSeatNum) not in seatingArrangement:
                # dict of connected node and weight{connected node (e.g. 4): weight, ect}
                dictOfConnectedNodeAndWeight = {}
                # Loops through nodes to compare with base num to see if an edge should be added
                for comparisonSeatNum in seatCoordDict:
                    if comparisonSeatNum == baseSeatNum:
                        pass
                    # This should be unreachable since comparisonSeatNum is an iterable through seatCoordDict which checks for the seat being in seating arrangement before adding to the dictionary
                    elif str(comparisonSeatNum) in seatingArrangement:
                        print("Failed in seatingArrangement check")
                    else:
                        # will cut down the number of times the dictionary is accessed
                        baseSeatNumCoords = seatCoordDict[baseSeatNum]
                        comparisonseatNumCoords = seatCoordDict[comparisonSeatNum]
                        distanceToSeat = ((baseSeatNumCoords[0] - comparisonseatNumCoords[0]) ** 2 + (
                                baseSeatNumCoords[1] - comparisonseatNumCoords[1]) ** 2) ** 0.5
                        if distanceToSeat <= acceptableEdgeLen:
                            dictOfConnectedNodeAndWeight[comparisonSeatNum] = round(distanceToSeat)

                # Ensure at least one node is connected check
                if dictOfConnectedNodeAndWeight == {}:
                    closestNode = None
                    # the current closest distance to seat
                    currentDistanceToSeat = 99999
                    # find the shortest edge seat
                    for extraComparisonSeatNum in seatCoordDict:
                        extraComparisonseatNumCoords = seatCoordDict[extraComparisonSeatNum]
                        distanceToSeat = ((baseSeatNumCoords[0] - extraComparisonseatNumCoords[0]) ** 2 + (
                                baseSeatNumCoords[1] - extraComparisonseatNumCoords[1]) ** 2) ** 0.5

                        if extraComparisonSeatNum == baseSeatNum:
                            # Comparing with self
                            pass
                        elif closestNode is None:
                            closestNode = extraComparisonSeatNum
                            currentDistanceToSeat = ((baseSeatNumCoords[0] - extraComparisonseatNumCoords[0]) ** 2 + (
                                    baseSeatNumCoords[1] - extraComparisonseatNumCoords[1]) ** 2) ** 0.5
                        elif distanceToSeat < currentDistanceToSeat:
                            closestNode = extraComparisonSeatNum
                            currentDistanceToSeat = distanceToSeat
                    dictOfConnectedNodeAndWeight[closestNode] = round(currentDistanceToSeat)

                classGraph.addNode(baseSeatNum, dictOfConnectedNodeAndWeight)
        # If the graph is connected cool else retry with a bit more inefficient range
        if classGraph.isConnected():
            classGraph.plotGraph(seatCoordDict)
        else:
            acceptableEdgeLen += 50
            classGraph.destroyGraph()
            convToGraph(root, canv, numOfSeats, seatingArrangement, acceptableEdgeLen)

    # Load existing seat reservations from the CSV file into a dictionary
    seatingArrangement = {}
    # Ensure csv exists
    if not os.path.exists(f"{room}.csv"):
        initialiseCsv(room)

    classroomRoot = tk.Toplevel()
    classroomRoot.title(room)
    classroomRoot.geometry("800x600")
    classroomRoot.config(bg="grey")
    frontLabel = tk.Label(classroomRoot, text="Front", font=("Arial", 16), bg="grey")
    frontLabel.pack()

    canvas = tk.Canvas(classroomRoot, width=800, height=600, bg="gray")

    teacherChair = canvas.create_rectangle(380, 50, 420, 80, fill="dark grey", outline="black")
    canvas.itemconfig(teacherChair, state=tk.DISABLED)

    seatWidth = 20
    seatHeight = 20
    numRows = 5

    numSeatsPerRow = 6
    numOfSeats = numRows * numSeatsPerRow
    # seatingArrangement is a dictionary in the form {Seat num as a string : Username}
    loadSeatingArrangement(period, numOfSeats, seatingArrangement, room)
    for row in range(numRows):
        for seatInR in range(numSeatsPerRow):
            x0 = (seatInR * (seatWidth + 30)) + 50
            y0 = (row * (seatHeight + 50)) + 50
            seatNumber = row * numSeatsPerRow + seatInR + 1
            # seat currently = an integer starting from 2, I added the tag seat{num-1} so it can start from 1 so make more sense
            # it calculates it separately in this case since easy to and for easier creation of other classrooms
            seat = canvas.create_rectangle(x0, y0, x0 + seatWidth, y0 + seatHeight, fill="red")
            canvas.addtag_withtag(f"Seat{seatNumber}", seat)
            # Checks if the seat is already booked and update its color
            if str(seatNumber) in seatingArrangement:
                canvas.itemconfig(seat, fill="green")
                canvas.tag_bind(seat, "<Button-1>",
                                lambda e, s=seatNumber, c=canvas, r=classroomRoot,
                                       ar=seatingArrangement: getUsernameForSeat(e, s, c, r, ar))
            else:
                # Binds the seat click event to the seatClicked function
                canvas.tag_bind(seat, "<Button-1>",
                                lambda e, u=username, s=seatNumber, p=period, sa=seatingArrangement,
                                       r=room, c=canvas, ro=classroomRoot: seatClicked(e, u, s, p, sa, r, c, ro))
    # Condition here for SEND student - Only available to SEND students due to framing bias
    if True:
        shortestPathButton = tk.Button(classroomRoot, text="Book seat with shortest path to door",
                                       command=lambda c=classroomRoot, ca=canvas, n=numOfSeats,
                                                      s=seatingArrangement: convToGraph(c, ca, n, s))
        shortestPathButton.pack(anchor=tk.NW)
    canvas.pack()
    classroomRoot.mainloop()


if __name__ == "__main__":
    Classroom("H8", "Euler", 2)
