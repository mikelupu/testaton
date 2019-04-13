import argparse
from .tests_processor import process_connections, process_datasets, process_tests


def main(args=None):

    parser = argparse.ArgumentParser(description='Test file')

    parser.add_argument('test_file', action='store', type=str,
                        help='The JSON file defining the tests')

    args = parser.parse_args()

    import json
    with open(args.test_file, 'r') as read_file:
        definition = json.load(read_file)

    connection_dict = process_connections(definition['connections'])
    datasets_dict = process_datasets(
        connection_dict, definition['data-definitions'])
    tests_dict = process_tests(datasets_dict, definition['tests'])

    for t in tests_dict:
        print(tests_dict[t].sql)
        tests_dict[t].execute()

    print(connection_dict)
    print(datasets_dict)
    print(tests_dict)

    # TODO this is breaking the call
    dt.publish()
