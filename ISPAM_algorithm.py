import numpy as np
from numpy import ndarray
from typing import Any


def init_bit_appering_and_first_position_sequences(dataset_sequences: dict[int, list[list[str]]], list_of_words: list[str]) \
        -> tuple[dict[Any, ndarray], dict[Any, ndarray], dict[Any, dict[Any, ndarray]]]:
    """

    :param dataset_sequences:
    :param list_of_words:
    :return:
    """
    appear_dict, fp_dict, bit_dict = initialise_zero_sequences(dataset_sequences, list_of_words)

    element_i = len(dataset_sequences) - 1
    for key, value in dataset_sequences.items():
        position_j = 1
        for sequence_j in value:
            for item_k in sequence_j:
                if appear_dict[item_k][element_i] == 0:
                    appear_dict[item_k][element_i] = 1

                bit_dict[key][item_k][-position_j] = 1

                if fp_dict[item_k][element_i] == 0:
                    fp_dict[item_k][element_i] = position_j
            position_j += 1
        element_i -= 1

    return appear_dict, fp_dict, bit_dict


def initialise_zero_sequences(dataset_sequences: dict[int, list[list[str]]], list_of_words: list[str]) \
    -> tuple[dict[Any, ndarray], dict[Any, ndarray], dict[Any, dict[Any, ndarray]]]:
    """

    :param dataset_sequences:
    :param list_of_words:
    :return:
    """
    appear_dict = dict()
    fp_dict = dict()
    bit_dict = dict()
    for word in list_of_words:
        appear_dict[word] = np.zeros(len(dataset_sequences))
        fp_dict[word] = np.zeros(len(dataset_sequences))
    for key, value in dataset_sequences.items():
        dict_sid = dict()
        for sequence in value:
            for item in sequence:
                if item not in dict_sid.keys():
                    dict_sid[item] = np.zeros(len(value))
            bit_dict[key] = dict_sid

    return appear_dict, fp_dict, bit_dict

def I_SPAM_algorithm():
    # L1=φ ;
# For each item k in appearing sequence table
# If 1_Count(Appeark)< min_sup, /* remove from the tables */
# For i=1 to |S|
# If Appeark(i)==1,
# Remove Bitk(i) from the bit sequence table;
# Remove the tuple [k, Appeark, FPk] from appearing
# sequence table;
# Else L1= L1 ∪ {k};
# For each item T∈ L1
# S-temp<T>= L1;
# I-temp<T>= {x | x∈ L1 ∧ x > T by lexicographic order};
# Call M_DFS(T, AppearT, FPT, S-temp<T>, I-temp<T>).
    pass
