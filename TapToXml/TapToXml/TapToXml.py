"""Convert tap to xml file.

Usage:

	python TapToXml.py <tap_file_name> <xml_file_name>

Using: 
    
    tap_parser.py and xml_creator.py
    
"""

import sys
from xml_creator import *
from tap_parser import *


if __name__ == "__main__":
    try:
        input = open(sys.argv[1],'r')
        output_file = sys.argv[2]

        ##FOR DBG##
        #input = open("tap_dbg",'r')
        #output_file = "xml_dbg"

    except IndexError:
        print ("Missing TAP or xml file input arguments.")
        sys.exit()

    tp = TAP13()
    tp.parse(input)
    generate_xml(tp, output_file)