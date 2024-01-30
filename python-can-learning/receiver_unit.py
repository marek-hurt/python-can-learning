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
        message_counts = {}
        with open(self.output_file, 'w') as file:
            while self.running:
                message = self.bus.recv()
                if message is None or message.arbitration_id not in self.accepted_ids:
                    continue

                #update statistics
                message_counts[message.arbitration_id] = message_counts.get(message.arbitration_id, 0) + 1
                
                file.write(str(message) + '\n')
                file.write(str(message_counts[message.arbitration_id]) + '\n')
                if message.arbitration_id == 0xFF:
                    self.send_statistics(message_counts)
                    self.stop_receiving()

    def stop_receiving(self):
        self.running = False
        print("0xFF message received in unit with output file: ", self.output_file)
        
    def send_statistics(self, message_counts):
        for adress, count in message_counts.items():
            if adress != 0xFF:  # Ignore ID 0xFF
                response_message = can.Message(arbitration_id=adress, data=count.to_bytes(4, byteorder='big'), is_extended_id=False)
                self.bus.send(response_message)
                