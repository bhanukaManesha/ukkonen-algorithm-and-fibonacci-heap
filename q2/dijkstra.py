########################################################################################################################
# Name - Bhanuka Manesha Samarasekara Vitharana Gamage
# Student ID - 28993373
# Monash Email - bsam0002@student.monash.edu

# Question 1 -  Dijkstra algorithm using Fibonacci Heap
########################################################################################################################

# Importing the libraries
import argparse as ap
import math

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

        self.visited = -2

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


class FibonacciHeap:
    '''
    Class to implement the fibonacci heap
    '''
    def __init__(self, number_of_nodes):
        '''
        Initial the root node for the fibonacci heap
        :param number_of_nodes: the number of unique inputs for the lookup table
        '''
        self.min = None
        self.count = 0

        # Create the look up table
        self.look_up = [-2] * (number_of_nodes + 1)

    def __len__(self):
        '''
        method to return the number of items in the heap
        :return: total number of nodes in the heap
        '''
        return self.count

    def __str__(self):
        '''
        method to print the fibonacci heap
        :return: return the fibonacci heap as a string
        '''
        if self.min != None:
            output = ""
            current = self.min

            output += str(current)

            if current.right != current:
                current = current.right
                while current != self.min:
                    output += "\n " + str(current)
                    current = current.right

            return output

        return ""

    def count_node(self):
        '''
        method to count the total number of nodes using traversal
        *** this method was used for test whether the node pointers are updated correctly
        :return:the total number of nodes in the heap
        '''
        if self.min != None:

            count_node = 0
            current = self.min
            count_node += current.count_all_children()

            if current.right != current:
                current = current.right

                while current != self.min:
                    count_node += current.count_all_children()
                    current = current.right

            return count_node

        return 0


    def insert(self, id, priority, data):
        '''
        method to insert new items to the fibonacci heap
        :param id: the unique id for the node, to be used for O(1) access
        :param priority: the priority to be used for the value
        :param data: the payload of the node
        :return: None
        '''

        # Create a new node using the node class
        new_node = Node(priority, data, None, None)
        new_node.left = new_node
        new_node.right = new_node

        # If the heap is empty then add the new node as the root
        if self.min == None:
            self.min = new_node
        else:

            # If there are items in the node, add the new node to the left of the current min
            new_node.left = self.min.left
            self.min.left.right = new_node
            self.min.left = new_node
            new_node.right = self.min

            # If the new node is smaller than the current min, update the min pointer
            if new_node.priority < self.min.priority:
                self.min = new_node

        # Increase the count of the heap
        self.count += 1

        # Add the new node to the loop up table for O(1) access
        self.look_up[id] = new_node

    def get_min(self):
        '''
        Method to get the reference to the minimum node
        :return: the pointer to the minimum node
        '''
        return self.min


    def extract_min(self):
        '''
        Method used to extract the minimum from the heap
        :return: (priority of the node, payload of the node)
        '''

        # Get reference to the minimum node
        minNode = self.min

        # Check of the root is none
        if self.min != None:

            # Remove the parent of each node of the roots children
            self.remove_parent(minNode.child)

            # Check if there is only one element in the list
            if self.min.right != self.min and self.min.child != None:

                # get the reference to the left sibling of the parent
                parent_sibling_left = self.min.left

                # get the reference of the sibling of the left child
                child_sibling_left = self.min.child.left

                # update the reference of the left sibling of the parent
                parent_sibling_left.right = self.min.child

                # update the reference of the left sibling of the child
                self.min.child.left = parent_sibling_left

                # Set the child of the min to none
                self.min.child = None

                # update the sibling of the left child to the min
                child_sibling_left.right = self.min

                # Update the left reference of the min of the parent to the sibling
                self.min.left = child_sibling_left

                # Set the degree of the parent to 0
                self.min.degree = 0

            # if there is only one root node with children
            elif self.min != None and self.min.child != None:

                # add the children of the root node to the root level by updating the pointers
                self.min.child.left.right = self.min
                self.min.left = self.min.child.left
                self.min.right = self.min.child
                self.min.child.left = self.min

                # Set the child of the root node to none
                self.min.child = None

                # Set the degree of the minimum to zero
                self.min.degree = 0

            # Consolidate the heap and get the reference to the next minimum element in the heap
            next_min = self.consolidate()

            # After consolidating, remove the current minimum from the heap
            if self.min.right != self.min:
                # Update the pointers
                left_sibling = self.min.left
                right_sibling = self.min.right

                left_sibling.right = right_sibling
                right_sibling.left = left_sibling

            # Check if there is only one item in the root list
            if minNode == minNode.right:

                # If yes, check whether min has children
                if minNode.child != None:
                    # If there is a child, then update the minimum to the next min
                    self.min = next_min
                else:
                    # if there are no children, then the heap is empty
                    self.min = None
            else:
                # update the minimum pointer to the next minimum
                self.min = next_min

            # Reduce the count
            self.count -= 1

        # return the minimum node priority and data
        return (minNode.priority, minNode.data)


    def consolidate(self):
        '''
        method used to consolidate the heap
        :return: the reference to the next minimum node in the heap
        '''

        # Calculate the log 2 value to determine the size of array A
        log_value = int((math.log2(self.count))) + 2

        # Create an array A with size of log
        A = [None] * log_value

        # Set the next min as the current minimum
        next_min = self.min

        # if there is more than one item in the heap
        if self.min.right != self.min:
            # update the next min to the the next item
            next_min = self.min.right

        # if there is only one item in the list, we do not need to consolidate
        if self.min == self.min.right:
            return

        # Set the pointer node to the next item in the list
        pointer_node = self.min.right

        # Loop until break
        while True :

            # Calculate the degree of the pointer node
            degree = pointer_node.degree

            # If there is an item in the index degree of array A, the we need to merge the two sub trees
            while A[degree] != None:

                # Get the reference to the other tree inside the array
                other_node = A[degree]

                # if the pointer node is the same as the other tree, break out of the loop
                if (pointer_node == other_node):
                    break

                if other_node.priority < pointer_node.priority:
                    pointer_node = self.merge(pointer_node, other_node)
                elif other_node.priority > pointer_node.priority:
                    pointer_node = self.merge(other_node, pointer_node)
                else:
                    pointer_node = self.merge(other_node, pointer_node)

                    if next_min == other_node or next_min == pointer_node:
                        next_min = pointer_node

                A[degree] = None
                degree += 1

            A[pointer_node.degree] = pointer_node

            if pointer_node.priority < next_min.priority and pointer_node != self.min:
                next_min = pointer_node

            pointer_node = pointer_node.right

            if pointer_node == self.min:
                break

        return next_min

    def remove_parent(self, node):
        '''
        method to remove the parent reference of a given list of child nodes
        :param node:
        :return:
        '''
        if node != None:
            # Remove all the links to the removed parent
            if node != None:
                current = node
                while True:
                    current.parent = None
                    current = current.right

                    if current == node:
                        break

        return

    def remove_from_circular_link_list(self, parent, children):


        if children == None:

            if parent.right != parent:
                left_sibling = parent.left
                right_sibling = parent.right

                left_sibling.right = right_sibling
                right_sibling.left = left_sibling

            return

        if parent.right != parent:
            parent_sibling_left = parent.left
            parent_sibling_right = parent.right

            child_sibling_left = children.left

            parent_sibling_left.right = parent.child
            parent.child.left = parent_sibling_left

            child_sibling_left.right = parent_sibling_right
            parent_sibling_right.left = child_sibling_left

            parent.child = None


    def merge(self, child, parent):

        if child.right != child:
            child.left.right = child.right
            child.right.left = child.left

            child.left = child
            child.right = child
            child.parent = parent

            if parent.child != None:
                child.left = parent.child
                child.right = parent.child.right
                parent.child.right.left = child
                parent.child.right = child

            else:
                parent.child = child

            # Increase the degree
            parent.degree += 1
            child.mark = False

        return parent


    def decrease_key(self, id, value):

        currentNode = self.look_up[id]

        if currentNode.parent != None and currentNode.parent.priority < value:
            currentNode.priority = value
            if currentNode.priority < self.min.priority:
                self.min = currentNode
        elif currentNode.parent != None:
            currentNode.priority = value

            # Case 2a
            parent_mark = currentNode.parent.mark

            self.promote_to_root(currentNode)

            if currentNode.priority < self.min.priority:
                self.min = currentNode

            # Case 2b
            while parent_mark == True:
                currentNode = currentNode.parent
                parent_mark = currentNode.parent.mark
                self.promote_to_root(currentNode)

        else:
            currentNode.priority = value
            if currentNode.priority < self.min.priority:
                self.min = currentNode



    def promote_to_root(self, node):

        if node.parent.parent != None:
            node.parent.mark = True


        if node.parent.child == node:
            if node.left == node:
                node.parent.child = None
            else:
                node.parent.child = node.left

        if node.left != node:
            node.left.right = node.right
            node.right.left = node.left

        else:
            node.left = None
            node.right = None

        node.parent = None


        self.min.left.right = node
        node.left = self.min.left
        self.min.left = node
        node.right = self.min

        node.mark = False


