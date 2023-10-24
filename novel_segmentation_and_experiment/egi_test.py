from egi_pynetstation import NetStation
import time


"""Test whether the EGI device can be connected properly, record the EEG data, and apply markers."""

print("import pynetstation")
# set ip address
IP_ns = '10.10.10.42'
# Set a port that NetStation will be listening to as an integer
port_ns = 55513
ns = NetStation.NetStation(IP_ns, port_ns)
# Set an NTP clock server (the amplifier) address as an IPv4 string
IP_amp = '10.10.10.51'
ns.connect(ntp_ip=IP_amp)

# sync_time = time.time()
# ns.set_synched_time(sync_time)

print("connected to netstation")


ns.begin_rec()
print("start recording")

n = 5
test_data = {"dogs": "0001"}
while n > 0:
    time.sleep(2)
    ns.send_event(event_type="test")
    n -= 1

# ns.end_rec()
# ns.disconnect()