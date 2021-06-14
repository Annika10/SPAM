import pydot
import os
import sys
from pathlib import Path


def create_tree_visualisation(nodes, name):
    """
    create a visualisation of the frequent sequences
    :param nodes: frequent sequences
    :return: None
    """
    dict_levels = get_dict_levels(nodes)
    dict_successors = get_dict_successors(dict_levels)

    graph = pydot.Dot('my_graph', graph_type='graph')

    root = pydot.Node('root')
    for first_nodes in dict_levels[1]:
        graph.add_edge(pydot.Edge(root, first_nodes))

    # Add nodes
    for node in nodes:
        graph.add_node(pydot.Node(node))
        # Add edges
        for successors in dict_successors[node]:
            graph.add_edge(pydot.Edge(node, successors))

    parent_path = Path(sys.path[0]).parent
    graph.write_raw(os.path.join(parent_path, 'results/tree' + name + '.dot'))
    graph.write_png(os.path.join(parent_path, 'plots/experiments/tree' + name + '.png'))


def get_dict_levels(nodes):
    """
    create a dictionary which stores the nodes of each level
    :param nodes: frequent sequences
    :return: dictionary
    """
    dict_levels = dict()
    nodes = list(nodes)
    for element in nodes:
        counter_level = element.count('[')
        counter_level = counter_level + element.count(',')
        if counter_level in dict_levels:
            old_list = dict_levels[counter_level]
            old_list.append(element)
            dict_levels[counter_level] = old_list
        else:
            dict_levels[counter_level] = [element]

    print("dict_levels", dict_levels)
    return dict_levels


def get_dict_successors(dict_levels):
    """
    create a dictionary which stores for each node it successors
    :param dict_levels: dictionary which stores the nodes of each level
    :return: dictionary
    """
    dict_successors = dict()

    level = 1
    max_level = max(dict_levels.keys())

    while level < max_level:
        for node in dict_levels[level]:
            successor_list = list()
            for child_node in dict_levels[level+1]:
                if child_node.startswith(node[:-1]):
                    successor_list.append(child_node)
            dict_successors[node] = successor_list

        level += 1

    # leaf nodes
    for node in dict_levels[max_level]:
        dict_successors[node] = list()

    print("dict_successors", dict_successors)
    return dict_successors