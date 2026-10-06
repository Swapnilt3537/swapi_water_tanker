# Swapi Water Tanker Dispenser

An automated water tanker dispensing system built in Python, featuring modular design, robust input validation, a clean command-line interface, unit tests, and a modern desktop graphical user interface (GUI).

---

## 📁 Project Structure

| File | Description |
|---|---|
| [`main.py`](file:///c:/Users/Swapnil/OneDrive/Desktop/swapi_water_tanker/main.py) | **Main Entrypoint** - Launcher menu to run Version 1, Version 2 CLI, GUI, or unit tests. |
| [`tanker_core.py`](file:///c:/Users/Swapnil/OneDrive/Desktop/swapi_water_tanker/tanker_core.py) | **Core Business Logic** - Water capacity management, validation, dispensing streams, and transaction logs. |
| [`cli.py`](file:///c:/Users/Swapnil/OneDrive/Desktop/swapi_water_tanker/cli.py) | **Version 2 CLI** - Polished terminal UI with animated progress bar, formatted receipts, and input error handling. |
| [`gui.py`](file:///c:/Users/Swapnil/OneDrive/Desktop/swapi_water_tanker/gui.py) | **Desktop GUI (Tkinter)** - Visual water tank canvas, water flow animation, coin presets, and transaction log. |
| [`test_tanker.py`](file:///c:/Users/Swapnil/OneDrive/Desktop/swapi_water_tanker/test_tanker.py) | **Unit Tests** - Test suite validating input handling, capacity boundaries, and dispensing flow. |

---

## 🚀 How to Run

### 1. Launch Interactive Menu
Run the main launcher to select any mode:
```bash
python main.py
```

### 2. Launch Desktop GUI Directly
Launch the graphical user interface:
```bash
python main.py --gui
# or directly:
python gui.py
```

### 3. Launch Enhanced CLI Directly (Version 2)
```bash
python main.py --cli
# or directly:
python cli.py
```

### 4. Run Original Basic Script (Version 1)
```bash
python main.py --basic
```

### 5. Run Automated Tests
```bash
python test_tanker.py
```

---

## ✨ Features Implemented

### 🛡️ 1. Input Error Handling
- Catches non-numeric inputs (e.g., text, symbols, spaces) without crashing.
- Restricts amounts to positive integers and enforces standard coin denominations: `[1, 2, 5, 10, 15, 20]`.
- Enforces tank water limits (prevents dispensing when tank is empty or insufficient water remains).
- Provides friendly prompts allowing the user to retry or cancel gracefully.

### 💻 2. Cleaner CLI UI
- Styled banners and clean terminal framing.
- Dynamic inline animated progress bar (`[======------] 5/10 L (50.0%)`).
- Formatted transaction receipt with price calculation, dispensed quantity, and remaining tank level.
- Tanker monitor with current water levels and one-click refill option.

### 🧩 3. Modular Functions & Architecture
- Clean separation between core data model (`tanker_core.py`), user interface (`cli.py`), and desktop app (`gui.py`).
- Generator-based dispensing logic (`dispense_stream`) reusable across both terminal and GUI.

### 🖥️ 4. Modern Desktop GUI (Tkinter)
- Custom visual canvas rendering the storage tank, water level, pipe, and dispensing nozzle.
- Live animated water flow and bucket ripples during dispensing.
- One-click preset coin buttons (`₹1`, `₹2`, `₹5`, `₹10`, `₹15`, `₹20`) and custom volume input.
- Real-time progress bar and status feedback.
- Background worker thread so the interface remains silky smooth and responsive without freezing.
- Real-time transaction history logger.
