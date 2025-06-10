# RPiCWServer

A lightweight server application for transmitting CW (Morse code) messages using a **Raspberry Pi** and the **Si5351 frequency generator module**.

---

## 📦 Features

- CW (Morse code) transmission
- Web-based interface for sending messages
- Integration with Raspberry Pi GPIO and Si5351 module

---

## 🧰 Requirements

### Hardware
- Raspberry Pi (any model with GPIO)
- Si5351 frequency generator module
- Jumper wires for connections
- Internet browser (for UI access)

### Software
- Python 3.7+
- Python packages:
  ```txt
  see requirements.txt

---

## 🚀 How to Run Locally

> ⚠️ Note: Do **not** install `RPi.GPIO` unless you're running this on a **Raspberry Pi**.

```bash
# Create a virtual environment
python -m venv venv

# Activate the environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py

---

# Open your browser and go to:
- http://localhost:8080
