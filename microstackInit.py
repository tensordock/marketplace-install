import enum
import os
import subprocess
import json

os.system('lspci -nn | grep VGA |grep NVIDIA > out.temp')
os.system('lspci -nn | grep Audio |grep NVIDIA > outAudio.temp')
id=[]
idAudio=[]
whitelist = "passthrough_whitelist = ["
with open("out.temp") as f:
    for line in f:
        j = str(line).split(' ')
        for h in j:
            if "10de" in h:
                id.append(h[6:int(len(h))-1])


with open("outAudio.temp") as f:
    for line in f:
        j = str(line).split(' ')

        for h in j:
            if "10de" in h:
                idAudio.append(h[6:int(len(h))-1])
           # print(h)


#todo delete repeats

os.system('sudo echo \'\n[pci]\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    whitelist+='{"vendor_id": "10de", "product_id": "'+i+'"},'
    #os.system('sudo echo \'\npassthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in idAudio:
    whitelist+='{"vendor_id": "10de", "product_id": "'+i+'"},'
    #os.system('sudo echo \'\npassthrough_whitelist = {"vendor_id": "10de", "product_id": "'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')
whitelist = whitelist[:-1]
whitelist+=']'
os.system('sudo echo \'\n'+whitelist+'\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for i in id:
    os.system('sudo echo \'\nalias = {"vendor_id":"10de","product_id":"'+i+'","device_type":"type-PCI","name":"'+i+'"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

for idx, x in enumerate(idAudio):
    os.system('sudo echo \'\nalias = {"vendor_id":"10de","product_id":"'+x+'","device_type":"type-PCI","name":"'+id[idx]+'Audio"}\' >> /var/snap/microstack/common/etc/nova/nova.conf.d/nova-snap.conf')

os.remove('out.temp')
os.remove('outAudio.temp')


admin_project = json.loads(
    subprocess.check_output(
        ['microstack.openstack', 'project', 'show', 'admin', '-f', 'json']
        ).strip().decode('ascii'))["id"]

security_group = ""
with os.popen('microstack.openstack security group list | grep '+admin_project) as security_group_file:
    security_group = security_group_file.readline().strip().split("| ")[1]

os.system("""microstack.openstack security group rule create """+ security_group 
        +""" --protocol any --remote-ip 0.0.0.0/0 --ingress""")
