
def factorial(userInp):
    if userInp <2:
        return 1
    else:
        return userInp * factorial(userInp-1)

print(factorial(4))