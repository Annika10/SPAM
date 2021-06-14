from experiments.experiments_tweets import load_dataset, run_experiment, run_experiment_ispam

from matplotlib import pyplot as plt
import csv
import os

import sys
from pathlib import Path


def plot_analysis(x_list, dataset_name, xlabel):
    """
    plots the stored results
    :param x_list: values for the x-axis
    :param dataset_name: name where results are stored
    :param xlabel: label of the x-axis
    :return: None
    """
    y_spam_runtime = list()
    y_ispam_runtime = list()

    parent_path = Path(sys.path[0]).parent
    # SPAM
    with open(os.path.join(parent_path, 'results/spam_' + dataset_name + '.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            y_spam_runtime.append(row[1])
    # ISPAM
    with open(os.path.join(parent_path, 'results/ispam_' + dataset_name + '.csv')) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            y_ispam_runtime.append(row[1])

    y_spam_runtime = [float(x) for x in y_spam_runtime]
    y_ispam_runtime = [float(x) for x in y_ispam_runtime]

    plt.plot(x_list, y_spam_runtime, marker="o", label='spam')
    plt.plot(x_list, y_ispam_runtime, marker="o", label='ispam')

    # Add title and axis names
    plt.title('Runtime for ' + dataset_name + ' dataset for different supports')
    plt.xlabel(xlabel)
    plt.ylabel('runtime in seconds')
    plt.legend()

    plt.show()


def analysis_to_csv_for_saving(minSup_list, dataset, word_list, dataset_name):
    """
    runs algorithms and store results as csv
    :param minSup_list: list of min_sups for which the algorithms run
    :param dataset: dataset
    :param word_list: list of words in dataset
    :param dataset_name: name of the dataset (e.g. "small")
    :return: None
    """
    dict_sup_runtime_spam = dict()
    dict_sup_runtime_ispam = dict()
    for minSup in minSup_list:
        # SPAM
        spam_runtime = run_experiment(dataset, word_list, minSup)
        dict_sup_runtime_spam[minSup] = spam_runtime
        # ISPAM
        ispam_runtime = run_experiment_ispam(dataset, word_list, minSup)
        dict_sup_runtime_ispam[minSup] = ispam_runtime

    parent_path = Path(sys.path[0]).parent
    with open(os.path.join(parent_path, 'results/spam_' + dataset_name + '.csv'), 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        for key, value in dict_sup_runtime_spam.items():
            # write a row to the csv file
            data_list = [key, value]
            writer.writerow(data_list)

    with open(os.path.join(parent_path, 'results/ispam_' + dataset_name + '.csv'), 'w', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)

        for key, value in dict_sup_runtime_ispam.items():
            # write a row to the csv file
            data_list = [key, value]
            writer.writerow(data_list)


if __name__ == "__main__":

    # small dataset
    sorted_dataset_Cid_Tid_100, word_list_100 = load_dataset(number_of_tweets=100)
    # medium dataset
    sorted_dataset_Cid_Tid_1000, word_list_1000 = load_dataset(number_of_tweets=1000)
    # large dataset
    sorted_dataset_Cid_Tid_10000, word_list_10000 = load_dataset(number_of_tweets=10000)

    minSup_small = [5, 6, 7, 8, 9, 10]
    minSup_medium = [50, 60, 70, 80, 90, 100]
    minSup_large = [500, 600, 700, 800, 900, 1000]

    analysis_to_csv_for_saving(minSup_small, sorted_dataset_Cid_Tid_100, word_list_100, "small")
    #plot_analysis(minSup_small, "small", "minimum support")

    analysis_to_csv_for_saving(minSup_medium, sorted_dataset_Cid_Tid_1000, word_list_1000, "medium")
    #plot_analysis(minSup_medium, "medium", "minimum support")

    analysis_to_csv_for_saving(minSup_large, sorted_dataset_Cid_Tid_10000, word_list_10000, "large")
    #plot_analysis(minSup_large, "large", "minimum support")
