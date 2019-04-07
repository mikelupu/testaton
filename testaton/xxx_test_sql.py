import ast
import re

def get_list_from_string(field_content):
    field_list = ast.literal_eval(field_content)
    return field_list


class TestResult:
    """At the moment this is just a holder for a list of results. The two result types that are supported are pandas DataFrames and markdown """

    def __init__(self, r):
        """Initialise with either one result or a list of results"""
        if isinstance(r, list):
            self.results = r
        else:
            self.results = [r]


class TestScript:
    """A container for a number of TestSql objects"""

    def addFile(self, filename, airline=None, substitution_variables=None):
        """Appends the contents of the file to the current TestScript
        Keyword arguments:
        filename -- file location of script
        airline -- airline code
        substitution_variables -- the parameters used in the script
        """
        all_tests_text = []
        with open(filename, 'r') as f:
            test_sql_def = ""
            for line in f:
                if line.rstrip().upper() == '--TEST':
                    if test_sql_def != "":  # one was being collected
                        all_tests_text.append(test_sql_def)
                    test_sql_def = "--TEST\n"
                elif test_sql_def != "":
                    test_sql_def = ''.join([test_sql_def, line])
            all_tests_text.append(test_sql_def)  # append last one
            for t in all_tests_text:
                self.all_tests_sql.append(TestSql(t, airline, substitution_variables))

    def addTest(self, testSql):
        """Method to a a test directly to a script"""
        self.all_tests_sql.append(testSql)

    def getLastTest(self):
        """A handy method to return last test in list when you want to execute the last test"""
        if self.all_tests_sql != []:
            return self.all_tests_sql[-1]
        return None

    def appendResult(self, testResult):
        """Appends a TestResult object to the lists of results"""
        self.all_test_results.append(testResult)

    def __init__(self, filename=None, airline=None, substitution_variables=None, title=""):
        self.title = title
        self.all_tests_sql = []   # this should eventually be hidden !!! (keeping like this for backward competiblility)
        self.all_test_results = []
        if filename is not None:
            self.addFile(filename, airline, substitution_variables)


class TestSql:

    def __init__(self, sql_string, airline=None, substitution_variables=None):
        self.sql_text = ''
        self.index = None
        self.measurements = None
        self.substitution_variables = None
        self.airline = None
        self.type = None
        self.name = ''
        self.description = ''
        self.file_name = ''
        for line in sql_string.splitlines():
            line = line.rstrip()
            if line.startswith("--"):
                #note this method is setting variables
                self.set_field(line)
            else:
                self.sql_text = ' '.join([self.sql_text, line])

        #give preference to passed variables but otherwise use ones defined
        #in the file
        if substitution_variables is not None:
            self.substitute(substitution_variables)
            self.substitution_variables = substitution_variables
        elif self.substitution_variables is not None:
            self.substitute(self.substitution_variables)
        if airline is not None:
            self.sql_text = self.sql_text.replace('XX', airline)
            self.sql_text = self.sql_text.replace('xx', airline)
            self.airline = airline
        elif self.airline is not None:
            self.sql_text = self.sql_text.replace('XX', self.airline)

    def substitute(self, sub_variables):
        index = 1
        for v in sub_variables:
            placeholder = ":" + str(index)
            #added quotes by default. now if i have to substitute an integer
            #this will have to change
            self.sql_text = self.sql_text.replace(placeholder, "'" + v + "'")
            index += 1

    def set_field(self, line):
        regex_search = re.search(r'--([A-Z_]+)=(.*)', line)
        if regex_search == None:
            return # it's a normal comment ignore
        field = regex_search.group(1)
        field_content = regex_search.group(2)
        if field == "INDEX":
            self.index = get_list_from_string(field_content)
        if field == "MEASUREMENTS":
            self.measurements = get_list_from_string(field_content)
        if field == "DEFAULTS":
            self.substitution_variables = get_list_from_string(field_content)
        if field == "AIRLINE":
            self.airline = field_content
        if field == "TYPE":
            self.type = field_content
        if field == "TEST_NAME":
            self.name = field_content
        if field == "FILE_NAME":
            self.file_name = field_content
        if field == "DESCRIPTION":
            self.description = field_content

if __name__ == '__main__':
    c = TestSql('../sql/by_departure.sql')
    print(c.sql_text)
    print(c.index)
    print(c.measurements)
