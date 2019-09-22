


class FibonacciHeap:

    def __init__(self):
        self.min = None
        self.biggest = None
        self.count = 0

    def __len__(self):
        return self.count

    def __str__(self):
        output = ""

        output += self.traverse(self.min)

        output += "\nmin : " + str(self.min)
        return output


    def traverse(self,root):
        output = ""
        start = root
        output += str(start.key) + " "
        current = start.right
        while current != start:
            output += str(current.key) + " [left : " + str(current.left) + " right : " + str(current.right) + "]  "

            if current.child != None:
                output += self.traverse(current.child)
            current = current.right

        return output

    def insert(self, key, data):
        if self.min != None:
            newNode = Node(key, data, self.min.left, self.min)
            self.min.left.right = newNode
            self.min.left = newNode

            if newNode.key < self.min.key:
                self.min = newNode

            self.count += 1
            return newNode

        else:
            self.min = Node(key, data, None, None)
            self.min.left = self.min
            self.min.right = self.min
            self.biggest = self.min

            self.count += 1
            return self.min

    def get_min(self):
        return self.min

    def extract_min(self):
        if self.count == 0:
            return None
        elif self.count == 1:
            minNode = self.min
            self.biggest = None
            self.min = None
            self.count -= 1
            return (minNode.key, minNode.data)
        else:

            if self.min.child != None:
                minNode = self.min
                self.min.left.right = self.min.child

                self.min.child.left.right = self.min.right

                self.min.right = self.min.child.left

                self.min.child.left = self.min.left

                currentNode = self.min.child
                currentNode.parent = None
                currentNode = currentNode.right

                while currentNode != self.min.child and currentNode is not None:
                    currentNode.parent = None
                    currentNode = currentNode.right


                self.min = minNode.right

                # Biggest??
                if self.biggest == minNode:
                    self.biggest = minNode.left

            else:
                minNode = self.min
                self.min.left.right = self.min.right
                self.min.right.left = self.min.left
                self.min = self.min.left

            self.count -= 1

            if self.count > 1:
                self.consolidate()

            return (minNode.key, minNode.data)

    def consolidate(self):

        A = [None] * (self.biggest.degree + 1)

        start = self.min
        A[start.degree] = start
        current = start.right

        while True:
            temp_start = start
            while temp_start.parent != None:
                temp_start = temp_start.parent


            # print(self)
            # Update the minimum
            if current.key < self.min.key:
                self.min = current

            if current.degree > len(A) - 1:
                A.append(None)


            if A[current.degree] != None:
                otherNode = A[current.degree]
                A[current.degree] = None
                current = self.merge(current, otherNode)

            else:
                A[current.degree] = current
                if current.right == temp_start:
                    break
                current = current.right



    def merge(self, nodeA, nodeB):
        if nodeB.key < nodeA.key:
            nodeA.parent = nodeB
            nodeA.right.left = nodeB
            nodeB.right = nodeA.right


            if nodeB.child != None:

                nodeB.child.left.right = nodeA
                nodeA.left = nodeB.child.left

                nodeB.child.left = nodeA
                nodeA.right = nodeB.child

            else:
                nodeB.child = nodeA
                nodeA.left = nodeA
                nodeA.right.left = nodeB
                nodeA.right = nodeA

            nodeB.degree += 1
            return nodeB

        else:
            nodeB.parent = nodeA
            nodeA.right.left = nodeA
            nodeA.right = nodeB.right

            if nodeA.child != None:
                nodeA.child.left.right = nodeB
                nodeB.left = nodeA.child.left

                nodeA.child.left = nodeB
                nodeB.right = nodeA.child
                nodeB.right.left = nodeA
            else:
                nodeA.child = nodeB
                nodeB.left = nodeB
                nodeB.right.left = nodeA
                nodeB.right = nodeB

            nodeA.degree += 1
            return nodeA

    def decrease_key(self, nodeA, value):
        if nodeA.parent != None and nodeA.parent.key <= value:
            nodeA.key = value
        elif nodeA.parent != None:
            nodeA.key = value

            currentNode = nodeA

            # Case 2a
            parent_mark = currentNode.parent.mark
            self.promote_to_root(currentNode)

            if nodeA.key < self.min.key:
                self.min = nodeA

            # Case 2b
            while parent_mark == True:
                currentNode = currentNode.parent
                parent_mark = currentNode.parent.mark
                self.promote_to_root(currentNode)


    def promote_to_root(self, node):

        if node.parent.parent != None:
            node.parent.mark = True

        if node.parent.child == node:
            if node.left == node:
                node.parent.child == None
            else:
                node.parent.child = node.left

        node.parent = None

        node.left = node.right
        node.right = node.left

        self.min.left.right = node
        node.left = self.min.left
        self.min.left = node
        node.right = self.min

        node.mark = False


