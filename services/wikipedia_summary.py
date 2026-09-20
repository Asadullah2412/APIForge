# fetches wikipedia summary 
# can work or fails (some times good , some times dumb)
import wikipedia
from fastapi import status

def fetch_Summary(topic:str):
    try:
        summary = wikipedia.summary(topic, sentences=5)
    except wikipedia.exceptions.PageError:
        return status.HTTP_404_NOT_FOUND


    return {"summary": [summary]}


x = fetch_Summary(topic="toyota supra")
print(x)