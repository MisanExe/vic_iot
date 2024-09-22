
from NManager import NetWorkMangerObj
import logging
import time

def main():
    
    '''//Timer starts///'''
    start_time = time.time()
    '''////////////////'''

    #logging
    logging.basicConfig(level=logging.DEBUG, filename='logs/NM_Wizard_log.txt',format='%(asctime)s - %(levelname)s - %(message)s')
    wizard = NetWorkMangerObj()
    try :
        if wizard.set_new_address('192.168.2.17') :
            print(wizard.response.get_response())
        else :
            print(f"Response :\n {wizard.response.get_response()}")

    except Exception as e:
        print(f"Error : {e}")




    '''///////////////Time END//////////////////'''
    end_time = time.time()
    exec_time = end_time - start_time
    print(f"total execution time : {exec_time}")
    '''/////////////////////////////////////////'''

if __name__ == "__main__":
    main()