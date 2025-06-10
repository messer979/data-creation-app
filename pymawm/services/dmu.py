search_services = {
	# "search_activity_tracking": "/dmui-facade/api/dmui-facade/entity/search"
	"search_chart_data":"/dmui-facade/api/dmui-facade/waves/chartdata",
	"search_chart_summary":"/dmui-facade/api/dmui-facade/waves/summaryMetric/search",
	"search_calculated_metrics":"/dmui-facade/api/dmui-facade/metric/search",
	"search_calculated_metrics_url":"/dmui-facade/api/dmui-facade/metric/url",
	"search_wave_metrics_detailed":"/dmui-facade/api/dmui-facade/monitor/detailedWaveMetrics/search",
}

general_services = {
    "base_chart_layout":"/dmui-facade/api/uimetadata/baseChartLayout/",
    "base_component_actions":"/dmui-facade/api/uimetadata/baseComponentActions/",
    "base_dashboard_layout":"/dmui-facade/api/uimetadata/baseDashboardLayout/",
    "base_details_layout":"/dmui-facade/api/uimetadata/baseDetailsLayout/",
    "base_entity_attributes":"/dmui-facade/api/uimetadata/baseEntityAttributes/",
    "base_entity_metrics":"/dmui-facade/api/uimetadata/baseEntityMetrics/",
    "base_entity_relationships":"/dmui-facade/api/uimetadata/baseEntityRelationships/",
    "base_filter_layout":"/dmui-facade/api/uimetadata/baseFilterLayout/",
    "base_lookup_layout":"/dmui-facade/api/uimetadata/baseLookupLayout/",
    "base_page_layout":"/dmui-facade/api/uimetadata/basePageLayout/",
    "chart_layout":"/dmui-facade/api/uimetadata/chartLayout/",
    "component_actions":"/dmui-facade/api/uimetadata/componentActions/",
    "dashboard_layout":"/dmui-facade/api/uimetadata/dashboardLayout/",
    "details_layout":"/dmui-facade/api/uimetadata/detailsLayout/",
    "dmui_config":"/dmui-facade/api/dmui-facade/dmuiConfig/",
    "dmui_sessions":"/dmui-facade/api/dmui-facade/dmuiSession/",
    "entity_metrics" : "/dmui-facade/api/uimetadata/entityMetrics/",
    "metadata_extpack" : "/dmui-facade/api/uimetadata/metadataExtPack/",
    "metadata_extension_pack" : "/dmui-facade/api/uimetadata/metadataExtensionPack/",
    "metadata_extension_ref" : "/dmui-facade/api/uimetadata/metadataExtensionRef/",
    "monitoring_config_param" : "/dmui-facade/api/dmui-facade/monitoringConfigParam/",
    "options_widget" : "/dmui-facade/api/uimetadata/optionsWidget/",
    "user_charts_preference":"/dmui-facade/api/dmui-facade/userChartsPreference/",
    "user_filter":"/dmui-facade/api/uimetadata/userFilter/",
    "user_filter_default":"/dmui-facade/api/uimetadata/userFilterDefault/",
    "user_filter_preference":"/dmui-facade/api/dmui-facade/userFilterPreference/",
    "user_homepage_preference":"/dmui-facade/api/dmui-facade/userHomepagePreference/",
    "user_preferred_filter":"/dmui-facade/api/uimetadata/userPreferredFilter/",
    "user_search":"/dmui-facade/api/dmui-facade/userSearch/",
    "view_layout":"/dmui-facade/api/uimetadata/viewLayout/",
    "widget":"/dmui-facade/api/uimetadata/widget/",
}

get_services = {
	"get_map_api_info":"/dmui-facade/api/dmui-facade/map/apiInfo",
	"get_map_build_layer":"/dmui-facade/api/dmui-facade/map/buildLayer",
	"get_employee_position":"/dmui-facade/api/dmui-facade/map/getEmployeesWithLastKnownPosition",
	"get_wave_metrics_additional":"/dmui-facade/api/dmui-facade/monitor/additionalWaveMetrics",
	"get_wave_metrics_detailed":"/dmui-facade/api/dmui-facade/monitor/detailedWaveMetrics",
	"get_calculated_metrics_for_wes":"/dmui-facade/api/dmui-facade/monitor/wes",
    "get_metadata_directory_content": "/dmui-facade/api/dmui-facade/config/getMetadataDirectoryContent",
}

import_services = {
    'post_inv_transfer': '/dmui-facade/api/dmui-facade/inventory/adjustTransferInventory',
}

# seems like we could get metadata with this 
# /api/dmui-facade/config/action/{componentName}/{viewName}
# /api/dmui-facade/config/attribute/{componentName}/{viewName}
# /api/dmui-facade/config/list/{componentName}/{viewName}
# /api/dmui-facade/config/chart/{componentName}/{viewName}
# /api/dmui-facade/config/lookup/{componentName}/{viewName}
# /api/dmui-facade/config/panel/{componentName}/{viewName}
# /api/dmui-facade/config/metric/{componentName}/{viewName}
