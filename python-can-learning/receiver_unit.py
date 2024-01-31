'''
Created on 30. 1. 2024

@author: Marek Hurt
'''
# receiver_unit.py
import can
import threading

class ReceiverUnit(threading.Thread):
    """
    Represents a receiver unit in a CAN bus simulation, handling message receiving.
    """
    def __init__(self, accepted_ids, output_file, bus_type='virtual', channel='vcan0', bitrate=500000):
        """
        Constructor that Initializes the ReceiverUnit with specified CAN bus configuration.

        Args:
            accepted_ids (list): List of message IDs that this unit should accept.
            output_file (str): Path to the file where received messages are logged.
            bus_type (str): The type of the bus (default is 'virtual').
            channel (str): The channel of the bus (default is 'vcan0').
            bitrate (int): The bitrate of the bus (default is 500000).
        """
        super().__init__()
        self.accepted_ids = accepted_ids
        self.output_file = output_file
        self.bus = can.interface.Bus(bustype=bus_type, channel=channel, bitrate=bitrate)
        self.running = True

    def run(self):
        """
        Runs the receiver unit, receiving messages and logging them to the output file.
        Stops receiving and sends statistics back to the bus when a message with ID 0xFF is received.
        """
        message_counts = {}
        with open(self.output_file, 'w') as file:
            while self.running:
                message = self.bus.recv()
                if message is None or message.arbitration_id not in self.accepted_ids:
                    continue

                #update statistics - increase message count
                currentCount = message_counts.get(message.arbitration_id, 0)
                message_counts[message.arbitration_id] = currentCount + 1
                
                file.write(str(message) + '\n')
                if message.arbitration_id == 0xFF:
                    self.__send_statistics(message_counts)
                    self.__stop_receiving()

    def __stop_receiving(self):
        """
        Stops the receiver unit from receiving any more messages.
        """
        self.running = False
        print("0xFF message received in unit with output file: ", self.output_file)
        
    def __send_statistics(self, message_counts):
        """
        Sends statistics of received messages back to the CAN bus.

        Args:
            message_counts (dict): A dictionary of message counts keyed by message IDs.
        """
        for adress, count in message_counts.items():
            if adress != 0xFF:  # Ignore ID 0xFF
                response_message = can.Message(arbitration_id=adress, data=count.to_bytes(4, byteorder='big'), is_extended_id=False)
                self.bus.send(response_message)
                