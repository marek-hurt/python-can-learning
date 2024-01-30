'''
Created on 30. 1. 2024

@author: marek
'''
# run_simulation.py
from main_unit import MainUnit
from receiver_unit import ReceiverUnit

def main():
    
    # run main unit, parameter input blf file
    main_unit = MainUnit('input.blf')
    
    #define receiver unit
    unit1 = ReceiverUnit([0xC0FFEE, 0xCACA0, 0xFF], 'output1.asc')
    unit2 = ReceiverUnit([0xBEEF, 0xFF], 'output2.asc')

    main_unit.run()
    unit1.start()
    unit2.start()

    unit1.join()
    unit2.join()
    print("connection lost")
if __name__ == "__main__":
    main()
