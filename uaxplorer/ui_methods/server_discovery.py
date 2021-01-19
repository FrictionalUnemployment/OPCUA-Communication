#DISCOVER ALL SERVERS WITH THIS METHOD.

TUPLE_ARRAY = []
DISCOVERY_OUTPUT = [('test_server', 'IP_ADDRESS', 'PORT_NUMBER'), ('test_server2', 'IP_ADDRESS2', 'PORT_NUMBER2')] #Change this to the discovery
                                                                #output we get later on

def insert_array(servers):
    for i in servers:
        TUPLE_ARRAY.append(i)

def get_all(array, type): #0 for server name, 1 for ip address, 2 for port number
    temp_array = []
    for i in TUPLE_ARRAY:
        temp_array.append(i[type])
    return temp_array




insert_array(DISCOVERY_OUTPUT)
print(get_all(TUPLE_ARRAY, 1))