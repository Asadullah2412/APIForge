# returns true if it is plalindorm or return false
from fastapi import status
def isPlaindrome(word:str):
    if word.isspace() == False:

        return {
            "isPlaindrome" : (word == word[::-1])
        }
    else:
        return status.HTTP_400_BAD_REQUEST

x = isPlaindrome(word="  ")
print(x)