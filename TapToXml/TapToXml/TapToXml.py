import sys

from xml_creator import *
from tap_parser import *


if __name__ == "__main__":
    try:
        #input = open(sys.argv[1],'r')
        #output_file = sys.argv[2]

        ##FOR DBG##
        input = open("tap_dbg",'r')
        output_file = "xml_dbg"

    except IndexError:
        print ("Missing TAP or xml file input arguments.")
        sys.exit()

    tp = TAP13()
    tp.parse(input)
    generate_xml(tp, output_file)