class Node:
    def __init__(self, key, data, left, right):
        self.parent = None
        self.left = left
        self.right = right
        self.child = None

        self.key = key
        self.data = data

        self.degree = 0
        self.mark = False

    def __str__(self):
        return str(self.key) + ":" + str(self.data)


class Graph:
    """
    The class for the graph
    """
    def __init__(self,N):
        """
        Initialize a graph by creating the vertices
        :param N:Total number of vertices in the graph
        :complexity : O(V) where V is the number of Vertices
        """
        self.vertices = [None]*N
        for i in range(len(self.vertices)):
            self.vertices[i] = Vertex(i)
        self.total_vertices = int(N)

    def add_edge(self,u,v,w):
        """
        Adding edges to the Graph, since it bi-directinal we add it from both the vertices
        :param u: Vertex the edge is from
        :param v:Vertex the edge is to
        :param w:Weight of the edge
        :return: None
        :complexity : O(E) where E is the number of edges
        """
        e1 = Edge(u,v,w)
        self.vertices[u].add_edge(e1)

        e2 = Edge(v,u,w)
        self.vertices[v].add_edge(e2)

    def get_vertex(self,id):
        """
        Get the vertex of the graph given an ID
        :param id:the id of the vertex
        :return:the reference to the vertex of the graph
        :complexity : O(1)
        """
        return self.vertices[id]

    def __str__(self):
        """
        Printing out the graph
        :return: string with the all the vertices and edges
        :complexity : O(V) where V is the number of Vertices
        """
        output = ""
        for vertex in self.vertices:
            output+=str(vertex) + "\n"
        return output

class Vertex:
    """
    The class for the Vertex
    """
    def __init__(self,id):
        """
        Initialize the vertex id and the edge array
        :param id: id of the vertex
        """
        self.id = id
        self.edges = []

    def add_edge(self,e):
        """
        Method to add an edge to the Vertex
        :param e: The edge that has to be added
        :return: None
        :complexity:O(1)
        """
        if e.edgeTo == e.edgeFrom :
            return

        self.edges.append(e)

    def __str__(self):
        """
        Method to print the vertex
        :return: String with the Vertex Representation
        """
        output = str(self.id) + " : "
        for edge in self.edges:
            output += str(edge)
        return output

class Edge:
    """
    The class for the Edge
    """
    def __init__(self,u,v,w):
        """
        Create an edge instance with the two edges and the weight
        :param u: The vertex where the edge is from
        :param v: The vertex where the edge is to
        :param w: The weight of the edge
        :complexity ; O(1)
        """
        self.edgeFrom = u
        self.edgeTo = v
        self.edgeWeight = w

    def __str__(self):
        """
        Method is print the edge
        :return: String with the edge representation
        :complexity: O(1)
        """
        output = "[" + str(self.edgeFrom) + "->" + str(self.edgeTo) + "-" + str(self.edgeWeight) + "] "
        return output

