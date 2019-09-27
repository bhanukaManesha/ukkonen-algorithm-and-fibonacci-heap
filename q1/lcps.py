########################################################################################################################
# Name - Bhanuka Manesha Samarasekara Vitharana Gamage
# Student ID - 28993373
# Monash Email - bsam0002@student.monash.edu

# Question 1 -  Longest Common Prefix with Ukkonen Implementation
########################################################################################################################
#
# References
#
# Roy, T (2016), Suffix tree [Source code] https://github.com/mission-peace/interview/blob/master/src/com/interview/suffixprefix/SuffixTree.java
#
########################################################################################################################

# Importing the files
import argparse as ap

# Define the size of the alphabet
SIZE_OF_ALPHABET = 63

def get_alphanumeric_order(letter):
    """
    Convert a given alphanumeric character in to ascii format
    :param letter: alphanumeric letter
    :return: ascii value for the input character
    """

    # Convert to ascii
    ascii = ord(letter)

    # Convert the dollar sign to ascii
    if ascii == 36:
        return 62
    # Convert numeric part to ascii
    elif ascii >= 48 and ascii <= 57:
        return ascii - 48
    # Convert upper case characters to respective index value
    elif ascii >= 65 and ascii <= 90:
        return ascii - 55
    # Convert lower case characters to respective index value
    elif ascii >= 97 and ascii <= 122:
        return ascii - 61
    # Return error of non alpha numeric letter is provided
    else:
        raise Exception("Unsupported Character")

def get_string(order):
    """
    Convert a given alpahnumeric character in to ascii format
    :param letter: alphanumeric letter
    :return: ascii value for the input character
    """

    # Convert the dollar sign to ascii
    if order == 62:
        return chr(36)
    # Convert numeric part to ascii
    elif order >= 0 and order <= 9:
        return chr(order + 48)
    # Convert upper case characters to respective index value
    elif order >= 10 and order <= 35:
        return chr(order + 55)
    # Convert lower case characters to respective index value
    elif order >= 36 and order <= 61:
        return chr(order + 61)
    # Return error of non alpha numeric letter is provided
    else:
        raise Exception("Unsupported Order")


class Node:
    '''
    Node class for each suffix node in the suffix tree
    '''
    def __init__(self, start, end):
        '''
        Method to initialize the node
        :param start: start index of the node
        :param end: end index of the node
        '''
        # Set the start and end value to the values passed by the input
        self.start = start
        self.end = end

        # Create a list based on the size of the alphabet
        self.children = [None] * SIZE_OF_ALPHABET

        # Initialize the suffix link to None
        self.suffix_link = None

    def __str__(self):
        '''
        Method to print out each node in the suffix tree
        :return:
        '''
        edges = " ["
        for i in range(len(self.children)):
            if self.children[i] != None:
                edges += get_string(i) + "::" + str(self.children[i]) + " "
        edges += "] "

        return str(self.start) + " -> " + str(self.end) + "" + str(edges)


class GlobalI():
    '''
    Wrapper class to generate the global i for the global i implementation trick
    '''
    def __init__(self,value):
        '''
        Initialize the global variable using the value passed in as the initial value
        :param value: initial value to be stored in the global variable
        '''
        self.i = value

    def __str__(self):
        '''
        Return the i value as a string
        :return: string with value
        '''
        return str(self.i)

class ActivePointers():
    '''
    Class to maintain the active pointers to aid in ukkonen implementation
    '''
    def __init__(self, node, edge, length):
        '''
        Method to initalize the Active Pointers
        :param node: reference to the active node
        :param edge: reference to the active edge
        :param length: value of the active length
        '''
        self.active_node = node
        self.active_edge = edge
        self.active_length = length

