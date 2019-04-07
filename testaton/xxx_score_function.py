import math
import numpy as np
from collections import namedtuple

"""
**Guide on reporting accuracy figures**

* All comparisons should be based on test - truth (i.e. planitas - actual) so that a +ve value means that planitas has a higher value and a negative means that planitas has a lower fare
* All percentages should be represented as percentages (i.e. multiplied by 100) not as fractions. This will make it easier to see and process high percentage error rates and very low error rates. Many decimal places are hard to read.
* Favour relative counts (i.e. percentages) when reporting counts (not 1000 tickets but 10% of tickets)
* Actual values are important when reporting revenue figures
* Figures should be reported to 2 significant figures
* Large numbers should be formatted with commas
"""

def score(test, truth):
    """
    A function that computes statistical difference between test and truth.
    The score function takes two arrays of real numbers (test = data that is being tested) and (truth = the ground truth that
    you're comparing against) and computes a number of statistics that measure the difference between the two data sets.
    It returns a named tuple called Score with a number of attributes of the result. This function just computes the measures.
    Pass the result to print_score to show a nice version of the score.
    """
    assert(len(truth) == len(test))
    total_size = len(truth)
    difference = test - truth
    abs_difference = abs(difference)

    rmse = math.sqrt( ((truth - test) ** 2).sum() ) / len(test)
    std_dev = np.std(truth - test)
    mean = np.mean(difference)
    median = np.median(difference)
    abs_mean = np.mean(abs(difference))

    negative = difference[difference < 0]
    positive = difference[difference > 0]
    exact = difference[difference == 0]
    #within_1_dollar = diff[(diff > -1) & (diff < 1)]   #this shows an alternative formulation
    within_1_dollar = abs_difference[abs_difference < 1]
    within_5_dollar = abs_difference[abs_difference <= 5]
    within_10_dollar = abs_difference[abs_difference <= 10]
    sum_test = sum(test)
    sum_truth = sum(truth)

    sum_diff = sum_test - sum_truth
    sum_diff_pc = (sum_diff / sum_truth) * 100

    assert(total_size == len(test))

    min_diff = min(difference)
    max_diff = max(difference)
    negative_count = len(negative)
    positive_count = len(positive)
    negative_pc = (negative_count / total_size) * 100
    positive_pc = (positive_count / total_size) * 100

    exact_count = len(exact)
    within_1_pc = (len(within_1_dollar) / total_size) * 100
    within_5_pc = (len(within_5_dollar) / total_size) * 100
    within_10_pc = (len(within_10_dollar) / total_size) * 100
    over_10_pc = 100 - within_10_pc

    assert(negative_count + positive_count + exact_count == len(difference))

    Score = namedtuple('Score', 'size rmse mean abs_mean median std_dev min max negative_pc positive_pc \
                       exact_count within_1_pc within_5_pc within_10_pc, over_10_pc sum_diff sum_diff_pc')

    return Score(total_size, rmse, mean, abs_mean, median, std_dev, min_diff, max_diff, negative_pc,
                 positive_pc, exact_count, within_1_pc, within_5_pc, within_10_pc, over_10_pc,
                 sum_diff, sum_diff_pc)


def print_score(score):
    """
    A function that takes a score namedtuple (out of the score function) and prints the result
    """
    return ('''
    SIZE:         {:15.4f}
    RMSE:         {:15.4f}\n
    AVG DIFF:     {:15.2f}
    ABS AVG DIFF: {:15.2f}
    MEDIAN:       {:15.2f}
    STD DEV:      {:15.2f}
    MIN / MAX:    {:15,.2f} / {:,.2f}\n
    UNDER-REPORT: {:15.2f}%
    OVER-REPORT:  {:15.2f}%\n
    WITHIN $ 1:   {:15.2f}%
    WITHIN $ 5:   {:15.2f}%
    WITHIN $10:   {:15.2f}%
    OVER   $10:   {:15.2f}%\n
    TOTAL DIFF:   {:15,.2f} ({:.2f}%)'''.format(score.size, score.rmse, score.mean, score.abs_mean, score.median, score.std_dev,
                                              score.min, score.max, score.negative_pc, score.positive_pc,
                                                 score.within_1_pc, score.within_5_pc, score.within_10_pc, score.over_10_pc,
                                                 score.sum_diff, score.sum_diff_pc))



"""

This function updates a dataframe with difference measures and computations directly. It has a very similar 
functionality to the score function but just updates the data frame.

Pass a map of measurements (test value - ground truth) and then the fields are created for the 
different computations. 

measure_map = {'TOTAL_FARE' : ('pas_total_fare', 'be_total_fare'), 
               'BASE_FARE' : ('pas_base_fare', 'be_base_fare'), 
               'TAX' : ('pas_tax', 'be_tax')}

If you want to calculate stats you can call calculate stats but in that case the score function (defined above)
is probably better to use.

"""
def calculate_ranges(df, measure_map):
    for field in measure_map.keys():
        (f1, f2) = measure_map[field]
        df[field + '_DIFF'] = df[f1] - df[f2]
        df[field + '_DIFF_ABS'] = abs(df[f1] - df[f2])
        df[field + '_DIFF_PC'] = (df[f1] - df[f2]) / df[f2]
        df[field + '_EXACT_MATCH'] = df[field + '_DIFF_ABS'] == 0
        df[field + '_WITHIN_1'] = df[field + '_DIFF_ABS'] <= 1
        df[field + '_WITHIN_5'] = df[field + '_DIFF_ABS'] <= 5
        df[field + '_WITHIN_10'] = df[field + '_DIFF_ABS'] <= 10
        df[field + '_GREATER_10'] = df[field + '_DIFF_ABS'] > 10

"""
A function to report stats very similar to the score function but reports from the dataframe computations.
"""
def calc_stats (df, field):
    total_count = len(df)
    exact_pc = (sum(df[field + '_EXACT_MATCH']) / total_count) * 100
    within_1_pc = (sum(df[field + '_WITHIN_1']) / total_count) * 100
    within_5_pc = (sum(df[field + '_WITHIN_5']) / total_count) * 100
    within_10_pc = (sum(df[field + '_WITHIN_10']) / total_count) * 100
    greater_10_pc = (sum(df[field + '_GREATER_10']) / total_count) * 100
    print ("Matched: %d\nExact:      %6.2f%%\n"
       "Within $ 1: %6.2f%%\nWithin $ 5: %6.2f%%\nWithin $10: %6.2f%%\nGreat  $10: %6.2f%%" % 
       (total_count, exact_pc, within_1_pc, within_5_pc, within_10_pc, greater_10_pc))