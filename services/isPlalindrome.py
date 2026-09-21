# returns true if it is plalindorm or return false
from fastapi import status
def isPlaindrome(word:str):
    if word.isspace() == False:

        return {
            "isPlaindrome" : (word.lower() == word[::-1].lower())
        }
    else:
        raise ValueError("invalid input")

# x = isPlaindrome(word="  ")
# print(x)