from zeroconf import ServiceBrowser, Zeroconf

INAME = 0
IADDR = 1
IPORT = 2
DADDR = 0
DPORT = 1

def get_info(zeroconf, type, name):
    info = zeroconf.get_service_info(type, name) 
    if info is not None:
        name = info.get_name()
        addresses = info.parsed_addresses()
        port = info.port
        return (name, addresses, port)
    return None

class DiscoveryListener:
    def __init__(self, servicedict):
        self.servicedict = servicedict;

    def remove_service(self, zeroconf, type, name):
        info = get_info(zeroconf, type, name)
        if info:
            print("Service %s removed" % (name,))
            del self.servicedict[info[INAME]]

    def add_service(self, zeroconf, type, name):
        info = get_info(zeroconf, type, name)
        if info:
            print("Service %s added, addresses: %s" % (info[INAME], info[IADDR]))
            self.servicedict[info[INAME]] = (info[IADDR], info[IPORT])

    def update_service(self, zeroconf, type, name):
        info = get_info(zeroconf, type, name)
        if info:
            print("Service %s updated, addresses: %s" % (info[INAME], info[IADDR]))
            self.servicedict[info[INAME]] = (info[IADDR], info[IPORT])

""" Vi ska kolla efter dessa tjänster:
    opc.tcp" = "_opcua-tcp._tcp"
    "opc.https" eller "https" = "_opcua-https._tcp"
    "opc.wss" = "_opcua-wss._tcp"
    enligt https://github.com/OPCFoundation/UA-LDS/blob/master/zeroconf.c
    rad 222-238. """

types = ["_opcua-https._tcp.local.", "_opcua-tcp._tcp.local.", "_opcua-wss._tcp.local."]
class Discovery:
    def __init__(self, types):
        self.sdict = {}
        self.zeroconf = Zeroconf()
        self.types = types
        self.listener = DiscoveryListener(self.sdict)
        browser = ServiceBrowser(self.zeroconf, self.types, self.listener)

    def get_services(self):
        l = []
        if not self.sdict:
            return l
        for k in self.sdict.keys():
            name = k
            port = self.sdict[k][DPORT]
            for addr in self.sdict[k][DADDR]:
                l.append((name, addr, port))
        return l