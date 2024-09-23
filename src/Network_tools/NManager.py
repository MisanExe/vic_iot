import subprocess
import NManager_except as NM_except
import re
from scapy.all import ARP, Ether, srp
import logging
from NM_wizard_res import response
import os
import time



class NetWorkMangerObj:

    def __init__(self) -> None:
        self.response = response()
        self.Conf_file_path = "/etc/NetworkManager/system-connections/"
        self.Nm_present = self._isInstalled()
        #check if net manager exists
        if not self.Nm_present:
            raise NM_except.NetworkManagerNotInstalled("Error : __init__() Unable to create object")
        #get current ssid
        self.ssid = self._get_ssid().strip()
        if self.ssid =='':
            raise NM_except.UnableToRetrive_SSID("Error : __init__() unable to retrive SSID")
        
        #construct connection config path
        self.Conf_file_path= self.Conf_file_path+self.ssid+'.nmconnection'

        #get file content
        self.Conf_file = self._read_configFile() #mutable file member
        self.temp_file = self.Conf_file          #temp storage of file for restoration

        #regex pattern for ip address
        self._ip_pattern = r"\b(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\b"


        #get address and Gateway
        self.address, self.gateway, self.subnet, self.index = self._get_ipv4_n_Gateway()
        print(f"address: {self.address}, gateway: {self.gateway}, subnet :{self.subnet}, index {self.index}")
    
        if re.match(self._ip_pattern, self.address) == None:
            raise NM_except.IPv4_AddressInvalid("Error : IPV4 address is invalid. Unable to create object")
        
        
        


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
                self.response.errors.append(f"Error [get_ssid(self)] Unable to get current ssid")
                return None
        except Exception as e:
            self.response.errors.append(f"Error : {e}")
            print(f"Error : {e}")

    def _read_configFile(self):

        try:
            with open(self.Conf_file_path, 'r') as config_file:
                return config_file.readlines()
        except Exception as e:
            print(f"Error : {e}")
            self.response.errors.append(f"Error : {e}")
            return None
        
    def _get_ipv4_n_Gateway(self):
        index = 0
        for line in self.Conf_file:
            index += 1
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
            

              return address, gateway, subnet, index
            
        
        return None
    
    def set_new_address(self, new_add):
        #set request
        self.response.request = 'Set new static IPV4 address'

        
        #validate address
        if self._validate_ipv4_address(new_add):
            try:
                new_conf = self._replace_as_static_address(new_add)
            except Exception as e:
                print(f"Error : {e}")
                #set response
                self.response.errors.append(f"Error : {e}")
                #construct a response
                self.response.response_construct()
                return False
            
            if new_conf != None:
                #write to system configuration file
                if self._write_to_conf(new_conf, self.Conf_file_path) :
                    #restart network manager
                    self.restart_network_manager()
                    time.sleep(4)
                    #check current ip address
                    if self._check_wireless_ip_connection(new_add):
                        #set status
                        self.response.status = 'success'
                        #construct response
                        self.response.response_construct()
                        return True
                    else :
                        #restore ip address
                        #construct a response
                        self.response.response_construct()
                        return False
                else :
                    self.response.errors.append(f"Error : [_validate_ipv4_address(new_add)] Error writing to config file!")
                    #construct a response
                    self.response.response_construct()
                    return False
            else :
                self.response.errors.append(f"Error : [_validate_ipv4_address(new_add)] Unable to edit IPV4 settings. try again!")
                #construct a response
                self.response.response_construct()
                return False
            
        else :
            #construct a response
            self.response.response_construct()
            return False
            


    def _validate_ipv4_address(self, address)->list:
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
            raise NM_except.IPv4_AddressInvalid("Error : [validate_ipv4_address] IPV4 address is invalid. Unable to create object")
        
        #check that new address matches gateway
        index = 0
        for gateway_octet, address_octet in zip(self.gateway.split('.'), address.split('.')):
            if gateway_octet == address_octet:
                index += 1
            if index == 3:
                 addr = self._scan_for_active_ip(address)
                 if len(addr) == 1:
                     return True
                 else:
                     self.response.suggestions = addr
                     self.response.errors.append(f"Error : Given already exists on network")
                     return False
        self.response.errors.append(f"Error : [validate_ipv4_address(self, address)] Failed attempt to validate IPV4 address")  
        return False
    

    
    def _scan_for_active_ip(self, ip)->list:
        """Scans for if an ip address is already active on the network
            parameters:
                ip : address to search for
            Returns 
                bool : True or False
            Raises:
        """
        # arp request to find all ip's on network
        ip_cidr = (ip+'/'+self.subnet)
        arp = ARP(pdst=ip_cidr)
        ether = Ether(dst='ff:ff:ff:ff:ff:ff')
        packet = ether/arp

        #send packet
        result = srp(packet, timeout=2, verbose=False)[0]
        addresses= []
        for req, res in result:
            addresses.append(res.psrc)

        ret = []
        
        if ip in addresses:
            #return unused addresses
            ret = self.__get_unassigned_ipv4(ip, addresses)
            return ret
        else:
            ret.append(ip)
            return ret
        
    def __get_unassigned_ipv4(self, ip, address_list)->list:
        """ Returns a list of unassigned ipv4 addresses

            Parameters :
                address list : a list of assigned addresses 
        """
        temp = self.gateway.split('.')
        slice_net = temp[0]+'.'+temp[1]+'.'+temp[2]+'.'
        slice_net.strip()
        ret_addr = []
        ret_addr.append(ip)
        
        for addr in range(0, 255):
            if not (slice_net+str(addr) in address_list):
                ret_addr.append(slice_net+str(addr))
                
        return ret_addr

    def _replace_as_static_address(self, new_addr)->list:
        """ Replaces current [ipv4] settings with specified static ip

            Parameters :
                new_addr : (str) new address
            Return :
                new_conf : (list) new configuration
        """
        static_line = "method=manual\naddress1="+new_addr+'/'+self.subnet+','+self.gateway+'\n'
        static_line_split = static_line.splitlines()
        #print(f"static line :{static_line_split}")
        
        #variables
        found_flag = False
        new_conf = []
        index = 0
    
        


        try:
            for line in self.Conf_file:
               
                if '[ipv4]' in line:
                    found_flag = True

                if found_flag :
                    if 'dns=' in line :
                        new_conf.append(line)
                        found_flag = False
                    elif '[ipv4]' in line:
                        new_conf.append(line)
                    elif not('dns=' in line ) and len(static_line_split) != index:
                        
                        print(index)
                        new_conf.append(static_line_split[index])
                        index += 1         
                else :
                    new_conf.append(line)
                    
            return new_conf
        except Exception as e :
            print(f"Error occurred {e}")
            self.response.errors.append(f"Error : {e}")
            return None
       


    def _write_to_conf(self, new_conf, path='../test_file'):
        """
            writes the new configuration to the config file

            Parameters:
                new_conf : (list) new configuration 
                path : (str). Defaults for a file in the source folder
        """
         #check if size is ok
        if len(self.Conf_file) >= len(new_conf):
            print("ok")
            try:
                with open(path, 'w') as conf_file:
                    for line in new_conf:
                        if not line.endswith('\n'):
                            conf_file.write(f"{line}\n")
                        else:
                            conf_file.write(line)
                        
                    
                return True
            except Exception as e:
                print(f"Error {e}")
                self.response.errors.append(f"Error : {e}")
                return False
        else :
            self.response.errors.append(f"Error : [write_to_conf(self, new_conf, path='../test_file')] new_conf list is bogus")
            return False
        
    def restart_network_manager(self)->bool:
        try:
            ret = subprocess.run("sudo systemctl restart NetworkManager", capture_output=True, text=True, shell=True)
            if ret.returncode == 0:
                print(f"return code : {ret.returncode} , restarted network manager")
                return True
            else :
                if self.restart_network_manager():
                    return True
                else :
                    self.response.errors.append(f"Error : [restart_network_manager()] Unable to complete restart")
                    return False
        except Exception as e:
            self.response.errors.append(f"Error : [restart_network_manager()] {e}")
            print(f"Error : {e}")


    def _check_wireless_ip_connection(self, new_addr, web=False, packets=2)->bool:

        try:
            ret = None
            if not web :
                
                ret = subprocess.run(f"ping -c {packets} {new_addr}", capture_output=True, text=True, shell=True)
            else :
                ret = subprocess.run(f"ping -c {packets} google.com", capture_output=True, text=True, shell=True)
                pass

            if ret.returncode == 0 :
                print(f"new address is active {ret.stdout}")
                return True
            else :
                print(f"new address is inactive. return code {ret.returncode}\nstd error : {ret.stderr}\nstd out : {ret.stdout} , {ret.args}")
                #print("os failed too")
                return False
            
        except Exception as e:
            print(f"Error: {e}")
            self.response.errors.append(f"Error : {e}")
            return False
    

        
                

          
           

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

    


            
