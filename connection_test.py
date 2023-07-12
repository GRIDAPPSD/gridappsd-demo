from gridappsd import GridAPPSD

MY_IP_ADDRESS = "xx.xxx.xxx.xx"
gapps = GridAPPSD(stomp_address=MY_IP_ADDRESS, stomp_port=61613, username="system", password="manager")

assert gapps.connected