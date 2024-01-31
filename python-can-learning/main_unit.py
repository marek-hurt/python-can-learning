'''
Created on 30. 1. 2024

@author: Marek Hurt
'''
# main_unit.py
import can
import time

class MainUnit:
    """
    Represents the main unit in a CAN bus simulation, handling message sending.

    Attributes:
        input_file (str): The path to the BLF file containing CAN messages.
        bus (can.Bus): The CAN bus interface.
    """
    def __init__(self, input_file, bus_type='virtual', channel='vcan0', bitrate=500000):
        self.input_file = input_file
        self.bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate)

    def run(self):
        """
        Reads and sends messages from the BLF file to the CAN bus.
        """
        try:
            with can.BLFReader(self.input_file) as log:
                for msg in log:
                    self.bus.send(msg)
                    time.sleep(0.001)
        except can.CanError as e:
            print("CAN communication error:", e)
            
    def receive_responses(self):
        """
        Receives responses from other units on the CAN bus.
        Continues receiving until no more messages are left.
        """
        print("Receiving...")
        while True:
            message = self.bus.recv(timeout=1)
            if message is None:
                break
            print(f"Received message: ID = {hex(message.arbitration_id)}, Number of messages = {int.from_bytes(message.data, byteorder='big')}")
            
    def close_bus(self):
        """
        Closes the CAN bus.
        """
        print("Closing CAN bus in main unit.")
        self.bus.shutdown()
        