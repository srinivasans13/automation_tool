from HelperFunctions import *
import Constants
import os


def check_for_declared_URL_schemes( plist_file_path=None ):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    if convert_plist_into_a_dictionary(plist_file_path)["Successful"]:
        plist_dict = convert_plist_into_a_dictionary(plist_file_path)["plist_dict"]
        if Constants.BUNDLE_URL_TYPES_KEY in plist_dict:
            bundle_url_types_array = plist_dict[Constants.BUNDLE_URL_TYPES_KEY]
            for bundle_url_type in bundle_url_types_array:
                if Constants.BUNDLE_TYPE_ROLE_KEY in bundle_url_type:
                    execution_result[Constants.EXECUTION_OUTPUT]=f"{execution_result[Constants.EXECUTION_OUTPUT]}Bundle type role is set as :{bundle_url_type[Constants.BUNDLE_TYPE_ROLE_KEY]}, for URL schemes:\n"
                for url_scheme in bundle_url_type[Constants.URL_SCHEME_NAMES_KEY]:
                    execution_result[Constants.EXECUTION_OUTPUT]=f"{execution_result[Constants.EXECUTION_OUTPUT]}-{url_scheme}\n"
                execution_result[Constants.STATUS] = Constants.FAIL
                execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}Please ensure that the URL schemes are validated in the canOpenURL app-delegate method\n"
        else:
            execution_result[Constants.EXECUTION_OUTPUT] = f"{execution_result[Constants.EXECUTION_OUTPUT]}No entries for URL schemes were found in this application"
    else:
        logging.info(f"{execution_result[Constants.EXECUTION_OUTPUT]}Unable to find the Info.plist file")

    return execution_result

################## sample call
# PATH = "/Users/harshith/Desktop/Whatsapp/Payload/WhatsApp.app/Info.plist"
# result = check_for_declared_URL_schemes(PATH)
# print (result)

def check_for_app_transport_security( plist_file_path=None ):
    execution_result = {Constants.STATUS:Constants.PASS, Constants.EXECUTION_OUTPUT:"\n"}
    if convert_plist_into_a_dictionary(plist_file_path)["Successful"]:
        plist_dict = convert_plist_into_a_dictionary(plist_file_path)["plist_dict"]
        if Constants.APP_TRANSPORT_SECURITY_KEY in plist_dict:
            app_transport_security_dict = plist_dict[Constants.APP_TRANSPORT_SECURITY_KEY]
            for security_key in Constants.APP_TRANSPORT_SECURITY_EXPECTED_VALUES.keys():
                if security_key in app_transport_security_dict:
                    if security_key == Constants.EXCEPTION_DOMAINS_KEY:
                        exception_domains = plist_dict[security_key]
                        for exception_domain in  exception_domains.keys():
                            exception_domain_subkeys_dict = exception_domains[exception_domain]
                            for exception_domain_subkey in exception_domain_subkeys_dict.keys():
                                if exception_domain_subkeys_dict[exception_domain_subkey] in Constants.APP_TRANSPORT_SECURITY_EXPECTED_VALUES[exception_domain_subkey]:
                                    execution_result[Constants.EXECUTION_OUTPUT]=f"{execution_result[Constants.EXECUTION_OUTPUT]}{exception_domain_subkey} is set to {exception_domain_subkeys_dict[exception_domain_subkey]}.\nExpected value is {Constants.APP_TRANSPORT_SECURITY_EXPECTED_VALUES[exception_domain_subkey]}"
                    else:
                        if app_transport_security_dict[security_key] != Constants.APP_TRANSPORT_SECURITY_EXPECTED_VALUES[security_key]:
                            execution_result[Constants.STATUS] = Constants.FAIL
                            execution_result[Constants.EXECUTION_OUTPUT]=f"{execution_result[Constants.EXECUTION_OUTPUT]}{security_key} is set to {app_transport_security_dict[security_key]}.\nExpected value is {Constants.APP_TRANSPORT_SECURITY_EXPECTED_VALUES[security_key]}"
    else:
        execution_result[Constants.EXECUTION_OUTPUT] = (f"{execution_result[Constants.EXECUTION_OUTPUT]}Unable to find the Info.plist file")

    return execution_result


################## sample call
# PATH = "/Users/harshith/Desktop/Whatsapp/Payload/WhatsApp.app/Info.plist"
# result = check_for_app_transport_security(PATH)
# print (result)
