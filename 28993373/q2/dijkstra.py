########################################################################################################################
# Name - Bhanuka Manesha Samarasekara Vitharana Gamage
# Student ID - 28993373
# Monash Email - bsam0002@student.monash.edu

# Question 2 -  Dijkstra algorithm using Fibonacci Heap
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

                # Check if the priority of the other node is less than the pointer node
                if other_node.priority < pointer_node.priority:

                    # Then merge pointer node with other node
                    pointer_node = self.merge(pointer_node, other_node)

                # If the priority of the other node is more than the pointer node
                elif other_node.priority > pointer_node.priority:

                    # Then merge the other node with the pointer node
                    pointer_node = self.merge(other_node, pointer_node)

                # else if the priority is the same
                else:
                    # merge other node with pointer node
                    pointer_node = self.merge(other_node, pointer_node)

                    # if the next min after merging, is either the other node or the pointer node, then update it to be
                    # the pointer node
                    if next_min == other_node or next_min == pointer_node:
                        next_min = pointer_node

                # Set the item of A in index degree to None
                A[degree] = None

                # Increase the degree by 1
                degree += 1

            # Update the A array to the next pointer node
            A[pointer_node.degree] = pointer_node

            # If the pointer node is less than the priority of the next min and its not the current min
            #  then update the next min to the pointer node
            if pointer_node.priority < next_min.priority and pointer_node != self.min:

                # update the next min
                next_min = pointer_node

            # Point the pointer node to the sibling
            pointer_node = pointer_node.right

            # If the pointer node is the min, then break from the loop
            if pointer_node == self.min:
                break

        # return the next min
        return next_min


    def remove_parent(self, node):
        '''
        method to remove the parent reference of a given list of child nodes
        :param node: the child node which the parent needs to be removed
        :return: None
        '''
        # If the node is not none, then perform removal
        if node != None:

            # Remove all the links to the removed parent
            if node != None:
                # Update the current to the node
                current = node

                # remove parenets until all the parents of the siblings are removed
                while True:

                    # Set the parent to None
                    current.parent = None

                    # Set the current to the sibling
                    current = current.right

                    # if the current node is the starting child, the break
                    if current == node:
                        break

        # return None
        return


    def merge(self, child, parent):
        '''
        method used to merge two subtree, the child will be merged as a child of the parent
        :param child: the node with higher priority value
        :param parent: the node with lower priority value
        :return: the parent node after merging the two trees
        '''

        # if there are more than one child in the tree
        if child.right != child:

            # then remove the pointer from the left sibling to the right sibling
            child.left.right = child.right
            child.right.left = child.left
            child.left = child
            child.right = child

            # Update the parent of the child
            child.parent = parent

            # If the parent has other children
            if parent.child != None:

                # Add the child node to the child list
                child.left = parent.child
                child.right = parent.child.right
                parent.child.right.left = child
                parent.child.right = child

            else:
                # If the parent does not have children, then set child
                parent.child = child

            # Increase the degree of the parent
            parent.degree += 1

            # Set the child mark as false
            child.mark = False

        # return the reference to parent
        return parent


    def decrease_key(self, id, value):
        '''
        method used to decrese key of the node
        :param id: the unique id to be used for O(1) access of the lookup table
        :param value: the value the node should be updated to
        :return: None
        '''

        # Get the reference to the node with O(1) time
        currentNode = self.look_up[id]


        # If the priority of the parent is less than the new value, then update the node without changing anything
        # Case 1
        if currentNode.parent != None and currentNode.parent.priority < value:

            # Set the new value to the current node
            currentNode.priority = value

        # If the parent value is higher than the updated value
        elif currentNode.parent != None:

            # Set the new value to the current node
            currentNode.priority = value

            # Case 2a
            # Get the parent mark
            parent_mark = currentNode.parent.mark

            # Promote the currrent node to the root list
            self.promote_to_root(currentNode)

            # If the current updated node is less than self.min, then update the reference
            if currentNode.priority < self.min.priority:
                self.min = currentNode

            # Case 2b
            # If the parent is also marked before, then promote the parent to the root while parent is not marked
            while parent_mark == True:

                # Update the current node to the parent
                currentNode = currentNode.parent

                # Check if the parent is not None
                if currentNode.parent != None:

                    # Get the parent mark
                    parent_mark = currentNode.parent.mark

                else:

                    # If the parent is none, then set the parent mark to false
                    parent_mark = False


                # Move the parent also to the root
                self.promote_to_root(currentNode)


        else:

            # If the current node is in the root, then update the value
            currentNode.priority = value

            # If the current node priority is less than the current minimum, update it
            if currentNode.priority < self.min.priority:
                self.min = currentNode



    def promote_to_root(self, node):
        '''
        method to promote the node the root list
        :param node: the node to be sent to the root list
        :return: none
        '''

        # If the parent is not a root node, then update the parent mark
        if node.parent.parent != None:

            # Set the parent as true
            node.parent.mark = True

        # If the child of the parent is not the node
        if node.parent.child == node:

            # If there is only one child
            if node.left == node:

                # set the child to none
                node.parent.child = None

            else:
                # set the child reference to the next sibling
                node.parent.child = node.left

        # If there are other children, then update the pointers
        if node.left != node:
            node.left.right = node.right
            node.right.left = node.left

        else:
            # If no siblings, set the references to None
            node.left = None
            node.right = None

        # Set the parent of the node to none
        node.parent = None

        # promote the node to the left of the current min
        self.min.left.right = node
        node.left = self.min.left
        self.min.left = node
        node.right = self.min

        # unmark the node
        node.mark = False


