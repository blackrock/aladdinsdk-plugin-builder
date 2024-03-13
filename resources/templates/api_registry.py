import os
import json
from pathlib import Path


def fetch_api_details_for_asdk():
    try:
        _domain_plugin_installation_path = Path(__file__).parent
        with open(os.path.join(_domain_plugin_installation_path, 'domain_apis_list.json'), "r") as file:
            _domain_registry_json = json.load(file)

            for api_entry in _domain_registry_json:
                relative_api_module_path = api_entry['api_module_path'].replace(".", "/")
                swagger_file_path = Path(os.path.join(_domain_plugin_installation_path.parent, relative_api_module_path, "swagger.json"))
                api_entry['swagger_file_path'] = swagger_file_path

            return _domain_registry_json
    except Exception as ex:
        raise Exception("Aladdin SDK Plugin setup error. Unable to read domain's API codegen list. Potentially malformed file.") from ex
