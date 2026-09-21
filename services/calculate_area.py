# calculates the area of a rectangle
def area_rectangle(length:float,width:float):
    if length and width > 0:
        area = length * width

        return {
        "area" : area
        }
    else: 
        raise ValueError("Length and width should be positive numbers")
    


# x = area_rectangle(length=20,width=100)
# print(x)