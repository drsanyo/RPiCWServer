from math import trunc

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from morse import MorseTranslator
from si5351_controller import Si5351
import asyncio
import time


# Add this class for request validation
class TransmissionRequest(BaseModel):
    message: str
    frequency: int
    speed: int


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize hardware
si5351 = Si5351()
morse = MorseTranslator()

# Global variables for control
is_transmitting = False


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Update the start_transmission endpoint
@app.post("/start")
async def start_transmission(request: TransmissionRequest):
    global is_transmitting
    is_transmitting = True

    # Convert message to Morse code
    morse_code = morse.text_to_morse(request.message)
    dot_duration = 1.2 / request.speed  # Standard dot duration formula

    # Set frequency
    si5351.set_frequency(request.frequency)

    # Transmit the message
    async def transmit():
        while 1:
            if not is_transmitting:
                break
            for symbol in morse_code:
                if not is_transmitting:
                    break
                print('transmitting... ' + symbol)
                if symbol == '.':
                    si5351.key_on()
                    await asyncio.sleep(dot_duration)
                    si5351.key_off()
                    await asyncio.sleep(dot_duration)
                elif symbol == '-':
                    si5351.key_on()
                    await asyncio.sleep(dot_duration * 3)
                    si5351.key_off()
                    await asyncio.sleep(dot_duration)
                elif symbol == ' ':
                    await asyncio.sleep(dot_duration * 3)

    asyncio.create_task(transmit())
    return {"status": "started"}


@app.post("/stop")
async def stop_transmission():
    global is_transmitting
    is_transmitting = False
    si5351.key_off()
    return {"status": "stopped"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
