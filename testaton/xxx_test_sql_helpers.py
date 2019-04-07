import math
import pandas as pd
import time

#This is an enhancement on the get_stats method to collect the results in a Pandas dataframe and return that dataframe
#This will allow the HTML displayer to visualise the data frame automatically
def  collect_stats(testSql, result):
    df = pd.DataFrame(columns=['SIZE', 'AVG_DIFF', 'RMSE', 'RMSE_PC', 'RAW_PC_ERROR', 'PC_DIFFERENCES'])
    size = len(result)
    for m in testSql.measurements:
        average_diff = result[m + '_diff'].mean()
        average_per_diff = result[m + '_per_diff'].mean()
        mse = result[m + '_sq_diff'].mean()
        rmse = math.sqrt(mse)
        #pc_error is the unsigned error (rmse) / true value
        pc_error = (rmse / result[m + '_source'].mean()) * 100
        non_mean_pc = (result[m + '_diff'].mean() / result[m + '_source'].mean()) * 100
        pc_differences = (len(result[result[m + '_diff'] != 0]) / float(len(result)) ) * 100
        df.loc[m] = [size, average_diff, rmse, pc_error, non_mean_pc, pc_differences]
    return df

def  get_stats(testSql, result):
    print("Size of dataset:  %d" % (len(result)))
    for m in testSql.measurements:
        average_diff = result[m + '_diff'].mean()
        average_per_diff = result[m + '_per_diff'].mean()
        mse = result[m + '_sq_diff'].mean()
        rmse = math.sqrt(mse)
        #pc_error is the unsigned error (rmse) / true value
        pc_error = (rmse / result[m + '_source'].mean()) * 100
        non_mean_pc = (result[m + '_diff'].mean() / result[m + '_source'].mean()) * 100
        pc_differences = (len(result[result[m + '_diff'] != 0]) / float(len(result)) ) * 100
        print("%10s \t Avg Diff: %10.2f \t Rmse: %10.2f \t %% Error (rmse): %5.2f%% \t  Error (mat): %5.2f%% \t PC Differences: %5.2f%%" % \
            (m, average_diff, rmse, pc_error, non_mean_pc, pc_differences))

def run_joined_test(testSql, dbEngine):
    joined = pd.read_sql_query(testSql.sql_text, dbEngine)
    for m in testSql.measurements:
        #this is calculated like this so that -ve values are mean we're under reporting and +ve value are over reporting
        joined[m + '_diff'] = joined[m + '_test'] - joined[m + '_source']
        joined[m + '_per_diff'] =  (1 - (joined[m + '_test'] / joined[m + '_source'])) * 100
        joined[m + '_sq_diff'] = (joined[m + '_source'] - joined[m + '_test']) ** 2
    print("Stats for test: %s" % testSql.description)
    print("Test executed: %s" % time.strftime("%d-%b-%y %H:%M"))
    get_stats(testSql, joined)
    return joined

#New method to work with the new HTML setup. It combines run test and run joined test
def run_test_stats(testSql, sourceEngine, testEngine=None):
    if testEngine is not None:
        source_df = pd.read_sql_query(testSql.sql_text, sourceEngine, index_col=testSql.index)
        test_df = pd.read_sql_query(testSql.sql_text, testEngine, index_col=testSql.index)
        joined = test_df.join(source_df, how='outer', lsuffix='_test', rsuffix='_source')
    else:
        joined = pd.read_sql_query(testSql.sql_text, sourceEngine)
    for m in testSql.measurements:
        joined[m + '_diff'] = joined[m + '_test'] - joined[m + '_source']
        joined[m + '_per_diff'] =  (1 - (joined[m + '_test'] / joined[m + '_source'])) * 100
        joined[m + '_sq_diff'] = (joined[m + '_source'] - joined[m + '_test']) ** 2
    #print("Stats for test: %s" % testSql.description)
    #print("Test executed: %s" % time.strftime("%d-%b-%y %H:%M"))
    stats = collect_stats(testSql, joined)
    if testEngine is not None:
        return (source_df, test_df, joined, stats)
    else:
        return (joined, stats)


def run_test(testSql, sourceEngine, testEngine):
    source_df = pd.read_sql_query(testSql.sql_text, sourceEngine, index_col=testSql.index)
    test_df = pd.read_sql_query(testSql.sql_text, testEngine, index_col=testSql.index)
    joined = test_df.join(source_df, how='outer', lsuffix='_test', rsuffix='_source')
    for m in testSql.measurements:
        joined[m + '_diff'] = joined[m + '_test'] - joined[m + '_source']
        joined[m + '_per_diff'] =  (1 - (joined[m + '_test'] / joined[m + '_source'])) * 100
        joined[m + '_sq_diff'] = (joined[m + '_source'] - joined[m + '_test']) ** 2
    print("Stats for test: %s" % testSql.description)
    print("Test executed: %s" % time.strftime("%d-%b-%y %H:%M"))
    get_stats(testSql, joined)
    return (source_df, test_df, joined)


def run_test_without_stats(testSql, sourceEngine, testEngine):
    source_df = pd.read_sql_query(testSql.sql_text, sourceEngine, index_col=testSql.index)
    test_df = pd.read_sql_query(testSql.sql_text, testEngine, index_col=testSql.index)
    joined = test_df.join(source_df, how='outer', lsuffix='_test', rsuffix='_source')
    for m in testSql.measurements:
        joined[m + '_diff'] = joined[m + '_test'] - joined[m + '_source']
        joined[m + '_per_diff'] =  (1 - (joined[m + '_test'] / joined[m + '_source'])) * 100
        joined[m + '_sq_diff'] = (joined[m + '_source'] - joined[m + '_test']) ** 2
    return (source_df, test_df, joined)


def print_zero_rows_result(all_tests_sql, detailed_results):
    i = 0
    for s in all_tests_sql:
        if detailed_results[i].empty:
            print("%2d:  %s  :  PASSED" % (i, s.name))
        else:
            print("%2d:  %s  :  FAILED  (%d)" % (i, s.name, len(detailed_results[i])))
        i += 1

def run_zero_rows(test_script, db_engine):
    detailed_results = []
    for s in test_script.all_tests_sql:
        result = pd.read_sql_query(s.sql_text, db_engine)
        detailed_results.append(result)
    assert len(test_script.all_tests_sql) == len(detailed_results)
    print_zero_rows_result(test_script.all_tests_sql, detailed_results)
    return detailed_results

#this procedure runs a single query and prints the pandas object returned
def run_single_result(testSql, dbEngine, printResult=True):
    result = pd.read_sql_query(testSql.sql_text, dbEngine)
    print("Stats for test: %s" % testSql.name)
    print("Test executed: %s" % time.strftime("%d-%b-%y %H:%M"))
    if printResult:
        print(result)
    return result

def pretty_print_panda(pd):
    for c in pd.columns:
        print("%s: %2.2f" % (c, pd[c]))