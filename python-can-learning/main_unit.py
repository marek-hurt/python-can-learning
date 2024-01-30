'''
Created on 30. 1. 2024

@author: marek
'''
# main_unit.py
import can
import time

class MainUnit:
    def __init__(self, input_file, bus_type='virtual', channel='vcan0', bitrate=500000):
        self.input_file = input_file
        self.bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate)

    def run(self):
        try:
            with can.BLFReader(self.input_file) as log:
                for msg in log:
                    self.bus.send(msg)
                    time.sleep(0.001)
        except can.CanError as e:
            print("CAN communication error:", e)
            
    def receive_responses(self):
        print("Receiving...")
        while True:
            message = self.bus.recv(timeout=10)
            if message is None:
                break
            print(f"Received message: ID={message.arbitration_id}, Data={message.data}")
            
    def close_bus(self):
        print("close the CAN bus")
        self.bus.shutdown()
        