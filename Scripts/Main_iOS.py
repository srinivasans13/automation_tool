import Constants

from HelperFunctions import *
from ClassTestComponents import TestComponents
from Info_Plist_Tests import *
from OTool_Tests import *
from report_generator import *

logging_directory = Constants.LOGS_FOLDER

### Setup logging
logging.basicConfig(filename="{}/{}".format(logging_directory, "log.txt"),
                              format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%m/%d/%Y %I:%M:%S %p',
                              level=logging.DEBUG)

INFO_PLIST_PATH = f"{Constants.OUTPUT_FOLDER}/Info.plist"
APP_EXECUTABLE_PATH = f"{Constants.OUTPUT_FOLDER}/{Constants.APP_NAME}"

### parse the config file
config_xml_dict = parse_xml_to_dict("{}/{}".format(Constants.CONFIG_FOLDER, 'config_ios.xml'))

for test_name in config_xml_dict.keys():
    test_dict = config_xml_dict[test_name]
    execution_result = {}
    logging.info(f"Execution Test - {test_dict['title']}\n")

    if test_dict['verification_type'] == "plist":
        execution_result = globals()[test_dict['test_function']](INFO_PLIST_PATH)
    elif test_dict['verification_type'] == "executable":
        execution_result = globals()[test_dict['test_function']](APP_EXECUTABLE_PATH)

    logging.info(f"{execution_result[Constants.STATUS]}\n")
    logging.info(f"{execution_result[Constants.EXECUTION_OUTPUT]}\n")
    test_dict[Constants.STATUS] = execution_result[Constants.STATUS]
    test_dict[Constants.EXECUTION_OUTPUT] = execution_result[Constants.EXECUTION_OUTPUT]
    logging.info("*****************//////////********************")


generate_report(config_xml_dict,"iOS")
