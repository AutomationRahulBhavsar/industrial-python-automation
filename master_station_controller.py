import csv
import time
import logging
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

# Silence internal library logs
logging.getLogger("pymodbus").setLevel(logging.CRITICAL)

SIMULATOR_IP = "127.0.0.1"
PORT = 502
FILE_NAME = "factory_production_log.csv"

client = ModbusTcpClient(SIMULATOR_IP, port=PORT)

print("[SYSTEM]: Launching Master Station Controller (Bits + Registers)...")
print("---------------------------------------------------------------------")

while True:
    try:
        if not client.is_socket_open():
            client.connect()

        # ---------------------------------------------------------------------
        # 1. READ BLOCK: Collect both Bits and Analog numbers from the machine
        # ---------------------------------------------------------------------
        # Read Safety E-Stop Switch (Discrete Input 10003 -> Offset 2)
        safety_check = client.read_discrete_inputs(address=2, count=1)
        
        # Read Live Motor Speed (Holding Register 400003 -> Offset 2)
        speed_check = client.read_holding_registers(address=2, count=1)

        if safety_check.isError() or speed_check.isError():
            print("[⚠️ DATA ERROR]: Frame corrupted this cycle. Skipping...")
            time.sleep(2)
            continue

        # Extract values
        is_estop_tripped = safety_check.bits[0]
        raw_speed = speed_check.registers[0]
        calculated_hz = raw_speed / 10.0
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # ---------------------------------------------------------------------
        # 2. LOGIC & WRITE BLOCK: Evaluate safety data and push corrections
        # ---------------------------------------------------------------------
        if is_estop_tripped == True:
            # HAZARD STATE: Turn Alarm Lamp ON (Coil 00001 -> Offset 0) and Force Speed to 0 Hz
            print(f"[{current_time}] 🚨 HAZARD! E-Stop Active! Shutting down motor speed safely.")
            client.write_coil(address=0, value=True)
            client.write_register(address=2, value=0)
            status = "EMERGENCY SHUTDOWN"
        else:
            # SAFE STATE: Keep Alarm Lamp OFF and display operating data
            print(f"[{current_time}] 🟢 OPERATIONAL | Motor Speed: {calculated_hz} Hz")
            client.write_coil(address=0, value=False)
            status = "NORMAL RUN"

        # ---------------------------------------------------------------------
        # 3. STORAGE BLOCK: Save the unified data row to your Excel spreadsheet
        # ---------------------------------------------------------------------
        try:
            with open(FILE_NAME, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([current_time, calculated_hz, is_estop_tripped, status])
        except PermissionError:
            print("[⚠️ STORAGE LOCK]: Close your Excel sheet so data can log!")

        time.sleep(1) # Fast 1-second process monitoring scan rate

    except (ModbusException, ConnectionError, OSError):
        print("[🔌 NETWORK FAULT]: Physical line dropped. Reconnecting in 5s...")
        client.close()
        time.sleep(5)
        
    except KeyboardInterrupt:
        print("\n[SYSTEM]: Graceful shutdown executed by engineer.")
        break

client.close()
