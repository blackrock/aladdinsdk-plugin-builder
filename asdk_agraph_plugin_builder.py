import os
import subprocess
import tempfile
import json
import argparse
import platform
import pathlib

"""
Utility to generate plugins for AladdinSDK
"""

# Run constants
_ASDK_PLUGIN_MODULE_PREFIX = "asdk_plugin_"
_openapi_generator_cli_version = "6.6.0"
_OPENAPI_GENERATOR_JAR_DOWNLOAD_LINK = f'https://artifactory.blackrock.com:9000/artifactory/libs-releases/org/openapitools/openapi-generator-cli/{_openapi_generator_cli_version}/openapi-generator-cli-{_openapi_generator_cli_version}.jar'  # noqa: E501
platform_os = platform.platform()
_ASDK_PLUGIN_BUILDER_REPO = os.getcwd()
if 'Windows' in platform_os:
    _ASDK_PLUGIN_BUILDER_REPO = pathlib.PureWindowsPath(os.getcwd()).as_posix()

_openapi_generator_jar_filepath = os.path.join(_ASDK_PLUGIN_BUILDER_REPO, 'resources', 'openapi-generator-cli.jar')


# Helper methods
def _run_command(command_array, message):
    """Given a command array, join with spaces and run.

    Args:
        command_array (_type_): Sequence of program arguments or else a single string. By default, the program to execute is the first item in
            args if args is a sequence. If args is a string, the interpretation is platform-dependent.
        message (_type_): Message to log what the command achieves
    """
    result = None
    platform_os = platform.platform()
    if 'Windows' in platform_os:
        if 'sudo' in command_array:
            command_array.remove('sudo')
        try:
            result = subprocess.run(command_array, stdout=subprocess.PIPE)
        except Exception:
            print(f"subprocess.run failed failed trying subprocess.run for {' '.join(command_array)}")
            os.system(" ".join(command_array))
    else:
        result = subprocess.run(command_array, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if _verbose:
        print(f"{message}: " + " ".join(command_array))

    if result is not None and hasattr(result, "returncode") and result.returncode == 0:
        return True
    else:
        return False


def _update_asdk_plugin_codegen_section(plugin_module_name, api_name, api_version, api_module_path,
                                        target_api_directory, plugin_pkg_target_location):
    """
    Method to update ASDK plugin's codegen sections. Particularly code generated APIs list file.
    This method assumes rest of the codegen steps are complete and swagger json file is present in target api location
    """
    domain_api_list_filepath = os.path.join(plugin_pkg_target_location, plugin_module_name, "domain_apis_list.json")

    # Load the API list file into a Python dictionary
    domain_api_list = []
    if os.path.exists(domain_api_list_filepath):
        with open(domain_api_list_filepath, "r") as file:
            domain_api_list = json.load(file)

    # Update the entry in the dictionary
    filtered_api_list = [x for x in domain_api_list if x['api_name'] != api_name]

    with open(os.path.join(target_api_directory, "swagger.json"), "r") as file:
        _target_swagger_json = json.load(file)

    filtered_api_list.append({
        'api_module_path': api_module_path,
        'api_name': api_name,
        'api_version': api_version,
        'host_url_path': _target_swagger_json['basePath']
    })

    # Always keep the autogenerated config list in sorted order of api_name
    filtered_api_list = sorted(filtered_api_list, key=lambda x: x['api_name'])
    domain_api_list = filtered_api_list

    # Write the updated dictionary back to the file
    with open(domain_api_list_filepath, "w") as file:
        json.dump(domain_api_list, file, indent=4)
    if _verbose:
        print(f"[API: {api_name}-{api_version}] - Registry settings file updated.")


def _generate_target_api_details_from_agraph_swagger_spec(plugin_module_name, agraph_swagger_file_path):
    """Given path to an Aladdin Graph swagger file, read API name, version and generate module path from 'info.x-aladdin-spec-id'.
    Assumption here is x-aladdin-spec-id is of the format 'agraph.<domain>.<segment>.<api>.<VERSION>.<API_NAME>'

    Args:
        plugin_module_name (String): Target plugin module name
        agraph_swagger_file_path (FileDescriptorOrPath): Path to swagger file for API to onboard

    Raises:
        Exception: _description_

    Returns:
        api_name, api_version, api_module_path: name and version of the API from x-aladdin-spec-id, and target module path for the API
    """
    try:
        with open(agraph_swagger_file_path, "r") as file:
            swagger_json_data = json.load(file)
            x_aladdin_spec_id = swagger_json_data['info']['x-aladdin-spec-id']
            spec_id_split = x_aladdin_spec_id.split('.')
            api_name = spec_id_split[-1]
            api_ver = spec_id_split[-2]
            api_module_path = plugin_module_name + "." + x_aladdin_spec_id
            return api_name, api_ver, api_module_path
    except KeyError:
        raise Exception("Incorrect swagger file encountered. "
                        "Info section needs to have 'x-aladdin-spec-id' to help identify API name, version and module path")
    except IndexError:
        raise Exception("Insufficient or incorrect value for x-aladdin-spec-id. "
                        "Expecting following format: agraph.<domain name>.<segment name>.<api group>.<version>.<API Name>")
    except Exception as e:
        print("unexpected error", e)
        return None, None, None


def _onboard_api_using_swagger(plugin_module_name, path_to_agraph_openapi_spec_file, plugin_pkg_target_location):
    """Given a path to agraph swagger file, uses openapi-codegen to create a python client and copy code into target module
    - Creates a temporary python client project
    - Rsync and copies code, swagger and requirements files under given target location
    - Updates api list configuration file

    Args:
        plugin_module_name (_type_): Final name of the plugin module being built
        path_to_agraph_openapi_spec_file (_type_): Absolute path to a agraph swagger file to be used for codegen
        plugin_pkg_target_location (_type_): Target location for API's domain

    Returns:
        tuple: API Name-Version, Generated APIs target module
    """
    api_name, api_ver, api_module_path = _generate_target_api_details_from_agraph_swagger_spec(plugin_module_name, path_to_agraph_openapi_spec_file)
    if api_name is None or api_ver is None or api_module_path is None:
        raise Exception("Insufficient API information in swagger files")

    # using api_module_path, generate target API location
    target_api_directory = os.path.join(plugin_pkg_target_location, *api_module_path.split('.'))

    print(f"Onboarding API - {api_name}-{api_ver}.")
    is_successful = True

    # create a temporary codegen repo
    with tempfile.TemporaryDirectory() as temp_dir:
        print(f'[API: {api_name}-{api_ver}] - created temporary directory', temp_dir)
        if 'Windows' in platform_os:
            temp_dir = pathlib.PureWindowsPath(temp_dir).as_posix()
            print(f'[API: {api_name}-{api_ver}] - windows updated temporary directory', temp_dir)

        python_codegen_command = ["java", "-jar", _openapi_generator_jar_filepath, "generate",
                                  "-i", path_to_agraph_openapi_spec_file,
                                  "-g", "python-nextgen",
                                  "-o", temp_dir,
                                  "--package-name", api_module_path,
                                  "--api-name-suffix", api_name]
        is_successful = is_successful and _run_command(python_codegen_command,
                                                       message=f"[API: {api_name}-{api_ver}] - Generate python client code using swagger spec")

        is_successful = is_successful and _run_command(["rm", "-rf", target_api_directory],
                                                       message=f"[API: {api_name}-{api_ver}] - Remove existing codegen dir if present")
        is_successful = is_successful and _run_command(["mkdir", "-pv", target_api_directory],
                                                       message=f"[API: {api_name}-{api_ver}] - Create target directory for codegen")

        cp_command_swagger = ["cp", path_to_agraph_openapi_spec_file, os.path.join(target_api_directory, "swagger.json")]
        is_successful = is_successful and _run_command(cp_command_swagger,
                                                       message=f"[API: {api_name}-{api_ver}] - Copy swagger file under target directory")

        rsync_command = ["rsync", "-a", os.path.join(temp_dir, plugin_module_name), plugin_pkg_target_location]
        is_successful = is_successful and _run_command(rsync_command,
                                                       message=f"[API: {api_name}-{api_ver}] - Rsync python client code into sdk repo's "
                                                       "codegen package under newly created target directory")

        # Copy requirements.txt at domain root - assumption: all codegen clients share the same requirements
        if not pathlib.Path(f"{plugin_pkg_target_location}/requirements.txt").exists():
            cp_command_requirements = ["cp", os.path.join(temp_dir, "requirements.txt"),
                                       os.path.join(plugin_pkg_target_location, "requirements.txt")]
            _run_command(cp_command_requirements,
                         message=f"[API: {api_name}-{api_ver}] - Copy requirements file under target directory")

    print(f"[API: {api_name}-{api_ver}] - Openapi codegen steps done. Proceeding with ASDK Plugin updates...")
    _update_asdk_plugin_codegen_section(plugin_module_name=plugin_module_name, api_name=api_name, api_version=api_ver,
                                        api_module_path=api_module_path, target_api_directory=target_api_directory,
                                        plugin_pkg_target_location=plugin_pkg_target_location)

    if is_successful:
        print(f"[API: {api_name}-{api_ver}] - API Onboarding complete. Result: 'success'")
    else:
        print(f"[API: {api_name}-{api_ver}] - API Onboarding complete. Result: 'fail/partial-success'")
    return f"{api_name}-{api_ver}"


def _build_plugin_with_swagger_files(plugin_module_name, api_swagger_files, plugin_pkg_target_location):
    """Given paths to swagger files that need to be packaged into the plugin and the target location details, use openapi-generator
    to generate python clients in a temporary location, and copy python code modules into target location under the similar
    domain/segment/api structure. Return list of completed APIs and skipped APIs (with error/reasons for skipping)

    Args:
        plugin_module_name (_type_): Final name of the plugin module being built
        api_swagger_files (_type_): List of swagger filepaths to be included in plugin
        plugin_pkg_target_location (_type_): Target location on build host to create package

    Returns:
        _type_: _description_
    """
    completed_apis_to_spec_map = {}
    skipped_api_specs_to_reason_map = {}

    for api_swagger_file in api_swagger_files:
        try:
            completed_api = _onboard_api_using_swagger(plugin_module_name, api_swagger_file, plugin_pkg_target_location)
            completed_apis_to_spec_map[completed_api] = api_swagger_file
        except Exception as e:
            skipped_api_specs_to_reason_map[api_swagger_file] = str(e)

    return completed_apis_to_spec_map, skipped_api_specs_to_reason_map


def create_plugin_content(swagger_bundle_path, plugin_pkg_target_location, plugin_version):
    """Generate plugin and print execution summary for this plugin.
    Add supplementary files for plugin artifacts:
        api_registry.py - To help AladdinSDK understand available APIs in this domain library
        setup.py - For plugin installation. Details in setup.py are updated for the plugin

    Args:
        swagger_bundle_path (_type_): Path to directory containing swagger files for APIs to be included in plugin
        plugin_pkg_target_location (_type_): Target location on build host to create package
        plugin_version (_type_): Version to be added for the plugin's pyproject.toml file
    """
    plugin_dir = os.path.basename(swagger_bundle_path)
    plugin_name = _ASDK_PLUGIN_MODULE_PREFIX + plugin_dir
    print(f"\nBegin processing plugin: '{plugin_name}'...")

    # Read file paths in swagger bundle directory
    api_swagger_files = []
    for plugin_dir_root, _, files in os.walk(swagger_bundle_path):
        api_swagger_files = [os.path.join(plugin_dir_root, x) for x in files]

    _completed_apis_to_spec_map = {}
    _skipped_api_specs_to_reason_map = {}

    # generate domain plugin
    _completed_apis_to_spec_map, _skipped_api_specs_to_reason_map = _build_plugin_with_swagger_files(plugin_name, api_swagger_files,
                                                                                                     plugin_pkg_target_location)

    # add supplementary files
    if len(_completed_apis_to_spec_map.keys()) > 0:
        cp_api_registry = ["cp", os.path.join(_ASDK_PLUGIN_BUILDER_REPO, "resources", "templates", "api_registry.py"),
                           os.path.join(plugin_pkg_target_location, plugin_name, "api_registry.py")]
        _run_command(cp_api_registry, message=f"[Plugin: {plugin_name}] - Copy api_registry template under target module")

        with open(os.path.join(_ASDK_PLUGIN_BUILDER_REPO, "resources", "templates", "pyproject.toml"), "r") as pyproject_file:
            pyproject_file_content = pyproject_file.read()
            pyproject_file_content = pyproject_file_content.replace(r"{{pkg_version}}", plugin_version)
            pyproject_file_content = pyproject_file_content.replace(r"{{pkg_name}}", plugin_name)

            with open(os.path.join(plugin_pkg_target_location, "pyproject.toml"), "w") as target_pyproject_file:
                target_pyproject_file.write(pyproject_file_content)

    print_run_summary(plugin_name, _completed_apis_to_spec_map, _skipped_api_specs_to_reason_map)


def _summary_helper_split_skipped_map(_skipped_api_specs_to_reason_map):
    _skipped_due_to_errors = {}
    _skipped_due_to_filtering = {}
    for x in _skipped_api_specs_to_reason_map:
        skip_note = _skipped_api_specs_to_reason_map[x]
        if skip_note == "Filtered out":
            _skipped_due_to_filtering[x] = skip_note
        else:
            _skipped_due_to_errors[x] = skip_note
    return _skipped_due_to_errors, _skipped_due_to_filtering


def print_run_summary(plugin_name, _completed_apis_to_spec_map, _skipped_api_specs_to_reason_map):
    print("\n==========================")
    print("FINAL SUMMARY")
    print("==========================")
    _skipped_due_to_errors, _skipped_due_to_filtering = _summary_helper_split_skipped_map(_skipped_api_specs_to_reason_map)
    if _verbose:
        print(f"Summary for plugin: '{plugin_name}' [completed: {len(_completed_apis_to_spec_map)}, "
              f"skipped due to errors: {len(_skipped_due_to_errors)}, filtered out: {len(_skipped_due_to_filtering)}]")
        if len(_completed_apis_to_spec_map) > 0:
            print("\nCompleted APIs:")
            [print(f"{x} - {_completed_apis_to_spec_map[x]}") for x in _completed_apis_to_spec_map]
        if len(_skipped_due_to_errors) > 0:
            print("\nSkipped due to errors APIs:")
            [print(f"{x} - {_skipped_due_to_errors[x]}") for x in _skipped_due_to_errors]
        print("------------------------------------")
    else:
        if len(_completed_apis_to_spec_map) > 0 or len(_skipped_due_to_errors) > 0:
            print(f"Summary for plugin: '{plugin_name}' [completed: {len(_completed_apis_to_spec_map)}, "
                  f"skipped due to errors: {len(_skipped_due_to_errors)}, filtered out: {len(_skipped_due_to_filtering)}]")
            print(f"\nCompleted APIs: {[x for x in _completed_apis_to_spec_map]}")
            print("------------------------------------")
    print(f"\n\nTotal - completed: {len(_completed_apis_to_spec_map)}, failed: {len(_skipped_due_to_errors)}")


# --------------------------------------------------- start ---------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="ASDK Codegen Util", description="Utility to generate python clients for aladdin-graph APIs")
    parser.add_argument('-sb', '--swagger-bundle', help="Path to directory containing swagger files to be bundled in plugin. "
                        "Path's basename is used to create plugin name as - asdk_plugin_<basename>")
    parser.add_argument('-tl', '--target-location', help="Target location where plugin libraries should be created")
    parser.add_argument('-pv', '--plugin-version', help="Tag version of domain plugin artifacts")
    parser.add_argument('-oj', '--openapi-generator-cli-jar', help="(Optional) Path to openapi-generator-cli jar. "
                        f"If not provided, script will attempt to get jar from {_OPENAPI_GENERATOR_JAR_DOWNLOAD_LINK}")
    parser.add_argument('-v', '--verbose', help="(Optional) More verbose summary", action='store_true')

    # Read input args
    args = parser.parse_args()
    print(f"Run args: {args}")

    # source
    _swagger_bundle_path = args.swagger_bundle
    # generator jar
    _custom_openapi_generator_jar_filepath = args.openapi_generator_cli_jar
    # output
    _target_location = args.target_location
    _plugin_version = args.plugin_version
    _verbose = args.verbose

    # Get openapi-generator jar file. If path provided via input args, use that instead.
    if _custom_openapi_generator_jar_filepath is not None:
        _openapi_generator_jar_filepath = _custom_openapi_generator_jar_filepath
    else:
        if not pathlib.Path(_openapi_generator_jar_filepath).exists():
            _run_command(['wget', _OPENAPI_GENERATOR_JAR_DOWNLOAD_LINK, '-O', _openapi_generator_jar_filepath, '--no-check-certificate'],
                         message="Get openapi-generator jar")

    # Create plugin and print summary
    create_plugin_content(_swagger_bundle_path, _target_location, _plugin_version)
