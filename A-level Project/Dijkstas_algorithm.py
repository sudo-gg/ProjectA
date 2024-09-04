import networkx as nx
import matplotlib.pyplot as plt
import random



class Graph:
    def __init__(self, graph={}):
        self._graph = graph


class SimpleWeightedGraph(Graph):
    def __init__(self, graph={}):
        super().__init__(graph)

    def destroyGraph(self):
        self._graph = {}

    def getGraph(self):
        return self._graph

    def getNodes(self):
        nodes = []
        for node in self._graph:
            nodes.append(node)
        return nodes

    def addNode(self, nodeName, dictConnectedNodesAndWeight):
        # If node is already in list then just overwrite
        if nodeName in self._graph:
            if dictConnectedNodesAndWeight == self._graph[nodeName]:
                return False
            else:
                pass
                # print("Overwriting node connections")

        self._graph[nodeName] = dictConnectedNodesAndWeight
        # Check if any connected nodes are not already in graph / Add the node to receiving nodes
        for key in dictConnectedNodesAndWeight:
            if key not in self._graph:
                self._graph[key] = {nodeName: dictConnectedNodesAndWeight[key]}
            else:
                self._graph[key].update({nodeName: dictConnectedNodesAndWeight[key]})

    def dijkstrasAlgorithm(self, sourceNode):
        # Initialisation

        unvisitedNodes = self.getNodes()
        if sourceNode not in unvisitedNodes:
            return "not in the graph"

        # {Node : Previous node}
        previousNodesDict = {sourceNode: sourceNode}

        # {Node : shortest known path from source node}
        shortestPathToNodeDict = {}
        # Initialise the shortest path dictionary
        for node1 in unvisitedNodes:
            shortestPathToNodeDict[node1] = 9999
        shortestPathToNodeDict[sourceNode] = 0

        # While nodes in previous node
        while unvisitedNodes:
            # ---------------------------------------------------------------------------------
            # Dijkstra's starts at each node with the lowest distance from start per iteration
            # So finds the node with the (current) lowest distance from start/shortestPath and assigns currentMinNode
            currentMinNode = None
            for possibleNextMinNode in unvisitedNodes:
                if currentMinNode is None:
                    currentMinNode = possibleNextMinNode
                elif shortestPathToNodeDict[possibleNextMinNode] < shortestPathToNodeDict[currentMinNode]:
                    currentMinNode = possibleNextMinNode
            # ---------------------------------------------------------------------------------
            # Gives the connected nodes and weights of the next node to be selected for the algorithm
            # (the node with the (current) lowest shortestPath)
            connectedNodesAndWeight = self._graph[currentMinNode]

            # Apply the algorithm to try to find a faster route for connected unvisited nodes

            # For every node connected to this base node
            for connectedNode in connectedNodesAndWeight:
                # Only consider unvisited nodes
                if connectedNode in unvisitedNodes:
                    newShortestPath = shortestPathToNodeDict[currentMinNode] + connectedNodesAndWeight[connectedNode]
                    # If the detour through the current min node is faster than what it currently is
                    if newShortestPath < shortestPathToNodeDict[connectedNode]:
                        # Then make that the new shortest path
                        shortestPathToNodeDict[connectedNode] = newShortestPath
                        # And assign the previous node to the node which the detour passed from
                        previousNodesDict[connectedNode] = currentMinNode

            # Now the iteration is finished the node is fully traversed
            unvisitedNodes.remove(currentMinNode)
        return previousNodesDict, shortestPathToNodeDict

    def isConnected(self):
        return nx.is_connected(nx.Graph(self._graph))

    def plotGraph(self, coordinateDict=None):
        G = nx.Graph()
        if coordinateDict is None:
            x = 10
            y = 10
            for node in self._graph:
                x = x + random.randint(-4, 4)
                y = x + random.randint(-4, 4)
                G.add_node(node, pos=(x, y))
        else:
            for node in self._graph:
                G.add_node(node, pos=(coordinateDict[node][0], 340 - coordinateDict[node][1]))

        for baseNode in self._graph:
            # make a dict_items object
            for compNode, weight in self._graph[baseNode].items():
                G.add_edge(baseNode, compNode, weight=weight)

        # nodeCoordDict = a dictionary of nodes and their coordinates in the required format
        nodeCoordDict = nx.get_node_attributes(G, 'pos')
        # edgesDict = another dictionary of two nodes and their weight (with no repeats)
        edgesDict = nx.get_edge_attributes(G, 'weight')

        nx.draw(G, nodeCoordDict, with_labels=True, font_weight='bold', node_size=500, node_color='skyblue',
                font_size=8)
        nx.draw_networkx_edge_labels(G, nodeCoordDict, edge_labels=edgesDict)
        plt.show()


if __name__ == "__main__":
    weightedGraph1 = {
        'A': {'B': 1, 'C': 2},
        'B': {'A': 1, 'C': 3},
        'C': {'A': 2, 'B': 3}
    }
    graph1 = SimpleWeightedGraph(weightedGraph1)
    #graph1.addNode("D", {"A": 6, "E": 5, "C": 1})
    #graph1.addNode('E', {'I': 4, 'F': 3})
    #graph1.addNode('I', {'E': 4, 'H': 6})
    #graph1.addNode('G', {'E': 4, 'H': 6})
    print(graph1.getGraph())
    print(graph1.dijkstrasAlgorithm("A"))
    graph1.plotGraph()