class Node:
    def __init__(self, priority, data, left, right):
        self.parent = None
        self.left = left
        self.right = right
        self.child = None

        self.priority = priority
        self.data = data

        self.degree = 0
        self.mark = False

    def __str__(self):

        children = ""
        if self.child != None:
            current = self.child
            children += str(current)
            current = current.right
            while current != self.child :
                children += str(current)
                current = current.right

        return str(self.priority) + "[" + children + " ]"

    def count_all_children(self):
        children_count = 0

        if self.child != None:
            current = self.child
            children_count += current.count_all_children()
            current = current.right
            while current != self.child :
                children_count += current.count_all_children()
                current = current.right

        return children_count + 1




def shortest_path(graph,source_vertex_id,target_vertex_id):
    """
    Find the shortest path from the source to the target vertex
    :param graph:the graph to search for the shortest path
    :param source_vertex_id:the vertex id for the source
    :param target_vertex_id:the vertex id for the target
    :return:the path and the shortest distance
    :complexity:O(ElogV)
    """

    cost_array = [-1] * (target_vertex_id + 1)


    # Create an array with all the vertices and initialize it with -2
    visited = [-2] * (target_vertex_id + 1)
    # Create an array with all the vertices and initialize it with None
    # previous  = [None]* (graph.total_vertices + 1)

    # Initialize the priority queue
    fibonacci_heap = FibonacciHeap(graph.total_vertices)

    # Add the source vertex with a priority of 0
    # vertices[source_vertex_id] = fibonacci_heap.insert(0,(source_vertex_id, None))
    fibonacci_heap.insert(source_vertex_id, 0, graph.get_vertex(source_vertex_id))

    # Loop until the priority queue is empty
    while len(fibonacci_heap) != 0:
        # Serve from the priority queue
        # O(logV)

        # Get the reference to the vertex of the graph and the cost
        (u_cost, u_vertex) = fibonacci_heap.extract_min()

        # if cost_array[u_vertex.id] == -1:
        cost_array[u_vertex.id] = u_cost

        # Assigning -1 to the vertex class to signify that it is visited
        visited[u_vertex.id] = -1

        # Go through each edge of the vertex
        # O(V)
        for edge in u_vertex.edges:

            # If the vertex is already visited
            if visited[graph.get_vertex(edge.edgeTo).id] == -1:
                pass
            else:
                next_vertex = graph.get_vertex(edge.edgeTo)

                # O(logV)
                if fibonacci_heap.look_up[next_vertex.id] == -2:

                    # O(logV)
                    fibonacci_heap.insert(next_vertex.id, u_cost + edge.edgeWeight, next_vertex)

                else:
                    v_distance = fibonacci_heap.look_up[next_vertex.id].priority
                    if v_distance > u_cost + edge.edgeWeight:
                        # Relaxing the vertex
                        fibonacci_heap.decrease_key(next_vertex.id, u_cost + edge.edgeWeight)

    # If there are no vertices
    return cost_array