def ukkonen(text):
    '''
    Method to create the suffix tree using ukkonnen's algorithm
    :param text: the string that neeed to be converted to the suffix tree
    :return: suffix tree for the given text
    '''

    # Add the dollar sign to the text
    text += "$"

    # Initialize the Global I to 1
    global_i = GlobalI(-1)

    # Initialize the j to zero
    j = 0

    # Initialize the root node with start index 0 and end index as the global i
    root = Node(0, global_i)

    # Initialize the active pointers
    active_pointers = ActivePointers(root, -1, 0)


    # Loop from global i 0 to end of text
    while global_i.i < len(text) - 1:

        # Resetting the last created node
        last_created_node = None

        # Incrementing the global i which will in turn apply rule 1
        global_i.i += 1

        # Loop until all extensions are done
        while j <= global_i.i:

            # Check if the active length is 0
            if active_pointers.active_length == 0:

                # Get the child from the active node
                child = active_pointers.active_node.children[get_alphanumeric_order(text[global_i.i])]

                # Check if the child node is not None
                if child != None:

                    # Then update the active edge to the start index of the current node
                    active_pointers.active_edge = child.start

                    # Increase the active length by one
                    active_pointers.active_length+=1

                    # Break from the inner loop
                    break

                else:

                    # Create the new node
                    # active_pointers.active_node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)
                    root.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    # Increase j by 1
                    j += 1

            else:

               # Get the next character after
                next_char  = skip_count(global_i.i, text, active_pointers)

                if next_char == -1 :
                    # Rule 2a extension
                    # If no path exist from the node
                    # Get the current node
                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    # Create a new node from the current node
                    node.children[get_alphanumeric_order(text[global_i.i])] = Node(global_i.i, global_i)

                    # If there is a last created node, then update the suffix link
                    if last_created_node != None:
                        last_created_node.suffix_link = node

                    # Set the current node as the last created node
                    last_created_node = node

                    # If the current node is not root
                    if active_pointers.active_node != root:
                        # Jump to the next active node using the suffix link
                        active_pointers.active_node = active_pointers.active_node.suffix_link

                    else:
                        # Else increase the active edge
                        active_pointers.active_edge = active_pointers.active_edge + 1

                        # Decrease the active length
                        active_pointers.active_length -= 1

                    # Increment the j
                    j += 1

                    # Go to the next iteration
                    continue

                # If the next character is the last letter for the phase
                if next_char == text[global_i.i]:

                    # If the last created node is not none, then update the suffix link
                    if last_created_node != None:
                        last_created_node.suffix_link = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    # Get the active node
                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    # Calculate the length of the text for the node
                    difference = node.end.i - node.start

                    # If the difference is less than the active length
                    if difference < active_pointers.active_length:

                        # Update the active node to the next node
                        active_pointers.active_node = node

                        # Update the active length
                        active_pointers.active_length = active_pointers.active_length - difference

                        # Update the active edge
                        active_pointers.active_edge = node.children[get_alphanumeric_order(text[global_i.i])].start

                    else:

                        # Update the active edge
                        active_pointers.active_length += 1

                    # Show stopper
                    break

                else:

                    # Get the next node
                    node = active_pointers.active_node.children[get_alphanumeric_order(text[active_pointers.active_edge])]

                    # Get the old start from the node
                    old_start = node.start

                    # Increment the current node start using the active length
                    node.start = node.start + active_pointers.active_length

                    # Create new middle node
                    new_middle_node = Node(old_start, GlobalI(old_start + active_pointers.active_length - 1))

                    # Create new leaf node
                    new_leaf_node = Node(global_i.i, global_i)

                    # Add the current node as middle node child
                    new_middle_node.children[get_alphanumeric_order(text[new_middle_node.start + active_pointers.active_length])] = node

                    # Add the leaf node in to the new intermediate node
                    new_middle_node.children[get_alphanumeric_order(text[global_i.i])] = new_leaf_node

                    # Add the active pointers
                    active_pointers.active_node.children[get_alphanumeric_order(text[new_middle_node.start])] = new_middle_node

                    # If there is a last created node, then update the suffix link
                    if last_created_node != None:
                        last_created_node.suffix_link = new_middle_node


                    # Set the new node for suffix link
                    last_created_node = new_middle_node

                    # Default the suffix link to root
                    new_middle_node.suffix_link = root

                    # If active node is not roor, go to the next active node using the suffix link
                    if active_pointers.active_node != root:
                        active_pointers.active_node = active_pointers.active_node.suffix_link

                    else:
                        # Update the active edge
                        active_pointers.active_edge = active_pointers.active_edge + 1

                        # Update the active length
                        active_pointers.active_length -= 1

                    # Increment j
                    j += 1

    # Return the tree
    return root

