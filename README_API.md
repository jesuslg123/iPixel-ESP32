# ESP32-iPixel API Guide

**ESP32-iPixel** is a project to control **iPixel color matrices** using an ESP32 microcontroller.  
It exposes the device's functionality via a **REST API** served by a built-in web server.

---

> [!NOTE]  
> This is the **actual working API** for the current development version.  
> The main README is outdated and refers to a previous API structure.

# ⚠️⚠️⚠️ UNSTABLE
This is currently only work-in-progress with the only supported device being the ESP32-S3 (SuperMicro).  
Support for further ESP32 boards is planned.  

---

## 🔧 API Workflow

The API uses a **two-step process**:

1. **Pair a device** via Bluetooth to get a unique ID
2. **Use that ID** in all subsequent control commands

---

## 📡 Pairing Endpoints

### Add a Pairing
**POST/GET** `/bluetooth/pairings/add`

Add a new Bluetooth device to the pairing list.

**Parameters:**
- `name` (string): Friendly name for the device (e.g., "Living Room Matrix")
- `mac` (string): BLE MAC address of the device (e.g., `19:2D:FE:55:52:AA`)
- `enabled` (boolean): Whether to connect to this device on startup (default: `true`)

**Response:**
```json
{
  "ok": true,
  "data": {
    "id": "464097975",
    "name": "Living Room Matrix",
    "mac": "19:2D:FE:55:52:AA",
    "enabled": true
  }
}
```

**Example:**
```bash
curl 'http://192.168.4.1/bluetooth/pairings/add?name=MyMatrix&mac=19:2D:FE:55:52:AA&enabled=true'
```

---

### List All Pairings
**GET** `/bluetooth/pairings/list`

Get all paired devices with their IDs.

**Response:**
```json
{
  "ok": true,
  "data": [
    {
      "id": "464097975",
      "name": "Living Room Matrix",
      "mac": "19:2D:FE:55:52:AA",
      "enabled": true
    },
    {
      "id": "123456789",
      "name": "Bedroom Matrix",
      "mac": "AA:BB:CC:DD:EE:FF",
      "enabled": false
    }
  ]
}
```

**Example:**
```bash
curl 'http://192.168.4.1/bluetooth/pairings/list'
```

---

### Update a Pairing
**GET** `/bluetooth/pairings/update`

Update an existing paired device's settings.

**Parameters:**
- `id` (string): The pairing ID (from list or add response)
- `name` (string): New friendly name
- `mac` (string): New BLE MAC address
- `enabled` (boolean): Whether to auto-connect

**Example:**
```bash
curl 'http://192.168.4.1/bluetooth/pairings/update?id=464097975&name=Updated Name&enabled=false'
```

---

### Remove a Pairing
**GET** `/bluetooth/pairings/remove`

Remove a device from the pairing list.

**Parameters:**
- `id` (string): The pairing ID to remove

**Example:**
```bash
curl 'http://192.168.4.1/bluetooth/pairings/remove?id=464097975'
```

---

## 🎮 Control Endpoints

All control endpoints require a `device` parameter with the **pairing ID** (not the MAC address).

### Clear Display
**GET** `/control/raw/clear`

Clear all content from the display.

**Parameters:**
- `device` (string): Pairing ID

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/clear?device=464097975'
```

---

### Set Brightness
**GET** `/control/raw/setBrightness`

Adjust display brightness.

**Parameters:**
- `device` (string): Pairing ID
- `brightness` (0-100): Brightness level

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setBrightness?device=464097975&brightness=75'
```

---

### Set Speed
**GET** `/control/raw/setSpeed`

Adjust animation speed.

**Parameters:**
- `device` (string): Pairing ID
- `speed` (0-100): Speed level

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setSpeed?device=464097975&speed=50'
```

---

### Set Time
**GET** `/control/raw/setTime`

Set the device's time display.

**Parameters:**
- `device` (string): Pairing ID
- `hour` (0-23): Hour
- `minute` (0-59): Minute
- `second` (0-59): Second

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setTime?device=464097975&hour=14&minute=30&second=0'
```

---

### Set Fun Mode
**GET** `/control/raw/setFunMode`

Enable or disable fun mode.

**Parameters:**
- `device` (string): Pairing ID
- `funMode` (true/false): Enable fun mode

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setFunMode?device=464097975&funMode=true'
```

---

### Set Orientation
**GET** `/control/raw/setOrientation`

Set display orientation.

**Parameters:**
- `device` (string): Pairing ID
- `orientation` (0-2): Orientation mode

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setOrientation?device=464097975&orientation=0'
```

---

### LED Control
**GET** `/control/raw/setLED`

Control LED state.

**Parameters:**
- `device` (string): Pairing ID
- `on` (true/false): Turn LEDs on or off

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setLED?device=464097975&on=true'
```

---

### Set Pixel
**GET** `/control/raw/setPixel`

Set an individual pixel color.

**Parameters:**
- `device` (string): Pairing ID
- `x` (0-255): X coordinate
- `y` (0-255): Y coordinate
- `r` (0-255): Red component
- `g` (0-255): Green component
- `b` (0-255): Blue component

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setPixel?device=464097975&x=10&y=5&r=255&g=0&b=0'
```

---

### Send Text
**GET** `/control/raw/sendText`

Display text on the matrix.

