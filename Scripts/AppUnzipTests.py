import re

from RegexExpressions import *
from HelperFunctions import *
import Constants


def check_signing_info():
    # execute the shell command to check the print the certificate contents
    # return boolean by checking if the signing key is debug key from the shell command execution output
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: "\n"}
    verification_keys = Constants.DEBUG_SIGNATURE
    original_folder_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/{Constants.ORIGINAL_FOLDER}"

    execution_output_from_shell_command = execute_shell_command(
        "keytool -printcert -file {}/META-INF/CERT.RSA".format(original_folder_path))

    if verification_keys in execution_output_from_shell_command:
        execution_result[Constants.EXECUTION_OUTPUT] += f"{verification_keys} found in signing key. App signed using a debug keystore\n"
        execution_result[Constants.STATUS] = Constants.FAIL
    else:
        execution_result[Constants.EXECUTION_OUTPUT] += f"{verification_keys} not found in signing key. App not signed using a debug keystore\n"

    return execution_result

def android_xml_content_verification():
    # read the contents of the manifest xml into a variable
    # get the regex from the regex file
    # check for each regex expression
    # fill the execution_output variable with the result of the regex matches
    # return the value
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: "\n"}
    android_manifest_xml_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/AndroidManifest.xml"

    with open(android_manifest_xml_path, 'r') as file:
        # read android manifest xml file into string variable
        android_xml_file_contents = file.read()
    verification_keys = get_manifest_xml_regex()

    for key in verification_keys.keys():
        regex_expression_variable = re.compile(verification_keys[key])

        if Constants.ANDROID_EXPORTED_KEY in key:
            component = 0
            component_name = 1
            for application_components in regex_expression_variable.findall(android_xml_file_contents):
                execution_result[Constants.EXECUTION_OUTPUT] += f"{application_components[component]} with name {application_components[component_name]} has android:exported set to true\n"
                execution_result[Constants.STATUS] = Constants.FAIL

        elif Constants.ANDROID_PROTECTION_LEVEL_KEY in key:
            permission_name = 0
            protection_level = 1
            for permission in regex_expression_variable.findall(android_xml_file_contents):
                if permission[protection_level] != Constants.ANDROID_PROTECTION_VALUE_SIGNATURE:
                    execution_result[Constants.EXECUTION_OUTPUT] += f"permission with name {permission[permission_name]} has android:protectionlevel set to {permission[protection_level]}\n"
                    execution_result[Constants.STATUS] = Constants.FAIL
        else:
            for regex_match in regex_expression_variable.findall(android_xml_file_contents):
                execution_result[Constants.EXECUTION_OUTPUT] += f"{key} set to true : {regex_match}\n"
                execution_result[Constants.STATUS] = Constants.FAIL

    if execution_result[Constants.STATUS] == Constants.PASS:
        execution_result[Constants.EXECUTION_OUTPUT] += f"No issues found in {android_manifest_xml_path}\n"

    return execution_result

def check_permissions():
    standard_android_permission_file_path = "{}/{}".format(Constants.SCRIPTS_FOLDER, "/Permissionsfile.txt")
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: ""}
    android_manifest_xml_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/AndroidManifest.xml"

    # construct regex to match the user features/permissions
    regex_string_for_matching_permissions_and_features_in_android_manifest_xml = get_permissions_regex()
    permissions_list_from_android_xml_path = re.compile(
        regex_string_for_matching_permissions_and_features_in_android_manifest_xml)

    execution_output = ""
    android_xml_file_contents = ""

    # Constants
    permission_or_feature_id = 0
    permission_or_feature_name = 1

    with open(android_manifest_xml_path, 'r') as file:
        # read android manifest xml file into string variable
        android_xml_file_contents = file.read()

    execution_result[Constants.EXECUTION_OUTPUT] += f"Dangerous permissions found :\n"
    # iterate over every permissions and feature from android manifest xml
    for permission_or_feature in permissions_list_from_android_xml_path.findall(android_xml_file_contents):

        with open(standard_android_permission_file_path, 'r') as standard_android_permission_file:
            # open standard permissions file and iterate over every permission in it

            for standard_android_permission in standard_android_permission_file.read().split('::'):
                # if the permission matches any entry in the permissions file, log it
                if (standard_android_permission.split(':')[permission_or_feature_id] in
                        permission_or_feature[permission_or_feature_name]):
                   execution_result[Constants.EXECUTION_OUTPUT] += f"{permission_or_feature[permission_or_feature_name].replace('android.permission','')},\n"
                   execution_result[Constants.STATUS] = Constants.FAIL
                    # skip to next iteration if entry found
                   break
            if permission_or_feature[permission_or_feature_name] not in execution_output:
                # if no matches found, log the custom permission
                execution_result[Constants.EXECUTION_OUTPUT] += f"{permission_or_feature[permission_or_feature_name].replace('android.permission','')},\n"
                execution_result[Constants.STATUS] = Constants.FAIL

    if execution_result[Constants.EXECUTION_OUTPUT] == "" :
        execution_result[Constants.EXECUTION_OUTPUT] += f"No unwanted permissions found\n"

    return execution_result


def check_smali_files():
    # check for the extension of the files if any other file is present other than that with smali extension
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: ""}
    smali_folder_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/{Constants.SMALI_FOLDER}"

    for root, subdirs, files in os.walk(smali_folder_path):
        logging.info("Checking folder : {}".format(root))

        for file in files:

            if "smali" not in file:
                execution_result[Constants.EXECUTION_OUTPUT] += f"{root}/{file} is not a smali file\n"
                execution_result[Constants.STATUS] = Constants.FAIL

    if execution_result[Constants.EXECUTION_OUTPUT] is "" :
        execution_result[Constants.EXECUTION_OUTPUT] += f"No unencrypted files found\n"

    return execution_result