def skip_count(i, text, active):

    # Get the next node to traverse down the tree
    node = active.active_node.children[get_alphanumeric_order(text[active.active_edge])]

    # Get the length of the text in the node
    difference = node.end.i - node.start

    # If the difference is greater than the active length
    if difference >= active.active_length:

        # If the difference is more, then the extension is in this node
        return text[active.active_node.children[get_alphanumeric_order(text[active.active_edge])].start + active.active_length]

    # If the length of the string + 1 is the active length
    if difference + 1 == active.active_length:

        # Then check if the next node exist
        if node.children[get_alphanumeric_order(text[i])] != None:

            # Then return the character
            return text[i]

    else:
        # If the length of the string is more, then traverse to the next node
        # Update the active node
        active.active_node = node

        # Update the active length
        active.active_length = active.active_length - difference - 1

        # Update the active edge
        active.active_edge = active.active_edge + difference + 1

        # Use skip count on the next node
        return skip_count(i,text, active)

    # Return -1 if there exist no path to the next node
    return -1


def lcps(root, index1, index2, text):
    '''
    Method used to calculate the longest common prefix
    :param root: The root node of the suffix tree
    :param index1: The start index of the first prefix
    :param index2: The start index of the second prefix
    :param text: The input string
    :return: the length of the longest common prefix
    '''

    # Set the count to zero
    count = 0

    # If the first two characters are diffrent, then return 0
    if text[index1] != text[index2]:
        return 0

    # Set the current node as the child with the first index of the root
    current_node = root.children[get_alphanumeric_order(text[index1])]

    # Set the calculate the length of the text in the node
    difference = current_node.end.i - current_node.start + 1

    # Increase the count since all of the string should match if the first index match
    count += difference

    # Check if the indexes are less than the text and the next character is the same
    while index1 + count < len(text) and index2 + count < len(text) and text[index1 + count] == text[index2 + count]:

        # Update the current node to the child of the next edge
        current_node = current_node.children[get_alphanumeric_order(text[index1 + count])]

        # Calculate the length of the edge
        difference = current_node.end.i - current_node.start + 1

        # Increase the count
        count += difference

    # Return the count
    return count


def read_input():
    """
    method used to read the arguments from the command line and read the text and pattern files
    :return: the arguments
    """

    # create a parser object
    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline
    parser.add_argument("string_file", help="specifies the name of the text file", type=str)
    parser.add_argument("pairs_file", help="specifies the name of the output file", type=str)

    # Get all the arguments
    arguments = parser.parse_args()

    # Get the filepath arguments
    string_file_path = arguments.string_file
    pairs_file_path = arguments.pairs_file

    # Open the files
    text_file = open(string_file_path, "r")
    pairs_file = open(pairs_file_path, "r")

    # Read the lines
    text = text_file.readlines()
    lines = pairs_file.readlines()

    # Strip the lines into an array
    lines  = [row.strip() for row in lines]

    # Extract the pairs of indexes from the row
    pairs = []
    for row in lines:

        # Tab doesnt work
        # row = row.split("\t")

        # Split each sub line
        row = row.split("   ")

        # Append the splitted values into the pairs list
        pairs.append(row)


    # Close the files
    text_file.close()
    pairs_file.close()

    # Return the strings
    return text[0], pairs

def write_output(output, output_path):
    """
    This method is used to write the string to the file
    :param output: the output string
    :param output_path: the path to the output file
    :return: None
    """
    output_file = open(output_path, "w")
    output_file.write(output)


if __name__ == "__main__":

    # Get the text and pattern from the file
    text, pairs = read_input()

    # Uncomment to run file directly here
    # path = "string.txt"
    # path = "input_text.txt"
    # text_file = open(path, "r")
    # text = text_file.readlines()
    # text = text[0]

    # Pass in the text while appending the $ sign
    tree = ukkonen(text)

    # Initialize the string
    write = ""

    # For all the paris in the pairs list
    for pair in pairs:

        # Calculate the longest common prefix
        lcp = lcps(tree, int(pair[0]) - 1, int(pair[1]) - 1, text)

        # Write the prefix to file
        write += pair[0] + "\t" + pair[1] + "\t" + str(lcp) + "\n"

    # Write the output to file
    write_output(write, 'output_lcps.txt')
