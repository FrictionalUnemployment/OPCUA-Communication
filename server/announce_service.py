from zeroconf import ServiceInfo, Zeroconf
import socket

ZC_PORT = 4840
DEV_NAME = "_testopc."

def start_service_announcement():
    info = ServiceInfo("_opcua-tcp._tcp.local.",
        DEV_NAME + "_opcua-tcp._tcp.local.",
        port = ZC_PORT,
        server=DEV_NAME,
        addresses=[socket.inet_pton(socket.AF_INET, get_ip_address())])
    zeroconf = Zeroconf()
    zeroconf.register_service(info)

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == "__main__":
    print("Starting service announcement for testing purposes"!)
    print("Press enter to exit.")
    start_service_announcement()
    input()