def check_assets_folder():
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: "\n"}
    assets_folder_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/{Constants.ASSETS_FOLDER}"
    for assets_folder_content in os.listdir(assets_folder_path):
        absolute_path_of_assets_folder_content = "{}/{}".format(assets_folder_path,assets_folder_content)
        # check if any of them are directories

        if os.path.isdir(absolute_path_of_assets_folder_content):
            logging.info("{} is not a zip, listing contents...".format(absolute_path_of_assets_folder_content))
            sub_folder_contents = []
            # if they are walk through them and print the contents

            for root,subdirs,files in os.walk(absolute_path_of_assets_folder_content):
                if len(files) != 0:
                    if any(".js" in file or ".css" in file or ".html" in file for file in files):
                        sub_folder_contents.append("\nFiles present in directory : {}".format(root))
                        sub_folder_contents.append("{}".format('\n'.join(files)))
            logging.info("\n{}\n".format("\n".join(sub_folder_contents)))
            execution_result[Constants.EXECUTION_OUTPUT] += f"{absolute_path_of_assets_folder_content} is not encrypted/zipped\n"
            execution_result[Constants.STATUS] = Constants.FAIL

        elif os.path.isfile(absolute_path_of_assets_folder_content):
            clear_directory(Constants.TMP_FOLDER)
            # if they are not, look for zip files

            if absolute_path_of_assets_folder_content.endswith(("zip","rar","tar.gz","tar.BZ2","tar.XZ","tar")):
                # unzip the files into tmp folder
                unzip_status = unzip_to_folder(absolute_path_of_assets_folder_content,Constants.TMP_FOLDER)

                if unzip_status == Constants.ENCRYPTED or unzip_status == Constants.CORRUPT or unzip_status == Constants.NOT_A_ZIP:
                    logging.info("{} is {}".format(absolute_path_of_assets_folder_content,unzip_status))
                    execution_result[Constants.EXECUTION_OUTPUT] += f"{absolute_path_of_assets_folder_content} is encrypted\n"
                else:
                    # if unzip successful, print the contents
                    logging.info("{} unzipped, listing contents...".format(absolute_path_of_assets_folder_content))
                    sub_folder_contents = []

                    for root, subdirs, files in os.walk(Constants.TMP_FOLDER):
                        if len(files) != 0:
                            if any(".js" in file or ".css" in file or ".html" in file for file in files):
                                sub_folder_contents.append("{}".format('\n'.join(files)))
                    logging.info("\n{}\n".format("\n".join(sub_folder_contents)))
                    execution_result[Constants.EXECUTION_OUTPUT] += f"{absolute_path_of_assets_folder_content} is not encrypted\n"
                    execution_result[Constants.STATUS] = Constants.FAIL
        else:
            execution_result[Constants.EXECUTION_OUTPUT] += f"{absolute_path_of_assets_folder_content} contains individual files\n"
            logging.info("{} is individual file".format(absolute_path_of_assets_folder_content))
    return execution_result

def check_res_xml_config_file(res_config_file_path):
    # read the contents of the config.xml file into a variable
    # get the regex expressions from the regex expressions file
    # check for matches from the regex expressions file
    # return the match results
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: "\n"}

    with open(res_config_file_path, 'r') as file:
        # read config xml file into string variable
        config_xml_file_contents = file.read()
    regex_expressions = res_config_xml_regex()

    for regex_expression_key in regex_expressions.keys():
            regex_expression = re.compile(regex_expressions[regex_expression_key])

            for regex_match in regex_expression.findall(config_xml_file_contents):

                if Constants.ACCESS_ORIGIN_KEY == regex_expression_key:
                    execution_result[Constants.EXECUTION_OUTPUT] += f"{regex_match} is set for access origin\n"
                    execution_result[Constants.STATUS] = Constants.FAIL

                elif Constants.ALLOW_INTENT_KEY == regex_expression_key:

                    if Constants.ALLOW_INTENT_HTTPS == regex_match:
                        execution_result[Constants.EXECUTION_OUTPUT] += f"{regex_match} is set for https access\n"
                        execution_result[Constants.STATUS] = Constants.FAIL

                    elif Constants.ALLOW_INTENT_HTTP == regex_match:
                        execution_result[Constants.EXECUTION_OUTPUT] += f"{regex_match} is set for http access\n"
                        execution_result[Constants.STATUS] = Constants.FAIL

                elif Constants.ALLOW_INTENT_NAVIGATION_KEY == regex_expression_key:
                    execution_result[Constants.EXECUTION_OUTPUT] += f"{regex_match} is set for allowing navigation\n"
                    execution_result[Constants.STATUS] = Constants.FAIL

    return execution_result


def check_res_folder():
    # if config.xml file is present call the corresponding function
    # if network_security.xml file is present call the corresponding function
    execution_result = {Constants.STATUS: Constants.PASS, Constants.EXECUTION_OUTPUT: "\n"}
    res_folder_path = f"{Constants.APKTOOL_OUTPUT_FOLDER}/{Constants.RES_FOLDER}"

    res_config_file_path = f"{res_folder_path}/xml/config.xml"
    res_network_security_config_file_path = f"{res_folder_path}/xml/network_security_config.xml"

    if os.path.exists(res_config_file_path):
        execution_result = check_res_xml_config_file(res_config_file_path)
    else:
        execution_result[Constants.EXECUTION_OUTPUT] += f"{res_config_file_path} is not found\n"
        execution_result[Constants.STATUS] = Constants.FAIL

    if os.path.exists(res_network_security_config_file_path):
        pass
    else:
        execution_result[Constants.EXECUTION_OUTPUT] += f"{res_network_security_config_file_path} is not found\n"

    return execution_result

