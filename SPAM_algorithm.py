from anytree import Node, RenderTree
from anytree.exporter import DotExporter


def create_tree_for_sequences(ordered_list_of_words, max_size_sequence):
    # we know here the lexicographic order a < b < c < d
    # ordered_list_of_words = ['a', 'b', 'c', 'd']
    # TODO: generalize for tweets
    root = Node("empty")
    current_parent = root
    for number in range(max_size_sequence):
        for element in ordered_list_of_words:
            Node(element, parent=current_parent)
        current_parent = Node(ordered_list_of_words[number])

    # Sequence-extension


    # printing
    for pre, fill, node in RenderTree(root):
        print("%s%s" % (pre, node.name))

    # visualization
    # graphviz needs to be installed for the next line!
    # doesn't work
    # DotExporter(root).to_picture("tree.png")


if __name__ == "__main__":

    minSup = 2

    # example dataset from paper
    dataset = {
        1: [['a', 'b', 'd'], ['b', 'c', 'd'], ['b', 'c', 'd']],
        2: [['b'], ['a', 'b', 'c']],
        3: [['a', 'b'], ['b', 'c', 'd']]
    }

    ordered_list_of_words = ['a', 'b', 'c', 'd']
    create_tree_for_sequences(ordered_list_of_words, 4)
