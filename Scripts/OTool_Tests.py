import re

from HelperFunctions import *
from RegexExpressions import *
import Constants



def cryptid_check (executable_file_path = None):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    cryptography_info = execute_shell_command(f"otool -l {executable_file_path}")
    crypto_regex = re.compile(get_cryptid_regex())
    cryptid_entries = crypto_regex.findall(cryptography_info)
    if len(cryptid_entries) == 0:
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{get_cryptid_regex()} flag not found in binary, the application is encrypted\n"
    for cryptid_entry in cryptid_entries:
        execution_result[Constants.STATUS] = Constants.FAIL
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{cryptid_entry} found. This application is not encrypted\n"
    return execution_result

def stack_smash_protection_check (executable_file_path = None):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    stack_flag_entries_output = execute_shell_command(f"otool -I -v {executable_file_path}")
    for stack_regex in get_stack_regex():
        stack_regex_entry = re.compile(stack_regex)
        stack_flag_entries = stack_regex_entry.findall(stack_flag_entries_output)
        if len(stack_flag_entries) == 0:
            execution_result[Constants.STATUS] = Constants.FAIL
            execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{stack_regex} flag not found in binary, this flag should be set for stack smash protection\n"
            continue
        for stack_flag_entry in stack_flag_entries:
            execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{stack_regex} flag found in binary. Stack smash protection is enabled\n"
            break
    return execution_result


def pie_flag_check (executable_file_path = None):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    PIE_flag_output = execute_shell_command(f"otool -vh {executable_file_path}")
    PIE_flag_regex = re.compile(get_pie_regex())
    PIE_flag_entries = PIE_flag_regex.findall(PIE_flag_output)
    if len(PIE_flag_entries) == 0:
        execution_result[Constants.STATUS] = Constants.FAIL
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{get_pie_regex()} flag not found in binary, this is required for randomizing the application objects' location in the memory to prevent remote exploitation of memory corruption vulnerabilities.\n"
        return execution_result
    for PIE_flag_entry in PIE_flag_entries:
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{PIE_flag_entry} flag found, helps in randomizing the application objects location in the memory to prevent remote exploitation of memory corruption vulnerabilities. \n"
        break
    return execution_result

def objc_release_flag_check (executable_file_path = None):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    objc_relese_output = execute_shell_command(f"otool -Iv {executable_file_path}")
    objc_release_regex = re.compile(get_objc_regex())
    objc_release_entries = objc_release_regex.findall(objc_relese_output)
    if len(objc_release_entries) == 0:
        execution_result[Constants.STATUS] = Constants.FAIL
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{get_objc_regex()} flag not found in binary, this implies that ARC is not utilized which protects applications from memory corruption vulnerabilities by moving the responsibility of memory management from the developer to the re.compiler.\n"
        return execution_result
    for objc_release_entry in objc_release_entries:
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}{objc_release_entry} found in the binary,\n"
        break
    return execution_result

def third_party_frameworks_check (executable_file_path = None):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    third_party_frameworks = execute_shell_command(f"otool -L {executable_file_path}")
    third_party_frameworks_regex = re.compile(get_third_party_frameworks_regex())
    third_party_frameworks = third_party_frameworks_regex.findall(third_party_frameworks)
    if len(third_party_frameworks) == 0:
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}No third party frameworks found.\n"
        return execution_result
    else:
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}Following are the third party frameworks found:\n"
    for third_party_framework in third_party_frameworks:
        third_party_framework = third_party_framework.replace("@executable_path/","")
        execution_result[Constants.STATUS] = Constants.FAIL
        execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}-{third_party_framework}\n"
    return execution_result


# PATH="/Users/harshith/Desktop/python/pythonFiles/tempdir/Whatsapp/Payload/WhatsApp.app/WhatsApp"
# execution_result = cryptid_check(PATH)
# print (f"cryptid  :  {execution_result}")
# execution_result = stack_smash_protection_check(PATH)
# print (f"stack_smash_protection_check  :  {execution_result}")
# execution_result = pie_flag_check(PATH)
# print (f"pie_flag_check  :  {execution_result}")
# execution_result = objc_release_flag_check(PATH)
# print (f"objc_release_flag_check  :  {execution_result}")
# execution_result = third_party_frameworks_check(PATH)
# print (f"third_party_frameworks_check  :  {execution_result}")
