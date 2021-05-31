import numpy as np
from numpy import ndarray
from typing import Any
from SPAM_algorithm import check_support


def init_bit_appering_and_first_position_sequences(dataset_sequences: dict[int, list[list[str]]],
                                                   list_of_words: list[str]) \
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
                if appear_dict['[' + item_k + ']'][element_i] == 0:
                    appear_dict['[' + item_k + ']'][element_i] = 1

                bit_dict[key]['[' + item_k + ']'][-position_j] = 1

                if fp_dict['[' + item_k + ']'][element_i] == 0:
                    fp_dict['[' + item_k + ']'][element_i] = position_j
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
        appear_dict['[' + word + ']'] = np.zeros(len(dataset_sequences))
        fp_dict['[' + word + ']'] = np.zeros(len(dataset_sequences))
    for key, value in dataset_sequences.items():
        dict_sid = dict()
        for sequence in value:
            for item in sequence:
                if item not in dict_sid.keys():
                    dict_sid['[' + item + ']'] = np.zeros(len(value))
            bit_dict[key] = dict_sid

    return appear_dict, fp_dict, bit_dict


def I_SPAM_algorithm(appear_dict: dict[Any, ndarray], min_sup, dataset_sequences, bit_dict, fp_dict):
    list_l = list()
    appear_dict_copy = appear_dict.copy()
    for itemk, value_app in appear_dict.items():
        # remove from tables
        if one_count(value_app) < min_sup:
            for i in range(1, len(dataset_sequences)):
                if value_app[-i] == 1:
                    bit_dict[i].pop(itemk)
            appear_dict_copy.pop(itemk)
            fp_dict.pop(itemk)
        else:
            list_l.append(itemk)
    appear_dict = appear_dict_copy.copy()

    dict_support = dict()
    for key, value in appear_dict.items():
        if check_support(value) >= min_sup:
            dict_support[key] = check_support(value)

    i_temp_t_dict = dict()
    for item_t in list_l:
        i_temp_t = [x for x in list_l if x > item_t]
        i_temp_t_dict[item_t] = i_temp_t

    for item_t in list_l:
        s_temp_t = list_l
        i_temp_t = [x for x in list_l if x > item_t]
        # Call M_DFS(T, AppearT, FPT, S-temp<T>, I-temp<T>)
        appear_dict, fp_dict, dict_support = m_dfs(item_t, appear_dict, fp_dict, s_temp_t, min_sup, bit_dict, i_temp_t_dict, dict_support)
    return appear_dict, fp_dict, dict_support


def m_dfs(item_t, appear_dict, fp_dict, s_temp_t, min_sup, bit_dict, i_temp_t_dict, dict_support):
    appear_t = appear_dict[item_t].astype(int)

    # s-step
    for s_extension_element in s_temp_t:
        # convert to int for bitwise and
        appear_s_extension_element = appear_dict[s_extension_element].astype(int)
        approximate_appear_t_s = appear_t & appear_s_extension_element

        appear_t_s = np.zeros((len(approximate_appear_t_s)))
        fp_t_s = np.zeros((len(approximate_appear_t_s)))

        if one_count(approximate_appear_t_s) >= min_sup:
            for bit_k in range(len(approximate_appear_t_s)):

                if approximate_appear_t_s[-(bit_k + 1)] != 0:
                    fp_item_t = int(fp_dict[item_t][-(bit_k + 1)])
                    fp_s = int(fp_dict[s_extension_element][-(bit_k + 1)])

                    if fp_item_t >= fp_s:
                        bit_s_extension_element = bit_dict[bit_k + 1][s_extension_element]

                        for shifting_number in range(fp_item_t):
                            bit_s_extension_element = np.roll(bit_s_extension_element, 1)
                            bit_s_extension_element[0] = 0

                        if one_count(bit_s_extension_element) > 0:
                            list_of_ones = np.where(bit_s_extension_element == 1)
                            h = len(bit_s_extension_element) - np.max(list_of_ones)
                            appear_t_s[-(bit_k + 1)] = 1
                            fp_t_s[-(bit_k + 1)] = fp_item_t + h

                    else:
                        appear_t_s[-(bit_k + 1)] = 1
                        fp_t_s[-(bit_k + 1)] = fp_s
                else:
                    appear_t_s[-(bit_k + 1)] = 0
                    fp_t_s[-(bit_k + 1)] = 0

            if one_count(appear_t_s) >= min_sup:
                appear_dict[item_t + s_extension_element] = appear_t_s
                fp_dict[item_t + s_extension_element] = fp_t_s
                dict_support[item_t + s_extension_element] = check_support(appear_t_s)
                m_dfs(item_t + s_extension_element, appear_dict, fp_dict, s_temp_t, min_sup, bit_dict, i_temp_t_dict, dict_support)

    # i-step
    last_sequence = item_t.split("[")
    splitted_item_t = last_sequence[-1].split(',')
    i_temp_t = i_temp_t_dict['[' + splitted_item_t[-1]]

    for i_extension_element in i_temp_t:
        # convert to int for bitwise and
        appear_i_extension_element = appear_dict[i_extension_element].astype(int)
        approximate_appear_t_i = appear_t & appear_i_extension_element

        appear_t_i = np.zeros((len(approximate_appear_t_i)))
        fp_t_i = np.zeros((len(approximate_appear_t_i)))

        if one_count(approximate_appear_t_i) >= min_sup:
            for bit_k in range(len(approximate_appear_t_i)):

                if approximate_appear_t_i[-(bit_k + 1)] != 0:
                    fp_item_t = int(fp_dict[item_t][-(bit_k + 1)])
                    fp_i = int(fp_dict[i_extension_element][-(bit_k + 1)])

                    if fp_item_t == fp_i:
                        appear_t_i[-(bit_k + 1)] = 1
                        fp_t_i[-(bit_k + 1)] = fp_item_t

                    else:
                        last_sequence_1 = item_t.split("[")
                        splitted_item_t_1 = last_sequence_1[-1].split(',')
                        last_item = splitted_item_t_1[-1][:-1]
                        last_item_bit = bit_dict[bit_k + 1]['[' + last_item + ']'].astype(int)
                        i_extension_element_bit = bit_dict[bit_k + 1][i_extension_element].astype(int)
                        and_bit = last_item_bit & i_extension_element_bit

                        if one_count(and_bit) > 0:
                            shifting_no = fp_item_t - 1
                            for shifting_number in range(shifting_no):
                                and_bit = np.roll(and_bit, 1)
                                and_bit[0] = 0

                            if one_count(and_bit) > 0:
                                list_of_ones = np.where(and_bit == 1)
                                h = len(and_bit) - np.max(list_of_ones)
                                appear_t_i[-(bit_k + 1)] = 1
                                fp_t_i[-(bit_k + 1)] = shifting_no + h

                else:
                    appear_t_i[-(bit_k + 1)] = 0
                    fp_t_i[-(bit_k + 1)] = 0

            if one_count(appear_t_i) >= min_sup:
                str_index = item_t[:-1] + ',' + i_extension_element[1:]
                appear_dict[str_index] = appear_t_i
                fp_dict[str_index] = fp_t_i
                dict_support[str_index] = check_support(appear_t_i)
                m_dfs(str_index, appear_dict, fp_dict, s_temp_t, min_sup, bit_dict, i_temp_t_dict, dict_support)

    return appear_dict, fp_dict, dict_support


def one_count(array):
    array_ones = np.where(array == 1)
    return np.size(array_ones)
