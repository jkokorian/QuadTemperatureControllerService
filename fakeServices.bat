start python QuadTemperatureControllerService.py --fake=True --service-port=5060
start python TemperatureControllerService.py --modbus-service=tcp://127.0.0.1:5060 --service-port=5061 --device-id=tc1
start python TemperatureControllerService.py --modbus-service=tcp://127.0.0.1:5060 --service-port=5062 --device-id=tc2
start python TemperatureControllerService.py --modbus-service=tcp://127.0.0.1:5060 --service-port=5063 --device-id=tc3
start python TemperatureControllerService.py --modbus-service=tcp://127.0.0.1:5060 --service-port=5064 --device-id=tc4