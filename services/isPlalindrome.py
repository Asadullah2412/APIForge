# returns true if it is plalindorm or return false

def isPlaindrome(word:str):

    return {
        "isPlaindrome" : (word == word[::-1])
    }

x = isPlaindrome(word="racecar")
print(x)