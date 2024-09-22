import subprocess
import NManager_except as NM_except
import re
import scapy



class NetWorkMangerObj:

    def __init__(self) -> None:
        self.Conf_file_path = "/etc/NetworkManager/system-connections/"
        self.Nm_present = self._isInstalled()
        #check if net manager exists
        if not self.Nm_present:
            raise NM_except.NetworkManagerNotInstalled("Error : Unable to create object")
        #get current ssid
        self.ssid = self._get_ssid().strip()
        #construct connection config path
        self.Conf_file= self.Conf_file_path+self.ssid+'.nmconnection'

        #get file content
        self.Conf_file = self._read_configFile().splitlines() #mutable file member
        self.temp_file = self.Conf_file          #temp storage of file for restoration

        #regex pattern for ip address
        self._ip_pattern = r"\b(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"


        #get address and Gateway
        self.address, self.gateway, self.subnet = self._get_ipv4_n_Gateway()
        print(f"address: {self.address}, gateway: {self.gateway}, subnet :{self.subnet}")
    
        if re.match(self._ip_pattern, self.address) == None:
            raise NM_except.IPv4_AddressInvalid("Error : IPV4 address is invalid. Unable to create object")
        
        self._validate_ipv4_address("192.168.2.100")
        
        print("created object")
        
        


        


    def _isInstalled(self)->bool:
        alias = 'network-manager'
        try:
            ret = subprocess.run(['dpkg', '-l' , '|', 'grep', 'network-manager'], capture_output=True, text=True)
            for line in ret.stdout.splitlines():
                if alias in line:
                    return True
                
        except Exception as e :
            print(f"Error failed {e}")
            return False
        
        return False
    
    def _get_ssid(self)->str:
        try:
            ret = subprocess.run("nmcli -t -f active,ssid dev wifi | grep '^yes:'", capture_output=True, text=True, shell=True)
            if 'yes' in ret.stdout:
                ssid = ret.stdout.split(':')[1]
                return ssid
            else:
                return None
        except Exception as e:
            print(f"Error : {e}")

    def _read_configFile(self):

        try:
            with open(self.Conf_file, 'r') as config_file:
                content = config_file.read()
            return content
        except Exception as e:
            print(f"Error : {e}")
            return None
        
    def _get_ipv4_n_Gateway(self):
        for line in self.Conf_file:
          if 'address' in line:
              #split line
              temp_ls = line.split('=')[1]
              address = temp_ls.split(',')[0].strip()
              gateway = temp_ls.split(',')[1].strip()
              subnet = None
              #get subnet 
              if '/' in address:
                  subnet = address.split("/")[1].strip()
                  address = address.split("/")[0].strip()

              return address, gateway, subnet
        
        return None
    
    def set_new_address(self, new_add):

        #validate address
        #replace line with address
        #write to conf file
        #restart network manager
        #validate new connection else write old content back and restart manager
        #return info
        pass

    def _validate_ipv4_address(self, address):
        """
            Validates the supplied ip address
            Parameters:
                address : ipv4 octet x.x.x.255
            Returns:
                bool : True or False
            Raises:
                IPv4_Address invalid : if the supplied address doesnt match
        """
        #validate address
        if re.match(self._ip_pattern, address) == None:
            raise NM_except.IPv4_AddressInvalid("Error : IPV4 address is invalid. Unable to create object")
        
        #check that new address matches gateway
        index = 0
        for gateway_octet, address_octet in zip(self.gateway.split('.'), address.split('.')):
            if gateway_octet == address_octet:
                index += 1
            if index == 3:
                return True
        return False
    
    def _scan_for_active_ip(self, ip):
        """Scans for if an ip address is already active on the network
            parameters:
                ip : address to search for
            Returns 
                bool : True or False
            Raises:
        """
        pass
    

                
    def _replace_address():
        pass

          
           

def find(needle, haystack)->int:
    indx = 0
    haystack_len = len(haystack)
    needle_len = len(needle)

    for i in range(0, haystack_len):
        if needle[indx] == haystack[i]:
            indx += 1
            if needle_len == indx:
                return i-needle_len
        else :
            indx = 0

    return -1

    


            
