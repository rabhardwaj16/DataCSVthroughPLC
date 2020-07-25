import csv, os, datetime
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusException
client = ModbusTcpClient('192.168.1.10')
Triggered = False

while True:
    try:
        rightnow = datetime.datetime.now()
        date = rightnow.strftime("%d/%m/%Y")
        time = rightnow.strftime("%H:%M:%S")
        
        # Creating Folder
        dirName = 'D:/PythonCSV'
        if not os.path.exists(dirName):
            os.makedirs(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            pass
        
        # Creating .csv data file on hourly basis
        file_n = "Python"+rightnow.strftime('%Y%m%d_%H')+".csv"
        file_dir = dirName + "/" +file_n
        
        #Data Read
        bit_input = client.read_coils(0).bits
        save_trig = bit_input[0]
        reg_lst = client.read_holding_registers(10, 10).registers
        chr_lst=[chr(od) for od in reg_lst]
        
        #String(List to String)
        string_data = ""
        for a in chr_lst:  
               string_data += a

        if save_trig == True:
            if Triggered == False:
                if not os.path.exists(file_dir):
                    with open(file_dir, 'w', newline='') as csvfile:
                        field_names = ['Data', 'Date', 'Time']
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writerow(
                            {'Data': 'Data','Date': 'Date','Time': 'Time'})
                        writer.writerow({'Data': string_data,'Date': date, 'Time': time})
                else:
                    with open(file_dir, 'a', newline='') as csvfile:
                        field_names = ['Data', 'Date', 'Time']
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writerow({'Data': string_data,'Date': date, 'Time': time})         
                print(f"{date}, {time}, File Updated")
                Triggered = True
        else:
            Triggered = False
    except AttributeError:
        print("Connection Lost")
    except ModbusException:
        print("Connection Lost, waiting for connection...")
    except KeyboardInterrupt:
        print("Quitting..")
        break
