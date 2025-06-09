from BusinessLogic.platform_detector import IS_RASPBERRYPI
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from BusinessLogic.morse import MorseTranslator
from BusinessLogic.si5351_controller import Si5351
from BusinessLogic.si5351Base import Si5351Base
import asyncio
from BusinessLogic.transmission_request import TransmissionRequest


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize hardware
if IS_RASPBERRYPI:
    si5351 = Si5351()
else:
    si5351 = Si5351Base()

morse = MorseTranslator()

# Global variables for control
is_transmitting = False


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/start")
async def start_transmission(request: TransmissionRequest):
    global is_transmitting
    is_transmitting = True

    # Convert message to Morse code
    morse_code = morse.text_to_morse(request.message)
    dot_duration = 1.2 / request.speed  # Standard dot duration formula

    print('Frequency: ' + str(request.frequency))
    si5351.set_frequency(request.frequency)

    # Transmit the message
    async def transmit():
        while 1:
            if not is_transmitting:
                break
            for symbol in morse_code:
                if not is_transmitting:
                    break
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
            await asyncio.sleep(dot_duration * 3)

    if morse_code:
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

    uvicorn.run(app, host="0.0.0.0", port=8080)
