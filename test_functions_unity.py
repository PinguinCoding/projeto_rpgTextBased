# This file serve from being a playground where I can test all the functions and write the code
# without distractions

class Zone(object):
    def __init__(self, ID=None):
        self.ID = ID
        self.ZONE_NAME = ''
        self.DESCRIPTION = ''
        self.EXAMINATION = ''
        self.ELEMENTS = {}
        self.CHANGES = {}
        self.ITEMS = {}
        self.solved = False


class Node:
    def __init__(self, data: object):
        self.data = data
        self.neighbors = []

    def get_neighbors(self):
        list_zone = list()
        zone_info = [0, 0]
        for node in self.neighbors:
            zone_info[0] = node.data.ZONE_NAME
            zone_info[1] = node.data.ID
            list_zone.append(tuple(zone_info))
        return list_zone

    def get_neighbors_directions(self):
        if len(self.neighbors) == 4:
            neighbors = self.get_neighbors()
            return print(f"North neighbor: {neighbors[0][1]}\nEast neighbor: {neighbors[1][1]}\nSouth neighbor: "
                         f"{neighbors[2][1]}\nWest neighbor: {neighbors[3][1]}")


class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, data):
        new_node = Node(data)
        self.nodes.append(new_node)

    def add_edge(self, node1_data, node2_data):
        node1 = self.find_node(node1_data)
        node2 = self.find_node(node2_data)
        if node1 and node2:
            node1.neighbors.append(node2)
            node2.neighbors.append(node1)

    @staticmethod
    def construct(center, *adjacent_zones):
        for zone in adjacent_zones:
            my_graph.add_edge(center, zone)

    def find_node(self, data):
        for node in self.nodes:
            if node.data == data:
                return node
        return None

    def display(self):
        for node in self.nodes:
            neighbors = node.get_neighbors()
            print(f"Zone ID: {node.data.ID} \nZone Name: {node.data.ZONE_NAME} \nZone Neighbors: {neighbors}")
            print()


# Exemplo de uso:
if __name__ == "__main__":
    my_graph = Graph()

    zone_a = Zone(ID="A")
    zone_b = Zone(ID="B")
    zone_c = Zone(ID="C")
    zone_d = Zone(ID="D")
    zone_e = Zone(ID="E")
    zone_f = Zone(ID="F")
    zone_g = Zone(ID="G")
    zone_h = Zone(ID="H")
    zone_i = Zone(ID="I")

    zone_a.ZONE_NAME = "Corridor A"
    zone_b.ZONE_NAME = "Cafeteria"
    zone_c.ZONE_NAME = "Classroom A"
    zone_d.ZONE_NAME = "Corridor B"
    zone_e.ZONE_NAME = "Classroom B"
    zone_f.ZONE_NAME = "Council room"
    zone_g.ZONE_NAME = "Computer Lab"
    zone_h.ZONE_NAME = "Corridor C"
    zone_i.ZONE_NAME = "Science Lab"

    my_graph.add_node(zone_a)
    my_graph.add_node(zone_b)
    my_graph.add_node(zone_c)
    my_graph.add_node(zone_d)
    my_graph.add_node(zone_e)
    my_graph.add_node(zone_f)
    my_graph.add_node(zone_g)
    my_graph.add_node(zone_h)
    my_graph.add_node(zone_i)

    my_graph.construct(zone_a, zone_b, zone_c, zone_d, zone_e)
    my_graph.construct(zone_d, zone_h, zone_f, zone_g)
    my_graph.construct(zone_h, zone_i)

    for node in my_graph.nodes:
        print(node.data.ID)
        node.get_neighbors_directions()
        print()
# When edges are added, they must be added in the formula north-east-south-west
# All neighbors are displayed counterclockwise