def get_edges(filename):
    """
    Method used to create the graph from the input file
    :param filename:Name of the file
    :return:the graph with all the edges
    :complexity:O(E)
    """

    # Open the file
    file = open(filename)

    # Get the first line and set the total
    total_vertices = file.readline()
    total_vertices.strip()

    # Initialize the graph with the total vertices plus one
    # O(V)
    graph = Graph(int(total_vertices)+1)
    # Loop through each line to add the edge to the graph
    # O(E)
    for line in file:
        line = line.strip()
        line = line.split(" ")
        # Add each edge
        # O(1)
        graph.add_edge(int(line[0]),int(line[1]),int(line[2]))

    # Return the graph
    return graph

def shortest_path(graph,source_vertex_id,target_vertex_id):
    """
    Find the shortest path from the source to the target vertex
    :param graph:the graph to search for the shortest path
    :param source_vertex_id:the vertex id for the source
    :param target_vertex_id:the vertex id for the target
    :return:the path and the shortest distance
    :complexity:O(ElogV)
    """

    # Create an array with all the vertices and initialize it with -2
    vertices = [-2] * (graph.total_vertices + 1)
    # Create an array with all the vertices and initialize it with None
    previous  = [None]* (graph.total_vertices + 1)

    # Initialize the priority queue
    fibonacci_heap = FibonacciHeap()

    # Add the source vertex with a priority of 0
    vertices[source_vertex_id] = fibonacci_heap.insert(0,(source_vertex_id, None))


    # Loop until the priority queue is empty
    while len(fibonacci_heap) != 0:
        # Serve from the priority queue
        # O(logV)
        u = fibonacci_heap.extract_min()
        # Get the reference to the vertex of the graph
        u_vertex = graph.get_vertex(u[1][0])

        # Assigning -1 to the vertex class to signify that it is visited
        vertices[u[1][0]] = -1

        # Storing the vertex id of the previous vertex for backtracking
        previous[u[1][0]] = u[1][1]

        # Check if the id of the served vertex is the target id
        if u[1][0] == target_vertex_id:
            # if so set the current vertex as the target vertex
            current = target_vertex_id
            # Create a list to hold the path to the vertex
            reversed_path = [target_vertex_id]
            # Until the source_vertex is found, loop through the previous array
            # O(V)
            while current != source_vertex_id:
                # Add the vertex to the path array
                reversed_path.append(previous[current])
                # Set the new current as the next previous
                current = previous[current]

            # O(V)
            path = [0] * len(reversed_path)

            # O(V)
            index = len(reversed_path)-1
            for item in reversed_path:
                path[index] = item
                index -= 1

            return path,u[0]

        # Go through each edge of the vertex
        # O(V)
        for edge in u_vertex.edges:
            # If the vertex is already visited
            if vertices[edge.edgeTo] == -1:
                pass
            else:
                # O(logV)
                if vertices[edge.edgeTo] == -2:
                    # O(logV)
                    fibonacci_heap.insert(u[0] + edge.edgeWeight, (edge.edgeTo, u[1][0]))

                else:
                    v_distance = vertices[edge.edgeTo][0]
                    if v_distance > u[0]+edge.edgeWeight:
                        # Relaxing the vertex
                        # O(logV)
                        fibonacci_heap.decrease_key(edge.edgeTo,u[0]+edge.edgeWeight,u[1][0])

    # If there are no vertices
    return [],0

if __name__ == "__main__":

    graph = get_edges("test.txt")
    path, cost = shortest_path(graph, 1, 0)

    print(path)
    print(cost)



    # fib = FibonacciHeap()
    #
    # # inserting
    # a = fib.insert(20,"a")
    # b = fib.insert(50,"b")
    # c = fib.insert(10,"c")
    # d = fib.insert(100,"d")
    # e = fib.insert(12,"e")
    # f = fib.insert(16,"f")
    #
    # print(fib)
    #
    # # Extract min
    # fib.extract_min()
    #
    # fib.decrease_key(d,1)
    # fib.decrease_key(b,2)
    #
    # print(fib)