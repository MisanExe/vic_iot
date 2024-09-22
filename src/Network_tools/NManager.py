import subprocess




class NetworkObjError(Exception):
    """Base class for exceptions"""
    pass

class NetworkManagerNotInstalled(NetworkObjError):
    """Exception raised if Network manager is not installed"""
    def __init__(self, value, message="Network manager is not installed!"):
        self.value = value
        self.msg  = message
        super().__init__(self.msg)

class NetWorkMangerObj:

    def __init__(self) -> None:
        self.Conf_file_path = "/etc/NetworkManager/system-connections/"
        self.Nm_present = self._isInstalled()
        #check if net manager exists
        if not self.Nm_present:
            raise NetworkManagerNotInstalled("Error : Unable to create object")
        #get current ssid
        self.ssid = self._get_ssid().strip()
        #construct connection config path
        self.Conf_file= self.Conf_file_path+self.ssid+'.nmconnection'

        #get file content
        self.Conf_file = self._read_configFile() #mutable file member
        self.temp_file = self.Conf_file          #temp storage of file for restoration

        print(self.temp_file)

        self._get_ipv4_n_Gateway()


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
        pos = find('address', self.Conf_file)
        if pos <0:
            return None
        print(f"Found it at {pos}")
          
           

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

    


            
