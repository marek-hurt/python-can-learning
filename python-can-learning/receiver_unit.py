'''
Created on 30. 1. 2024

@author: marek
'''
# receiver_unit.py
import can
import threading

class ReceiverUnit(threading.Thread):
    def __init__(self, accepted_ids, output_file, bus_type='virtual', channel='vcan0', bitrate=500000):
        super().__init__()
        self.accepted_ids = accepted_ids
        self.output_file = output_file
        self.bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate)
        self.running = True

    def run(self):
        with open(self.output_file, 'w') as file:
            while self.running:
                message = self.bus.recv()
                if message is None or message.arbitration_id not in self.accepted_ids:
                    continue

                file.write(str(message) + '\n')
                if message.arbitration_id == 0xFF:
                    self.stop_receiving()

    def stop_receiving(self):
        self.running = False
        print("0xFF message received in unit with output file: ", self.output_file)