import subprocess
import  sys

#RETURN CODES
PROCESS_ERROR 	= -10
VALID_SSID 		= 120
INVALID_SSID 	= -120
FEW_ARGS		= -121

def Auth_ssid(input_ssid)->int:
	#start subprocess to  get ssid
	try:
		ret = subprocess.run(['sudo', 'iwlist' , 'wlan0','scan'], capture_output=True, text=True)
		if input_ssid in ret.stdout:
			return VALID_SSID
	except Exception as e:
		return PROCESS_ERROR
	return INVALID_SSID


def main():
	

	if len(sys.argv) < 1:
		print(FEW_ARGS)
		sys.exit(PROCESS_ERROR)

	
	try:	
		user_input =  sys.argv[1] 
	except Exception as e:
		print("PROCESS ERROR")
		exit(PROCESS_ERROR)


	res = Auth_ssid(user_input) 
	if  res == VALID_SSID:
		print("VALID SSID")
		sys.exit(VALID_SSID)

	elif res == INVALID_SSID:
		print("INVALID SSID")
		sys.exit(INVALID_SSID)
		
	elif res == PROCESS_ERROR:
		print("PROCESS ERROR")
		sys.exit(PROCESS_ERROR)


if __name__ == "__main__":
	main()
