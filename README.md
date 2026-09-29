# 🤖 Industrial Automation & Control Systems Hub

A production-ready repository containing rugged Python applications engineered to interface directly with industrial machinery, Programmable Logic Controllers (PLCs), Variable Frequency Drives (VFDs), and robotic workstations over the **Modbus TCP/IP** protocol. 

---

## 🛠️ Repository Architecture

This repository showcases an enterprise-grade automation architecture built specifically to survive harsh factory floor environments:

1. **`master_station_controller.py` (Unified Control Node)**
   * **Telemetry Scanning:** Executes a high-speed, 1-second process loop that reads physical binary input states (`read_discrete_inputs`) and 16-bit analog registers (`read_holding_registers`) simultaneously.
   * **Safety Interlocking:** Evaluates discrete sensor configurations (such as proximity switches and E-Stops) and immediately executes fail-safe command updates (`write_coil`, `write_register`) to drive actuators to safe operational thresholds instantly.
   * **Data Processing & Scaling:** Programmatically manages register multiplier steps, converting raw 16-bit unsigned integer counts into human-readable engineering metrics (e.g., scale counts of `500` translate precisely to `50.0 Hz`).

2. **`modbus_rugged_logger.py` (Industrial Data Logger)**
   * **Network Exception Armor:** Engineered with dual-layer exception handlers. If a physical communication line drops, power drops out, or noise disrupts transmission frames, the script safely catches the exception, closes the socket context, and runs a 5-second auto-reconnection recovery thread without crashing.
   * **File System Protection:** Features `PermissionError` monitoring modules. If an engineer opens the runtime log report inside Microsoft Excel, the logging script handles the file lock gracefully, alerts the workstation terminal, and prevents system crashes.

---

## 🎛️ Core Specialized Toolkit
* **Languages & Protocols:** Python, Modbus TCP/IP (Industrial Ethernet)
* **Libraries:** `pymodbus` (Network Infrastructure Management), `csv` (Local Storage Engines), `datetime` (Production Timestamp Tracking)
* **Core Competencies:** Control Loop Optimization, Register Data Mapping, Fault Isolation, Process Scripting

---

## 🚀 Deployment & Testing Blueprint
All scripts were validated utilizing local loopback configurations (`127.0.0.1:502`) mapped directly against **ModRSsim2** simulation nodes simulating multi-axis industrial hardware registers.

*Developed by an Electrical & Robotics Service Engineer.*


