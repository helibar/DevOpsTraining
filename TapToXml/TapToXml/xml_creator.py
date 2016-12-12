import pprint
import os
from xml.etree.ElementTree import *
from xml.etree import ElementTree
from xml.dom import minidom


def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def build_testsuitXml(tss, program,tests,failures,errors):
    testsuite = SubElement(tss, 'testsuite')
    att = ('tests', 'failures', 'errors')
    testsuite.set('name', program)
    dic = {'tests':tests, 'failures':failures, 'errors':errors}
    for a in att:
        if a in dic:
            testsuite.set(a,dic[a])
    return testsuite


def build_testcaseXml(ts, id, description):
    testcase = SubElement(ts, 'testcase')
    testcase.set('name','#'+str(id)+' '+description)
    return testcase

def build_failureXml(tc, yaml_buffer):
    failure = SubElement(tc, 'failure')
    failure.text = format_failure(yaml_buffer)

def format_failure(yaml_buffer):
    text = '\n';
    for line in yaml_buffer:
        text += '\t\t'+ line
    text +='          \n      '
    return text;


def generate_xml(tp,xml_name):
    testsuites = Element('testsuites')
    
    for program in tp.programs:
        testsuite=build_testsuitXml(testsuites, program.name,program.tests_num, program.failure_num, program.error_num)
        for test in program.tests:
            testcase = build_testcaseXml(testsuite, test.id, test.description)
            if test._yaml_buffer is not None:
                build_failureXml(testcase, test._yaml_buffer)
   
    write_xml (prettify(testsuites),xml_name)

def write_xml(xml_input, xml_name):
    print('Creating xml file...')
    name=xml_name
    extension="xml"

    try:
        name=name+"."+extension
        if os.path.exists(name):
            print(name + " file already exist.")
        file=open(name,'a')
        file.write(xml_input)
        file.close()
        print(name + " file has been created!")
    except:
            print("error occured.")
            sys.exit(0)