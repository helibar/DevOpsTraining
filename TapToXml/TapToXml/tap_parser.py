"""Tap file parser.

Usage:
    parse(<tap_file>)

Example:
    tp=TAP13()
    tp.parse(<tap_file>)

"""

import re
from io import StringIO

RE_VERSION = re.compile(r"^\s*TAP version 13\s*$")
RE_PLAN = re.compile(r"^\s*(?P<start>\d+)\.\.(?P<end>\d+)\s*(#\s*(?P<explanation>.*))?\s*$")
RE_TEST_LINE = re.compile(r"^\s*(?P<result>(not\s+)?ok)\s*(?P<id>\d+)?\s*(?P<description>[^#]+)?\s*(#\s*(?P<directive>TODO|SKIP)?\s*(?P<comment>.+)?)?\s*$",  re.IGNORECASE)
RE_EPROGRAM = re.compile(r"^\s*#\s*(?P<explanation>.+)?\s*$") 
RE_YAMLISH_START = re.compile(r"^\s*---.*$")
RE_YAMLISH_END = re.compile(r"^.*\.\.\.\s*$")


class Test(object):
    def __init__(self, result, id, description = None, directive = None, comment = None):
        self.result = result
        self.id = id
        self.description = description
        try:
            self.directive = directive.upper()
        except AttributeError:
            self.directive = directive
        self.comment = comment
        self.yaml = None
        self._yaml_buffer = None
        self.diagnostics = []

class Program():
    def __init__(self, name, tests, tests_num, failure_num, error_num):
        self.name = name
        self.tests = tests
        self.tests_num = tests_num
        self.failure_num = failure_num
        self.error_num = error_num

class TAP13(object):
    def __init__(self):
        self.programs = []
        self.__tests_counter = 0
        self.tests_planned = None
        self.program = None
        self.tests = None
        self.failures = 0
        self.errors = 0

    def _parse(self, source):
        seek_version = True
        seek_plan = False
        seek_test = False
        seek_program = False

        in_program = False
        in_test = False
        in_yaml = False

        for line in source:
            if in_yaml:
                if RE_YAMLISH_END.match(line):
                    self.tests[-1]._yaml_buffer.append(line.strip())
                    in_yaml = False
                else:
                    self.tests[-1]._yaml_buffer.append(line)
                continue

            line = line.strip()
            
            if in_test:
                if RE_YAMLISH_START.match(line):
                    self.tests[-1]._yaml_buffer = [line+'\n']
                    in_yaml = True
                    continue

            # this is "beginning" of the parsing, skip all lines until
            # version is found
            if seek_version:
                if RE_VERSION.match(line):
                    seek_version = False
                    seek_plan = True
                    seek_test = False
                    seek_program = True
                else:
                    continue


            if seek_plan:
                m = RE_PLAN.match(line)
                if m:
                    d = m.groupdict()
                    self.tests_planned = int(d.get('end', 0))
                    seek_plan = False

                    # Stop processing if tests were found before the plan
                    #    if plan is at the end, it must be the last line -> stop processing
                    if self.__tests_counter > 0:
                        p=Program(self.program, self.tests, str(len(self.tests)), str(self.failures), str(self.errors))
                        self.programs.append(p)
                        break

            if seek_program:
                m = RE_EPROGRAM.match(line)
                if m:
                    if self.program is not None and self.tests is not None:
                        #self.programs.update({self.program:self.tests})
                        p=Program(self.program, self.tests, str(len(self.tests)), str(self.failures), str(self.errors))
                        self.programs.append(p)

                    self.program = m.string[2:]
                    in_program = True
                    seek_test = True
                    self.tests =[]
                    self.failures=0
                    self.errors=0
                    continue

            if seek_test:
                m = RE_TEST_LINE.match(line)
                if m:
                    self.__tests_counter += 1 #for all tests
                    t_attrs = m.groupdict()
                    if t_attrs['id'] is None:
                        t_attrs['id'] = self.__tests_counter
                    t_attrs['id'] = int(t_attrs['id'])
                    if t_attrs['id'] < self.__tests_counter:
                        raise ValueError("Descending test id on line: %r" % line)
                    # according to TAP13 specs, missing tests must be handled as 'not ok'
                    # here we add the missing tests in sequence
                    while t_attrs['id'] > self.__tests_counter:
                        self.tests.append(Test('not ok', self.__tests_counter, comment = 'DIAG: Test %s not present' % self.__tests_counter, description="ERROR:Test not present"))
                        self.__tests_counter += 1
                        self.errors += 1
                    if t_attrs['result'] == 'not ok':
                        self.failures +=1
                    
                    t = Test(**t_attrs)
                    self.tests.append(t)
                    in_test = True
                    continue
       
        if self.tests_planned is None:
            # TODO: raise better error than ValueError
            raise ValueError("Missing plan in the TAP source")
        sum_tests = sum(int(program.tests_num) for program in self.programs)
        if sum_tests != self.tests_planned:
            for i in range(len(sum_tests), self.tests_planned):
                self.tests.append(Test('not ok', i+1, comment = 'DIAG: Test %s not present', description="ERROR:Test not present"))
                self.errors += 1


    def parse(self, source):
        if isinstance(source, (bytes, str)):
            self._parse(source)
        elif hasattr(source, "__iter__"):
            self._parse(source)