class Node:
    '''
    Node class for each node in the Fibonacci Heap
    '''
    def __init__(self, priority, data, left, right):
        '''
        Method to initialize the node
        :param priority: priority of the node
        :param data: payload of the node
        :param left: reference to the left sibling
        :param right: reference to the right sibling
        '''

        # initialize the parent to None
        self.parent = None

        # initialize the references to the left and right nodes
        self.left = left
        self.right = right

        # initialize the child to none
        self.child = None

        # set the priority
        self.priority = priority

        # set the payload
        self.data = data

        # set the degree to zero
        self.degree = 0

        # set the initial mark to false
        self.mark = False

    def __str__(self):
        '''
        method to return the node as a string
        :return: string of the node
        '''
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
        '''
        count the number of children by traversing for debugging the node for correct pointers
        *** used only for debugging
        :return: number of children
        '''
        children_count = 0

        if self.child != None:
            current = self.child
            children_count += current.count_all_children()
            current = current.right
            while current != self.child :
                children_count += current.count_all_children()
                current = current.right

        return children_count + 1




def shortest_path(graph,source_vertex_id,total_vertices):
    """
    Find the shortest path from the source to all the other vertexes
    :param graph:the graph to search for the shortest path
    :param source_vertex_id:the vertex id for the source
    :param total_vertices:the total number of vertices in the graph
    :return:the shortest distance for all the nodes from the source
    """

    # initialize the cost array tot he size of the target
    cost_array = [-1] * (total_vertices + 1)

    # Create an array with all the vertices and initialize it with -2
    visited = [-2] * (total_vertices + 1)

    # Initialize the fibonacci heap
    fibonacci_heap = FibonacciHeap(graph.total_vertices)

    # Add the source vertex with a priority of 0
    fibonacci_heap.insert(source_vertex_id, 0, graph.get_vertex(source_vertex_id))

    # Loop until the priority queue is empty
    while len(fibonacci_heap) != 0:

        # Get the reference to the min of the heap and the cost
        (u_cost, u_vertex) = fibonacci_heap.extract_min()

        # update the cost array to the minimum cost
        cost_array[u_vertex.id] = u_cost

        # Assigning -1 to the vertex class to signify that it is visited
        visited[u_vertex.id] = -1

        # Go through each edge of the vertex
        for edge in u_vertex.edges:

            # If the vertex is already visited
            if visited[graph.get_vertex(edge.edgeTo).id] == -1:

                # then just skip
                pass

            # if the vertex is not visited
            else:

                # get the reference to the next vertex
                next_vertex = graph.get_vertex(edge.edgeTo)

                # if the vertex was never added
                if fibonacci_heap.look_up[next_vertex.id] == -2:

                    # add the node to the fibonacci heap, with the calculate distance
                    fibonacci_heap.insert(next_vertex.id, u_cost + edge.edgeWeight, next_vertex)

                else:

                    # if the heap already has the node, then access the lookup table and get the distance
                    v_distance = fibonacci_heap.look_up[next_vertex.id].priority

                    # if the current distance is less than the distance in the heap
                    if v_distance > u_cost + edge.edgeWeight:

                        # Relaxing the vertex by decreasing the key using the reference gained from the lpook up table
                        fibonacci_heap.decrease_key(next_vertex.id, u_cost + edge.edgeWeight)

    # if all the paths are visited, then return the cost array
    return cost_array

def test(test_file_path, actual_result_path):
    '''
    method used to test whether the actual result matches the generated result
    *** only for debugging purposes
    :param test_file_path:
    :param actual_result_path:
    :return:
    '''

    # Open the file
    test_file = open(test_file_path)
    actual_result_file = open(actual_result_path)

    # Create the test array with the test results
    # O(E)
    test_arr = []
    for line in test_file:
        line = line.strip()
        line = line.split("\t")
        test_arr.append(line)

    # Create the actual array with the actual results
    actual_arr = []
    for line in actual_result_file:
        line = line.strip()
        line = line.split("\t")
        actual_arr.append(line)

    # min = [0,10000]

    # set the count to zero
    count = 0

    # count the total mismatches
    for i in range(len(test_arr)):
        if test_arr[i] != actual_arr[i]:
            count+= 1

            # print the mismatch location
            print("mismatch at " + str(i + 1) + " " + str(actual_arr[i]))

            # if int(actual_arr[i][1]) < int(min[1]):
            #     min = actual_arr[i]

            # print(min)

    # return the count
    print(count)

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


if __name__ == "__main__":

    # Get the text and pattern from the file
    path = read_input()

    # Uncomment to run file directly here
    # path = "input_dijkstra_test.txt"
    # path = "test_input.txt"

    # create the graph with the path to the graph file
    graph = get_edges(path)

    # set the source id to 1
    source_id = 1

    # get the cost array to all the nodes
    cost_array = shortest_path(graph, source_id, graph.total_vertices - 1)

    # Convert the output array to a string to be written to file
    write = ""
    for i in range(1,len(cost_array)):
        write += str(i) + "\t" + str(cost_array[i]) + "\n"

    # Write the output to file
    write_output(write, 'output_dijkstra.txt')

    # Uncomment to check with the test file
    # test("output_dijkstra.txt","output_dijkstra_test.txt")