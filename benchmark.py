import sys
import psutil
import os

os.system('rm benchmark.txt')
os.system('rm network.txt')
os.system('rm portAvail.txt')

ethernetDevice = input("input the name of your networking device")
#vmCount = input("Maximum VMs that will run on server?")
#portRange = input("Range of ports in 'xxxx-yyyy' format").split("-")
#portSkip = input("Enter reserved ports to skip over separated with commas").split(",")

with open('/home/tensordock/.td_network.txt', 'w') as bench:
    bench.write(ethernetDevice+"\n")
#    bench.write(vmCount+"\n")
#    bench.write(portRange[0]+" "+portRange[1]+"\n")
#    bench.write(''.join(str(x) for x in portSkip)+"\n")
    
with open('/home/tensordock/.td_benchmark.txt', 'w') as bench:
    bench.write(str(psutil.cpu_count(logical=False))+"\n")
    bench.write(str(psutil.virtual_memory().total)+"\n")
    bench.write(str(psutil.disk_usage('/').total)+"\n")


vcpus = str(psutil.cpu_count(logical=True))
ram = str(int(round(psutil.virtual_memory().total/(1024*1024)-4096,0)))
os.system('microstack.openstack quota set --instances 999 --cores '+vcpus+' --ram '+ram+' admin')

#portskip not implemented yet
