from asyncua import Client

# Example of url:
# 'opc.tcp://localhost:4840/freeopcua/server/'
class LocalClient():
    def __init__(self, url):
        self.nodes = {}
        self.values = {}
        self.url = url

    def run(self):
        async with Client(self.url) as client:
            while True:
                for n in self.nodes.keys():
                    node = client.get_node(n)
                    value = await node.read_value()
                    self.values[self.nodes[n]] = value

    def add_node(self, node, name):
        self.nodes[node] = name

    def remove_node(self, node, name):
        self.values.pop(name)
        self.nodes.pop(node)

    def get_value(self, name):
        return self.values[name])

if __name__=="__main__":
    c = LocalClient()
