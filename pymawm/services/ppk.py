general_services = {
    'add_lpn_to_order_crit': '/pickpack/api/pickpack/addLpnToOrderCriteria/',
    'add_non_inv_olpn_crit': '/pickpack/api/pickpack/addNonInventoryOlpnCriteria/',
    'audit_outbound_container_crit': '/pickpack/api/pickpack/auditOutboundContainerCriteria/',
    'audit_planning_crit': '/pickpack/api/pickpack/auditPlanningCriteria/',
    'audit_result': '/pickpack/api/pickpack/auditResult/',
    'container_type': '/pickpack/api/pickpack/containerType/',
    'cancel_olpn_crit': '/pickpack/api/pickpack/cancelOlpnCriteria/',
    'clear_outbound_sort_crit': '/pickpack/api/pickpack/clearObSortLocationCriteria/',
    'dedicated_by':'/pickpack/api/stagingLocationAssignment/dedicatedBy/',
    'document_category': '/pickpack/api/docgeneration/documentCategory/',
    'document_template_type': '/pickpack/api/docgeneration/documentTemplateType/',
    'document_template_xref': '/pickpack/api/pickpack/docTemplateXref/',
    'document_type_category_xref': '/pickpack/api/pickpack/docTypeCategoryXref/',
    'make_pick_cart_crit':'/pickpack/api/pickpack/makePickCartCriteria/',
    'olpn':'/pickpack/api/pickpack/olpn/',
    'olpn_detail':'/pickpack/api/pickpack/olpnDetail/',
    'olpn_condition_code':'/pickpack/api/pickpack/olpnConditionCode/',
    'olpn_condition_assign_crit':'/pickpack/api/pickpack/olpnConditionAssignCriteria/',
    'olpn_creation_code': '/pickpack/api/pickpack/olpnCreationCode/',
    'olpn_creation_mode': '/pickpack/api/pickpack/olpnCreationMode/',
    'olpn_palletize_crit':'/pickpack/api/pickpack/olpnPalletizeCriteria/',
    'olpn_planning_crit':'/pickpack/api/pickpack/olpnPlanningCriteria/',
    'olpn_planning_run':'/pickpack/api/pickpack/olpnPlanningRun/',
    'olpn_planning_run_detail':'/pickpack/api/pickpack/olpnPlanningRunDetail/',
    'olpn_status':'/pickpack/api/pickpack/olpnStatus/',
    'ob_manual_sorter':'/pickpack/api/pickpack/obManualSorter/',
    'ob_sort_loc_assignment':'/pickpack/api/pickpack/obSortLocationAssignment/',
    'outbound_container_gen_crit':'/pickpack/api/pickpack/outboundContainerGenerationCriteria/',
    'outbound_container_inquiry_crit':'/pickpack/api/pickpack/outboundContainerInquiryCriteria/',
    'outbound_putaway_crit':'/pickpack/api/pickpack/outboundPutawayCriteria/',
    'outbound_sort_crit':'/pickpack/api/pickpack/outboundSortCriteria/',
    'outbound_unique_attr':'/pickpack/api/pickpack/outboundUniqueAttributes/',
    'pack_crit':'/pickpack/api/pickpack/packCriteria/',
    'pack_loc_det':'/pickpack/api/pickpack/packLocationDetermination/',
    'pack_loc_det_crit':'/pickpack/api/pickpack/packLocationDeterminationCriteria/',
    'pack_loc_det_strat':'/pickpack/api/pickpack/packLocationDeterminationStrategy/',
    'pack_override_crit':'/pickpack/api/pickpack/packOverrideCriteria/',
    'pick_crit':'/pickpack/api/pickpack/pickCriteria/',
    'pick_override_crit':'/pickpack/api/pickpack/pickOverrideCriteria/',
    'picking_container':'/pickpack/api/pickpack/pickingContainer/',
    'print_crit':'/pickpack/api/pickpack/printCriteria/',
    'print_ob_doc_strategy':'/pickpack/api/pickpack/printOutboundDocumentationStrategy/',
    'print_criteria_doc_template_type_xref':'/pickpack/api/pickpack/printCriteriaDocTemplateTypeXref/',
    'printer_type_doc_template_xref':'/pickpack/api/docprinting/printerTypeDocTemplateXref/',
    'printer_doc_template_type':'/pickpack/api/pickpack/printDocTemplateType/',
    'reason_code': '/pickpack/api/pickpack/reasonCode/',
    'split_combine_olpn_crit': '/pickpack/api/pickpack/splitCombineOlpnCriteria/',
    'store_pack_location_lookup': '/pickpack/api/pickpack/storePackLocationLookup/',
    'track_number_generation_crit': '/pickpack/api/pickpack/trackingNumberGenerationCriteria/',
}

search_services = {
    'search_audit_status':'/pickpack/api/pickpack/auditStatus/search',
    'search_olpn_dtl_status':'/pickpack/api/pickpack/olpnDetailStatus/search',
    'search_picking_container_status': '/pickpack/api/pickpack/pickingContainerStatus',
}

get_services = {
    'get_audit_status':'/pickpack/api/pickpack/auditStatus/',
    'get_olpn_dtl_status':'/pickpack/api/pickpack/olpnDetailStatus/',
    'get_temp_file_names': '/pickpack/api/document/templateFileNames',
}


import_services = {
    'import_ship_to_hold':'/pickpack/api/pickpack/olpn/olpns/shipToHold',
    'post_doc_for_label' : '/pickpack/api/document/view'
}

