# AladdinSDK Plugin Builder

This project builds API bundle plugins for [AladdinSDK](https://github.com/blackrock/aladdinsdk) using swagger specifications.

Plugins are built via Github Actions based on specifications included in plugin directories [here](/resources/swagger_plugin_bundles/).
For each plugin directory, an AladdinSDK plugin will be published which contains API clients based on the swagger files in that directory.

## Table of Contents

- [AladdinSDK Plugin Builder](#aladdinsdk-plugin-builder)
  - [API Plugins](#api-plugins)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)
  - [Credits](#credits)
  - [Contact](#contact)

## API Plugins

_Pre-requisite: Install AladdinSDK using `pip install aladdinsdk`_

AladdinSDK's functional capabilities can be extended as needed using 'plugins'. These are essentially API bundles created at domain level. </br>
The external facing APIs are bundled as follows:

### asdk_plugin_accounting
- Command to install: `pip install asdk_plugin_accounting`
  | Included APIs |
  |:-------------------------------------------------|
  | [PortfolioConfigurationAPI v1](resources/swagger_plugin_bundles/accounting/accounting_configuration_attribute_portfolio_records_v1_portfolio_configuration_api.swagger.json) |
  | [CompositeMembershipAPI v1](resources/swagger_plugin_bundles/accounting/accounting_configuration_composite_membership_v1_composite_membership_api.swagger.json) |
  | [AborLotAPI v1](resources/swagger_plugin_bundles/accounting/accounting_transactions_abor_lot_v1_abor_lot_api.swagger.json) |
  | [ValuationsAPI v1](resources/swagger_plugin_bundles/accounting/accounting_workflow_valuations_v1_valuations_api.swagger.json) |

### asdk_plugin_analytics
- Command to install: `pip install asdk_plugin_analytics`
  | Included APIs |
  |:-------------------------------------------------|
  | [ClimateAPI v1](resources/swagger_plugin_bundles/analytics/analytics_data_climate_v1_climate_api.swagger.json) |
  | [EsgDataAPI v1](resources/swagger_plugin_bundles/analytics/analytics_data_esg_v1_esg_data_api.swagger.json) |
  | [EvaluatorAnalyticsAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_evaluator_analytics_api.swagger.json) |
  | [RiskConfigAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_config_api.swagger.json) |
  | [RiskCustomEvaluationMetricAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_custom_evaluation_metric_api.swagger.json) |
  | [RiskExceptionAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_exception_api.swagger.json) |
  | [RiskRuleAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_rule_api.swagger.json) |
  | [RiskTaskAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_task_api.swagger.json) |
  | [RiskWorkflowAPI v1](resources/swagger_plugin_bundles/analytics/analytics_oversight_governance_v1_risk_workflow_api.swagger.json) |
  | [SecurityReturnsAPI v1](resources/swagger_plugin_bundles/analytics/analytics_security_analytics_returns_v1_security_return_api.swagger.json) |

### asdk_plugin_clients
- Command to install: `pip install asdk_plugin_clients`
  | Included APIs |
  |:-------------------------------------------------|
  | [EnrichedCapitalFlowAPI v1](resources/swagger_plugin_bundles/clients/clients_capital_flows_enriched_capital_flow_v1_enriched_capital_flow_api.swagger.json) |

### asdk_plugin_compliance
- Command to install: `pip install asdk_plugin_compliance`
  | Included APIs |
  |:-------------------------------------------------|
  | [ComplianceRuleAssignmentAPI v1](resources/swagger_plugin_bundles/compliance/compliance_state_compliance_rule_assignment_v1_compliance_rule_assignment_api.swagger.json) |
  | [ComplianceRuleAPI v1](resources/swagger_plugin_bundles/compliance/compliance_state_compliance_rule_v1_compliance_rule_api.swagger.json) |
  | [LevelAPI v1](resources/swagger_plugin_bundles/compliance/compliance_state_level_v1_level_api.swagger.json) |
  | [ViolationAPI v1](resources/swagger_plugin_bundles/compliance/compliance_state_violation_v1_violation_api.swagger.json) |

### asdk_plugin_data
- Command to install: `pip install asdk_plugin_data`
  | Included APIs |
  |:-------------------------------------------------|
  | [PricingAPI v2](resources/swagger_plugin_bundles/data/data_market_data_price_v2_price_api.swagger.json) |
  | [SecurityCreationAPI v1](resources/swagger_plugin_bundles/data/data_reference_data_asset_asset_creation_v1_security_creation_api.swagger.json) |

### asdk_plugin_investment_operations
- Command to install: `pip install asdk_plugin_investment_operations`
  | Included APIs |
  |:-------------------------------------------------|
  | [CorporateActionAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_asset_lifecycle_corporate_action_v1_corporate_action_api.swagger.json) |
  | [CorporateActionEntitlementAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_asset_lifecycle_corporate_action_v1_corporate_action_entitlement_api.swagger.json) |
  | [CouponResetAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_asset_lifecycle_coupon_reset_v1_coupon_reset_api.swagger.json) |
  | [PrincipalInterestFactorAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_asset_lifecycle_principal_interest_factor_v1_principal_interest_factor_api.swagger.json) |
  | [MiscellaneousCashflowAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_cash_flows_miscellaneous_cashflow_v1_miscellaneous_cashflow_api.swagger.json) |
  | [AccountInfoAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_account_info_v1_account_info_api.swagger.json) |
  | [AuditAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_audit_api.swagger.json) |
  | [BrokerAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_broker_api.swagger.json) |
  | [BrokerConfirmRoutingAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_broker_confirm_routing_api.swagger.json) |
  | [BrokerDeskAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_broker_desk_api.swagger.json) |
  | [BrokerExternalAliasAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_broker_external_alias_api.swagger.json) |
  | [CounterPartySettlementInstructionAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_counterparty_settlement_instruction_api.swagger.json) |
  | [CounterPartySettlementInstructionTemplateAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_broker_v1_counterparty_settlement_instruction_template_api.swagger.json) |
  | [ContactAPI v1](resources/swagger_plugin_bundles/investment_operations/investment_operations_reference_data_contact_v1_contact_api.swagger.json) |

### asdk_plugin_investment_research
- Command to install: `pip install asdk_plugin_investment_research`
  | Included APIs |
  |:-------------------------------------------------|
  | [AnalystCoverageAPI v1](resources/swagger_plugin_bundles/investment_research/investment_research_analyst_coverage_v1_analyst_coverage_api.swagger.json) |
  | [EngagementAPI v1](resources/swagger_plugin_bundles/investment_research/investment_research_content_engagement_v1_engagement_api.swagger.json) |
  | [ResearchNoteAPI v2](resources/swagger_plugin_bundles/investment_research/investment_research_content_research_note_v2_research_note_api.swagger.json) |
  | [CriterionAPI v1](resources/swagger_plugin_bundles/investment_research/investment_research_surveillance_criterion_v1_criterion_api.swagger.json) |
  | [WatchlistAPI v1](resources/swagger_plugin_bundles/investment_research/investment_research_surveillance_watchlist_v1_watchlist_api.swagger.json) |

### asdk_plugin_platform
- Command to install: `pip install asdk_plugin_platform`
  | Included APIs |
  |:-------------------------------------------------|
  | [PermissionAPI v1](resources/swagger_plugin_bundles/platform/platform_access_permission_v1_permission_api.swagger.json) |
  | [UserGroupPermissionAPI v1](resources/swagger_plugin_bundles/platform/platform_access_permission_v1_user_group_permission_api.swagger.json) |
  | [UserGroupAPI v1](resources/swagger_plugin_bundles/platform/platform_access_user_group_v1_user_group_api.swagger.json) |
  | [UserGroupMemberAPI v1](resources/swagger_plugin_bundles/platform/platform_access_user_group_v1_user_group_member_api.swagger.json) |
  | [UserAPI v1](resources/swagger_plugin_bundles/platform/platform_identity_user_v1_user_api.swagger.json) |
  | [AdcDatasetAPI v1](resources/swagger_plugin_bundles/platform/platform_studio_adc_adc_dataset_v1_adc_dataset_api.swagger.json) |

### asdk_plugin_portfolio
- Command to install: `pip install asdk_plugin_portfolio`
  | Included APIs |
  |:-------------------------------------------------|
  | [PortfolioGroupAPI v1](resources/swagger_plugin_bundles/portfolio/portfolio_configuration_portfolio_group_v1_portfolio_group_api.swagger.json) |
  | [RestrictedAssetAPI v1](resources/swagger_plugin_bundles/portfolio/portfolio_configuration_restricted_asset_v1_restricted_asset_api.swagger.json) |

### asdk_plugin_portfolio_management
- Command to install: `pip install asdk_plugin_portfolio_management`
  | Included APIs |
  |:-------------------------------------------------|
  | [CashLadderAPI v2](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_cash_cash_ladder_v2_cash_ladder_api.swagger.json) |
  | [PositionsAPI v2](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_positions_positions_v2_positions_api.swagger.json) |
  | [CIDReaderAPI v1](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_setup_cids_v1_cids_reader_api.swagger.json) |
  | [CIDWriterAPI v1](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_setup_cids_v1_cids_writer_api.swagger.json) |
  | [InvestmentTargetAPI v1](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_target_investment_target_v1_investment_target_api.swagger.json) |
  | [StrategyAPI v1](resources/swagger_plugin_bundles/portfolio_management/portfolio_management_target_strategy_v1_strategy_api.swagger.json) |

### asdk_plugin_trading
- Command to install: `pip install asdk_plugin_trading`
  | Included APIs |
  |:-------------------------------------------------|
  [OrderAPI v1](resources/swagger_plugin_bundles/trading/trading_order_management_order_v1_order_api.swagger.json) 

## Usage

This script is used in Github Action to build plugins for every tag dropped on this repository.

- The entry point of the script is asdk_agraph_plugin_builder.py. AGraph swagger specifications are read and [openapi-generator v6.6.0](https://github.com/OpenAPITools/openapi-generator/releases/tag/v6.6.0) is used to create an AladdinSDK plugin which bundles together the corresponding API clients.
- To run script, the following inputs are required:
  - `-sb` / `--swagger-bundle`: Path to a directory containing swagger files to be added to the API bundle
  - `-tl` / `--target-location`: Path to where the built API plugin artifact should be stored
  - `-pv` / `--plugin-version`: Version of plugin to be created
- Optional arguments:
  - `-v` / `--verbose`: Prints more detailed log statements during the execution
  - `-oj` / `--openapi-generator-cli-jar`: Path to openapi-generator-cli jar file, if user wants to use a different version of the jar

### API Specification file details

- To update contents of any plugin, or to create/delete plugins, update the directory structure and contents under [/resources/swagger_plugin_bundles](/resources/swagger_plugin_bundles/) directory.
- For Aladdin's Graph APIs, the specification should include the following details:
  - `info.x-aladdin-spec-id`:
    - ID given in the following format `agraph.<domain name>.<segment name>.<api group>.<version>.<API Name>`
    - This is used to create the registry entry and determine python module path
    - **Note:** The ID should also ensures uniqueness of the API across all plugins. Same API may be bundled in different plugins, but only one definition will be picked by AladdinSDK.
  - Endpoint path security definitions:
    - Used by python client to add authentication headers for API calls

### Requirements to run the script:
- Python (v3.9+)
- Java (to run openapi-generator-cli jar to perform codegen using swagger file)
- Openapi-generator-cli jar OR ability to `wget` jar from maven
- Target location to where the python project needs to be created
- Plugin version (should correspond to agraph version of swagger gen files)

## Contributing

- API bundles are under `/resources/swagger_plugin_bundles`. Any updates to contents of this directory must be approved by Aladdin API stakeholders.
- The builder creates plugins which contain the following:
  - API client code bundled under appropriate paths derived from spec ID
  - `api_registry.py` and `domain_apis_list.json` files to help the core AladdinSDK read contents of the plugin </br>
    _Any updates to these files should be coordinated with the AladdinSDK project._
  - `pyproject.toml` configuration file used by packaging tools

Also refer [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)

## License

The license for the project:
  - [LICENSE](./LICENSE)

## Credits

Core Contributors:
- Vedant Naik
- Eli Kalish
- Harshita Das
- Infant Vasanth

Libraries:
- [openapi-generator v6.6.0](https://github.com/OpenAPITools/openapi-generator/releases/tag/v6.6.0)

## Contact

GitHub Issues: https://github.com/blackrock/aladdinsdk-plugin-builder/issues

Copyright © 2017-2024 os72, licensed under Apache License, Version 2.0.

Copyright © 2024 BlackRock, Inc. Distributed under the Apache License, Version 2.0.
