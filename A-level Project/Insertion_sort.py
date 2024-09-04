arr = [1, 32, 5, 2, 5, 6, 2, 8]
dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 8, 'I': 12, 'F': 11, 'H': 17, 'G': 15}


def insertionSort(userDict):
    userList = []
    for item in userDict:
        userList.append((item, userDict[item]))
    # Loops through each item
    for x in range(1, len(userList)):
        position = x
        # While the position is above 0 (don't want to try compare with -1) and the previous value is greater than the current value swap
        while position > 0 and userList[position][1] < userList[position - 1][1]:
            # Swapping process
            userList[position], userList[position - 1] = userList[position - 1], userList[position]
            position -= 1
    return userList


if __name__ == "__main__":
    arr = [1, 32, 5, 2, 5, 6, 2, 8]
    dic = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 8, 'I': 12, 'F': 11, 'H': 17, 'G': 15}
    print(insertionSort(dic))