def write_output(output, output_path):
    """
    This method is used to write the string to the file
    :param output: the output string
    :param output_path: the path to the output file
    :return: None
    """
    output_file = open(output_path, "w")
    output_file.write(output)


def read_input():
    """
    method used to read the arguments from the command line and read the text and pattern files
    :return: the arguments
    """

    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("graph_file", help="specifies the name of the graph file", type=str)

    # Get all the arguments
    arguments = parser.parse_args()

    # Get the filepath arguments
    graph_file_path = arguments.graph_file

    return graph_file_path

def test(test_file_path, actual_result_path):

    # Open the file
    test_file = open(test_file_path)
    actual_result_file = open(actual_result_path)

    # Loop through each line to add the edge to the graph
    # O(E)
    test_arr = []
    for line in test_file:
        line = line.strip()
        line = line.split("\t")
        test_arr.append(line)

    actual_arr = []
    for line in actual_result_file:
        line = line.strip()
        line = line.split("\t")
        actual_arr.append(line)

    # min = [0,10000]

    count = 0
    for i in range(len(test_arr)):

        if test_arr[i] != actual_arr[i]:
            count+= 1
            print("mismatch at " + str(i + 1) + " " + str(actual_arr[i]))

            # if int(actual_arr[i][1]) < int(min[1]):
            #     min = actual_arr[i]

            # print(min)

    print(count)


if __name__ == "__main__":

    # Get the text and pattern from the file
    path = read_input()

    # Uncomment to run file directly here
    # path = "input_dijkstra_test.txt"
    # path = "test_input.txt"

    graph = get_edges(path)

    source_id = 1

    cost_array = shortest_path(graph, source_id, graph.total_vertices - 1)

    # Convert the output array to a string to be written to file
    write = ""
    for i in range(1,len(cost_array)):
        write += str(i) + "\t" + str(cost_array[i]) + "\n"

    # Write the output to file
    write_output(write, 'output_dijkstra.txt')

    # Uncomment to check with the test file
    test("output_dijkstra.txt","output_dijkstra_test.txt")