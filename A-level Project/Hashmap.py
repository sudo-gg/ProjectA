import hashlib
import random


class HashMap:
    # Constructor
    def __init__(self, maxLength):
        self.length = 0
        self.maxLength = maxLength
        self.map = {}
        self.overflowTable = []
        self.overflowLength = maxLength

    def hash(self, input):
        # Added a measure to keep consistent hashing
        key = str(input)
        hashObject = hashlib.sha256()
        hashObject.update(key.encode('utf-8'))
        hashedText = hashObject.hexdigest()
        return hashedText

    def add(self, key):
        if self.length < self.maxLength:
            hashVal = hash(key)
            try:
                # when self.map[hashVal] is called, if it does not exist key error so can be added
                # If not a collision and just a duplicate
                if self.map[hashVal] == key:
                    print("already in table")
                    pass
                # Collision handling
                else:
                    self.overflowTable.append(key)
                    self.overflowLength += 1
            #
            except KeyError:
                self.map[hashVal] = key
                self.length += 1
        else:
            print("Max size reached")

    def find(self, key):
        hashAddress = hash(key)
        try:  # If failed then no self.map at the address hence not in the hashmap
            return f"{self.map[hashAddress]} is at {hashAddress}"
        except KeyError:
            return False

    def delete(self, key):
        hashAddress = hash(key)
        try:  # Attempts to pop but if cant then false address so return false
            self.map.pop(hashAddress)
            self.length -= 1
        except KeyError:
            return False


hm1 = HashMap(4)
hm1.add("help")
hm1.add("bi")
hm1.add("ge")
hm1.add("1")
hm1.add("12")
hm1.delete("ge")
hm1.add("afterdelete")
print(hm1.map)
