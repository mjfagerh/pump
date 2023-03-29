


import logging
import asyncio
import platform
import ast

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover

# These values have been randomly generated - they must match between the Central and Peripheral devices
# Any changes you make here must be suitably made in the Arduino program as well

SERVICE = "19B10010-E8F2-537E-4F6C-D104768A1214"
CHAR = "19b10011-e8f2-537e-4f6c-d104768a1214"





def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def is_int(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def create_byte_map():
    arr = [0,0.001]
    for i in range(2,201):
        arr.append(0.005*(i-1))
    for i in range(202,204):
        arr.append(10**(i-201))
    return arr

def print_byte_map():
    for i,flow in enumerate(create_byte_map()):
        print(f"In pos {i} you get {flow} microL/min")



async def setflow(client):
    val = int(input('Enter input (use printed list):'))
    byt_map = create_byte_map()

    print(f"you wrote {val} this should give a flow of {byt_map[val]} which is {byt_map[val]*2000} hz")
    byte_to_send = val.to_bytes(1,"little")
    await client.write_gatt_char(CHAR, byte_to_send, response=True)


async def run():
    print('ProtoStax MKR 1010 Peripheral Central Service')
    print('Looking for MKR 1010 BLE Sense Peripheral Device...')

    found = False
    devices = await BleakScanner.discover()
    print("The following devices was fund::")
    for d in devices:
        print(d)
    name = "pump"
    for d in devices:
        if d.name != None:
            if name in d.name:
                print('connected to pump')
                print_byte_map()
                found = True
                async with BleakClient(d.address) as client:
                    print(f'Connected to {d.address}')
                    val = await client.read_gatt_char(CHAR)
                    while True:
                        await setflow(client)

    if not found:
        print('Could not find Arduino Nano 33 BLE Sense Peripheral')


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
