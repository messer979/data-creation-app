search_services = {
	# "search_activity_tracking": "/dmui-search/api/dmui-facade/entity/search"
	"search_chart_data":"/dmui-search/api/dmui-facade/waves/chartdata",
	"search_chart_summary":"/dmui-search/api/dmui-facade/waves/summaryMetric/search",
	"search_calculated_metrics":"/dmui-search/api/dmui-facade/metric/search",
	"search_calculated_metrics_url":"/dmui-search/api/dmui-facade/metric/url",
	"search_wave_metrics_detailed":"/dmui-search/api/dmui-facade/monitor/detailedWaveMetrics/search",
}

general_services = {
    "base_chart_layout":"/dmui-search/api/uimetadata/baseChartLayout/",
    "base_component_actions":"/dmui-search/api/uimetadata/baseComponentActions/",
    "base_dashboard_layout":"/dmui-search/api/uimetadata/baseDashboardLayout/",
    "base_details_layout":"/dmui-search/api/uimetadata/baseDetailsLayout/",
    "base_entity_attributes":"/dmui-search/api/uimetadata/baseEntityAttributes/",
    "base_entity_metrics":"/dmui-search/api/uimetadata/baseEntityMetrics/",
    "base_entity_relationships":"/dmui-search/api/uimetadata/baseEntityRelationships/",
    "base_filter_layout":"/dmui-search/api/uimetadata/baseFilterLayout/",
    "base_lookup_layout":"/dmui-search/api/uimetadata/baseLookupLayout/",
    "base_page_layout":"/dmui-search/api/uimetadata/basePageLayout/",
    "chart_layout":"/dmui-search/api/uimetadata/chartLayout/",
    "component_actions":"/dmui-search/api/uimetadata/componentActions/",
    "dashboard_layout":"/dmui-search/api/uimetadata/dashboardLayout/",
    "details_layout":"/dmui-search/api/uimetadata/detailsLayout/",
    "dmui_config":"/dmui-search/api/dmui-facade/dmuiConfig/",
    "dmui_sessions":"/dmui-search/api/dmui-facade/dmuiSession/",
    "entity_metrics" : "/dmui-search/api/uimetadata/entityMetrics/",
    "user_charts_preference":"/dmui-search/api/dmui-facade/userChartsPreference/",
    "user_filter":"/dmui-search/api/uimetadata/userFilter/",
    "user_filter_default":"/dmui-search/api/uimetadata/userFilterDefault/",
    "user_filter_preference":"/dmui-search/api/dmui-facade/userFilterPreference/",
    "user_homepage_preference":"/dmui-search/api/dmui-facade/userHomepagePreference/",
    "user_preferred_filter":"/dmui-search/api/uimetadata/userPreferredFilter/",
    "user_search":"/dmui-search/api/dmui-facade/userSearch/",
    "view_layout":"/dmui-search/api/uimetadata/viewLayout/",
    "widget":"/dmui-search/api/uimetadata/widget/",
}

get_services = {
	"get_map_api_info":"/dmui-search/api/dmui-facade/map/apiInfo",
	"get_map_build_layer":"/dmui-search/api/dmui-facade/map/buildLayer",
	"get_employee_position":"/dmui-search/api/dmui-facade/map/getEmployeesWithLastKnownPosition",
	"get_wave_metrics_additional":"/dmui-search/api/dmui-facade/monitor/additionalWaveMetrics",
	"get_wave_metrics_detailed":"/dmui-search/api/dmui-facade/monitor/detailedWaveMetrics",
	"get_calculated_metrics_for_wes":"/dmui-search/api/dmui-facade/monitor/wes",
    "get_metadata_directory_content": "/dmui-search/api/dmui-facade/config/getMetadataDirectoryContent",
}

# seems like we could get metadata with this 
# /api/dmui-facade/config/action/{componentName}/{viewName}
# /api/dmui-facade/config/attribute/{componentName}/{viewName}
# /api/dmui-facade/config/list/{componentName}/{viewName}
# /api/dmui-facade/config/chart/{componentName}/{viewName}
# /api/dmui-facade/config/lookup/{componentName}/{viewName}
# /api/dmui-facade/config/panel/{componentName}/{viewName}
# /api/dmui-facade/config/metric/{componentName}/{viewName}
