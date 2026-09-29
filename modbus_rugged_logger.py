'''import csv
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException

SIMULATOR_IP = "127.0.0.1"
PORT = 502
FILE_NAME = "vfd_production_telemetry.csv"

# Setup connection object
client = ModbusTcpClient(SIMULATOR_IP, port=PORT)

print("[SYSTEM]: Launching rugged industrial monitoring loop...")
print("---------------------------------------------------------------------")

while True:
    try:
        # 1. Force a network connection attempt if it's currently closed
        if not client.is_socket_open():
            client.connect()

        # 2. Try to read holding register 400003 (offset = 2)
        result = client.read_holding_registers(address=2, count=1)
        
        if result.isError():
            print("[⚠️ DATA ERROR]: Received an empty or corrupted frame from the machine.")
            time.sleep(2)
            continue

        # Extract data parameters
        raw_value = result.registers[0]
        calculated_hz = raw_value / 10.0
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{current_time}] Machine Operational | Current Speed: {calculated_hz} Hz")

        # 3. Try to append to the log file
        with open(FILE_NAME, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([current_time, raw_value, calculated_hz, "OPERATIONAL"])
            
        time.sleep(2)  # Normal 2-second cycle scan time

    # =====================================================================
    # EXCEPTION 1: Catches physical hardware drops (Cables, power down, etc.)
    # =====================================================================
    except (ModbusException, ConnectionError, OSError):
        print("[🔌 HARDWARE ALERT]: Connection to machine lost or unreachable. Retrying in 5s...")
        client.close()  # Safely flush and release the corrupted network socket port context
        time.sleep(5)   # Wait before looping back to try client.connect() again

    # =====================================================================
    # EXCEPTION 2: Catches local system file locks (Excel open)
    # =====================================================================
    except PermissionError:
        print("[⚠️ STORAGE LOCK]: Excel sheet is OPEN. Please close it so Python can write.")
        time.sleep(5)   # Wait 5 seconds to give the user time to close Excel

    # Safe escape exit trigger
    except KeyboardInterrupt:
        print("\n[SYSTEM]: Shutdown sequence initialized by engineer.")
        break

client.close()
print("[SYSTEM]: Network socket lines closed. System stopped safely.")


#connect()  ──► fails ──► returns False (usually no exception)
#   │
 #  ▼ succeeds
#read/write request
   #├─ pipe breaks         ──► ConnectionError / OSError
   #├─ no reply / bad reply ──► ModbusException
   #└─ device says "no"    ──► result.isError() is True'''
'''Situation	Why
Right after client = ModbusTcpClient(...)	No connection attempted yet, client.socket is None
client.connect() was never called	Same reason
client.connect() failed	Failed attempt stores no socket
You called client.close()	close() sets client.socket = None
Returns True
Situation	Why
client.connect() succeeded and you haven't closed it	The socket is stored
Connection was good, then the machine crashed or the cable was pulled, but you haven't called close() yet	Socket is still stored locally, even though the connection is actually dead'''
import csv
import time
from datetime import datetime
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
sim_ip='127.0.0.1'
Port=502
FILE_NAME = "vfd_production_telemetry.csv"
client=ModbusTcpClient(sim_ip,port=Port)
while True:
    try:
        if client.is_socket_open():
            client.connect()

        result=client.read_holding_registers(address=2,count=1)
        if result.isError():
            print('recived empty or corrupted frame from machine ')
            time.sleep(5)
            continue
        raw_value=result.registers[0]
        calcualted_hz=raw_value/10
        time_stamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f'[{time_stamp}]--->raw vlaue:{raw_value}...Calculated frequncy--{calcualted_hz}')
        with open(FILE_NAME,'a',newline='') as f:
            writer=csv.writer(f)
            writer.writerow([time_stamp,raw_value,calcualted_hz,'operational'])
            time.sleep(3)
    except (ModbusException,ConnectionError,OSError):
        print('connection to machine lost or unrechable...')
        time.sleep(5)
    except PermissionError:
        print('Excelfile may be open ')
        print('[remides].... close file then try again.... ')
        time.sleep(5)
    except KeyboardInterrupt:
        print('loging closed sucessfuly........')
        break
client.close()
print('system stop safely..........')

        
            
        
        
            
        
        