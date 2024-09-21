
import time
import subprocess
import logging
import ipaddress
from datetime import datetime
import os



class dhcpcd_config_obj:

    def __init__(self, path, config) -> None:
        self.res = response()
        self.res.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.filepath = path
        self._config = config
        self.lines = self._read_file()
        self.buffer = self.lines
        self.new_ip = ""
        self._static_const="static ip_address="
        
        logging.info("dhcpcd config object created")

    def _validate_address(self,add_str, net_str)->bool:
        logging.info("validate_address() called")
        
        try:
            ip = ipaddress.ip_address(add_str)
            net_str = ipaddress.ip_network(net_str, strict=False)
            return ip in net_str
        except Exception as e:
            logging.error(f"_validate_address() . error : {e}")
            self.res.errors.append(f"ERROR : Given IPV4 Address is not valid. Address :{add_str}")
            return False
        
    def _get_base_ipv4(self,ip)->str:
        split_ip = ip.split('.')
        base = split_ip[0]+'.'+split_ip[1]+'.'+split_ip[2]+'.0'
        return base

    def _read_file(self)-> bool:
        logging.info(f"Opening {self.filepath}")

        try:
            with open(self.filepath, 'r') as file:
                return file.readlines()
        except PermissionError:
            logging.error("Read File(path) -> Unable to open file")
            self.res.errors.append(f"ERROR : Unable to open network configuration file")
        except FileNotFoundError:
            logging.error("Read File(path) -> path does not exist")
            self.res.errors.append(f"ERROR : Configuration file does not exist")
        except OSError as e:
            logging.error(f"Read File(path) -> {e}")
            self.res.errors.append(f"ERROR : {e}")


    def replace_address(self) ->bool:
        """replace address
        Args:
            args (list) : [interface, new address]
        Returns:
            bool : failed or success
        """
        #validate address
        if self._validate_address(self._config[1], self._get_base_ipv4(self._config[1])+'/24'):
            self.new_ip = self._config[1]
            self._config[1] = self._static_const+self._config[1]+'/24\n'
            index = 0
            for line in self.lines:
                if(self._config[0] in line):
                    self.lines[index+1] = self._config[1]
                index += 1

            logging.info("replace_address(self) : validation and replacement successful")
            return True
        else :
            logging.debug("replace_address(self) failed validation")
            self.res.errors.append(f"ERROR : Failed IPV4 address validation")
            return False

    def writeTofile(self, path) -> bool:
        """Write Configuration to file
        Args:
            path (string): file path
        Returns:
            bool : failed or success
        """
        logging.info("writeTofile(self, path) : write to dhcpcd file started")
        try:
            with open(path, 'w') as file:
                for line in self.lines:
                    file.write(line)
                return True
        except PermissionError:
            logging.error("writeTofile() -> Unable to open file")
            self.res.errors.append(f"ERROR : Unable to open network configuration file")
            return False
        except FileNotFoundError:
            logging.error("WriteoFile(path) -> file not found")
            self.res.errors.append(f"ERROR : Configuration file does not exist")
            return False
        except OSError as e:
            logging.error(f"WriteToFile(path) -> {3}")
            self.res.errors.append(f"ERROR : {e}")
            return False


    def restart_dhcpcd(self) -> bool:
        """Restart dhcpcd service
        """
        try:
            process_ret = subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], capture_output=True, text=True)
            time.sleep(2)
            process_ret = subprocess.run(['sudo', 'systemctl', 'restart', 'dhcpcd'], capture_output=True, text=True)

            if process_ret.returncode == 0:
                logging.info("restart_dhcpcd(self) : restart successful")
                if self._check_connection():
                    self.res.status = "successful"
                    return True
                else:
                    self.res.errors.append(f"ERROR : new address connection failed")
                    self._restore_dhcpcd_settings()
                    return False
            else :
                self.res.errors.append(f"ERROR : dhcpcd restart failed")
                return False

            
        except Exception as e:
            logging.error(f"(restart_dhcpcd). Error : {e}")
            self.res.errors.append(f"ERROR : {e}")
            self._restore_dhcpcd_settings()
            return False
        

    def _restore_dhcpcd_settings(self):
        try:
            with open(self.filepath, 'w') as file:
                for line in self.buffer:
                    file.write(line)
                    pass
        except Exception as e:
            self.res.errors.append(f"ERROR : {e}")
            logging.error(f"restore_dhcpcd_settings(self) . error : {e}")
            

    def _check_connection(self)->bool:
        """check connection
        """
        print(self.new_ip)
        try:
            ret = subprocess.run(['ip', 'addr' ,'show' ,'wlan0'], capture_output=True, text=True)
            print(f"return :{ret.stdout}")
            if ret.returncode == 0:
                if self.new_ip in ret.stdout:
                    logging.info("check_connection() : configuration successful")
                    return True
                else:
                    logging.info("check_connection() : configuration failed")
                    return False

            else:
                return False
        except Exception as e:
            self.res.errors.append(f"ERROR : {e}")
            logging.error(f"_check_connection(self) . error : {e}")
            return False


    def config_ip_address(self)->bool:
        #attempt to replace address
        if self.replace_address():
            #write replacement to dhcpcd conf
            if self.writeTofile(self.filepath):
                if self.restart_dhcpcd():
                    
                    self.res.response_construct()
                    return True
                else :
                  
                    self.res.response_construct()
                    return False
            else :
                
                self.res.response_construct()
                return False
        else :
            
            self.res.response_construct()
            return False
    
        
class response:

    def __init__(self):
        self.errors = []
        self._response = {}
        self._id = 11
        self.status = 'failed' 
        self.start_time = None
        self.stop_time = None


    def response_construct(self)->dict:
        res = {
                "request_id" : self._id,
                "alias" : "wlan0 config",
                "status" : self.status,
                "errors" : self.errors,
                "timestamp":
                {
                    "start":self.start_time,
                    "end":self.start_time,
                },

                "logs": ""

                }
        return res
    def get_response(self)->dict:
        self.stop_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.response_construct()


    




def main():
    #constants
    ETH0_INTERFACE_STR  =   "interface eth0"
    WLAN0_INTERFACE_STR =   "interface wlan0"


    #logging
    logging.basicConfig(level=logging.DEBUG, filename='../logs/wlan_config_log.txt',format='%(asctime)s - %(levelname)s - %(message)s')

    #receive Ip address
    NEW_ADDRESS =  '192.168.2.120'

    #dhcp file path
    dhcpcd_conf_file_path = "/etc/dhcpcd.conf"
    test_file = "../src/test_file"
    
    #new settings
    settings = [WLAN0_INTERFACE_STR, NEW_ADDRESS]

  
    #config
    conf = dhcpcd_config_obj(dhcpcd_conf_file_path, settings)
    #conf = dhcpcd_config_obj(test_file, settings)
    

    
    if conf.config_ip_address():
        print(conf.res.get_response())
    else :
        print(conf.res.get_response())

    #pipe output
    fifo = "../pipes/lan_config_fifo"
    
    try:
        with open(fifo, 'w') as pipe:
            pipe.write(str(conf.res.get_response()))
            pipe.flush()
    except Exception as e:
        print("failed to pipe : catch my drift\n")
    


    


if __name__ == "__main__":
    main()
