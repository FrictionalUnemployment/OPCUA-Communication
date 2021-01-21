from zeroconf import ServiceInfo, Zeroconf
import socket

# This file handles the announcement of the OPCUA
# service for zeroconf discovery to work.
#
# Usage:
# Call the start_service_announcement() function.
# Input is name of the device and the port it's using.

# Standard OPCUA server port, per IANA.
ZC_PORT = 4840
# Test
DEV_NAME = "_testopc."

def start_service_announcement(device_name=DEV_NAME, port=ZC_PORT):
    info = ServiceInfo("_opcua-tcp._tcp.local.",
        device_name + "_opcua-tcp._tcp.local.",
        port = ZC_PORT,
        server=device_name,
        addresses=[socket.inet_pton(socket.AF_INET, get_ip_address())])
    zeroconf = Zeroconf()
    zeroconf.register_service(info)

# Hacky way to get ip address which isn't localhost under linux.
# The google dns ip does not have to be routeable.
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == "__main__":
    print("Starting service announcement for testing purposes"!)
    print("Press enter to exit.")
    start_service_announcement()
    input()