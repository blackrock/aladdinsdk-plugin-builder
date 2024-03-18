# AladdinSDK Plugin Builder

This project builds API bundle plugins for AladdinSDK using swagger specifications. The valid Aladdin API specifications are to be included in the appropriate plugin directory [here](/resources/swagger_plugin_bundles/).


## Table of Contents

- [AladdinSDK Plugin Builder](#aladdinsdk-plugin-builder)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Credits](#credits)
  - [Contact](#contact)

## Installation

The plugins will be built via Github Actions on this repository. 

_For local development refer [Contributing](#contributing) section._

## Usage

To update contents of any plugin, or to create/delete plugins, update the directory structure and contents under [swagger_plugin_bundles](/resources/swagger_plugin_bundles/).

For Aladdin's Graph APIs, the specification should include the following details:
- `info.x-aladdin-spec-id` - ID given in the following format `agraph.<domain name>.<segment name>.<api group>.<version>.<API Name>`
- Path security definitions

### Requirements to run the script:
- Python (v3.9+)
- Java (to run openapi-generator-cli jar to perform codegen using swagger file)
- Openapi-generator-cli jar OR ability to `wget` jar from maven
- Target location to where the python project needs to be created
- Plugin version (should correspond to agraph version of swagger gen files)

## Contributing

- The main entry point of the project is asdk_agraph_plugin_builder.py, and houses the core logic of how to read an AGraph swagger specification. The script requires the following inputs:
  - `-sb` / `--swagger-bundle`: Path to a directory containing swagger files to be added to the API bundle
  - `-tl` / `--target-location`: Path to where the built API plugin artifact should be stored
  - `-pv` / `--plugin-version`: Version of plugin to be created
- API bundles are under `/resources/swagger_plugin_bundles`
- The builder creates plugins which contain the following:
  - API client code bundled under appropriate paths derived from spec ID
  - `api_registry.py` and `domain_apis_list.json` files to help the core AladdinSDK read contents of the plugin
  - `pyproject.toml` configuration file used by packaging tools

Also refer [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

The license for the project. Lint to the LICENSE file in the root

## Credits

Acknowledgements for any contributors, libraries, or resources.

## Contact

Contact information for questions or feedback.