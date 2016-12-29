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
        tap_file = open(sys.argv[1],'r')
        xml_output_file = sys.argv[2]

        tp = TAP13()
        tp.parse(tap_file)
        generate_xml(tp, xml_output_file)

    except IndexError:
        print ("Missing TAP or xml file input arguments.")
        sys.exit()
    except FileNotFoundError:
        print("Wrong TAP file or file path")

    