**Parameters:**
- `device` (string): Pairing ID
- `text` (string): Text to display
- `animation` (0-7): Animation style
- `save_slot` (1-10): Save slot
- `speed` (0-100): Text speed
- `colorR` (0-255): Red component
- `colorG` (0-255): Green component
- `colorB` (0-255): Blue component
- `rainbow_mode` (0-9): Rainbow effect mode
- `matrix_height` (0-255): Matrix height (typically 16)

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/sendText?device=464097975&text=Hello&animation=0&save_slot=1&speed=50&colorR=255&colorG=0&colorB=0&rainbow_mode=0&matrix_height=16'
```

---

### Send PNG
**GET** `/control/raw/sendPNG`

Send a PNG image to the display.

**Parameters:**
- `device` (string): Pairing ID
- `hex` (string): Hex-encoded PNG file data

**Note:** Convert your PNG to hex using online tools like "File to Hex" converter.

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/sendPNG?device=464097975&hex=89504e470d0a1a0a...'
```

---

### Send GIF
**GET** `/control/raw/sendGIF`

Send a GIF animation to the display.

**Parameters:**
- `device` (string): Pairing ID
- `hex` (string): Hex-encoded GIF file data

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/sendGIF?device=464097975&hex=47494638...'
```

---

### Delete Screen
**GET** `/control/raw/deleteScreen`

Delete a saved screen from a slot.

**Parameters:**
- `device` (string): Pairing ID
- `screen` (0-10): Screen slot to delete

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/deleteScreen?device=464097975&screen=1'
```

---

### Set Clock Mode
**GET** `/control/raw/setClockMode`

Configure clock display mode.

**Parameters:**
- `device` (string): Pairing ID
- `style` (1-8): Clock style
- `dayOfWeek` (1-7): Day of week
- `year` (0-99): Year (last 2 digits)
- `month` (1-12): Month
- `day` (1-31): Day

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setClockMode?device=464097975&style=1&dayOfWeek=5&year=25&month=12&day=6'
```

---

### Set Rhythm Level Mode
**GET** `/control/raw/setRhythmLevelMode`

Set rhythm level visualization.

**Parameters:**
- `device` (string): Pairing ID
- `style` (0-4): Style
- `l0` (0-15): Level 0 through `l14` (0-15): Level 14

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setRhythmLevelMode?device=464097975&style=0&l0=5&l1=10&l2=8&l3=12&l4=6&l5=9&l6=7&l7=11&l8=8&l9=10&l10=9&l11=12&l12=7&l13=8&l14=10'
```

---

### Set Rhythm Animation Mode
**GET** `/control/raw/setRhythmAnimationMode`

Set rhythm animation mode.

**Parameters:**
- `device` (string): Pairing ID
- `style` (0-1): Style
- `frame` (0-7): Frame

**Example:**
```bash
curl 'http://192.168.4.1/control/raw/setRhythmAnimationMode?device=464097975&style=0&frame=3'
```

---

## 🚀 Quick Start

### Step 1: Connect to WiFi
1. Power on the ESP32
2. If no WiFi credentials are saved, it will start AP mode: `iPixel-ESP32` / `123456789`
3. Or add WiFi credentials first via the WiFi pairing endpoints (below)
4. Once connected, note the IP address from the serial logs

### Step 1b: Add your local WiFi (so you do not need the AP)
```bash
# Add home WiFi with priority 10
curl 'http://192.168.4.1/wifi/pairings/add?ssid=YourSSID&password=YourPass&enabled=true&priority=10'

# Optional: scan to discover SSIDs
curl 'http://192.168.4.1/wifi/scan/start'
curl 'http://192.168.4.1/wifi/scan/list'
```
- The device orders enabled WiFi pairings by `priority` and connects in station mode.
- AP mode is only used if every saved WiFi pairing fails; once it joins your LAN, use the LAN IP shown in serial logs.

### Step 2: Pair Your Device
Discover your iPixel device's BLE MAC address (using Android BLE Scanner or similar), then:

```bash
curl 'http://192.168.x.x/bluetooth/pairings/add?name=MyMatrix&mac=19:2D:FE:55:52:AA&enabled=true'
```

Save the returned `id` value (e.g., `464097975`).

### Step 3: Control Your Device
Use the pairing ID in all subsequent commands:

```bash
# Clear the display
curl 'http://192.168.x.x/control/raw/clear?device=464097975'

# Display text
curl 'http://192.168.x.x/control/raw/sendText?device=464097975&text=Hello&animation=0&save_slot=1&speed=50&colorR=255&colorG=0&colorB=0&rainbow_mode=0&matrix_height=16'

# Set brightness
curl 'http://192.168.x.x/control/raw/setBrightness?device=464097975&brightness=80'
```

---

## 🖼️ GFX (Advanced)
**ESP32-iPixel** features an early-stage GFX stack for rendering element-based views via JSON.  
See [GFX.md](GFX.md) for details.

---

## 📝 Todo
* Support `sendText` for other matrices than 96x16
* Password or key-based protection
* Connection improvements (faster connect? better disconnect handling?)
* Clock Mode via NTP
* Web Flasher Support
* Update main README with correct API

---

## 🙏 Credits
Reverse engineering of the protocol by **[lucagoc](https://github.com/lucagoc)** via his **[iPixel-CLI](https://github.com/lucagoc/iPixel-CLI)**.

## 🤖 AI Disclaimer
Some descriptions and code-snippets in this repository are generated by artificial intelligence.
