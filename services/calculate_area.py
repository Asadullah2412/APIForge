# calculates the area of a rectangle
from fastapi import status

def area_rectangle(length:float,width:float):
    if length and width > 0:
        area = length * width

        return {
        "area" : area
        }
    else: 
        return status.HTTP_400_BAD_REQUEST
    


x = area_rectangle(length=20,width=100)
print(x)