general_services = {
    'allocation':'/dcinventory/api/dcinventory/allocation/',
    'attribute_statistics': '/dcinventory/api/dcinventory/attributeStatistics/',
    'condition_code':'/dcinventory/api/dcinventory/conditionCode/',
    'container_condition':'/dcinventory/api/dcinventory/containerCondition/',
    'dock_door':'/dcinventory/api/dcinventory/dockDoor/',
    'ilpn': '/dcinventory/api/dcinventory/ilpn/',
    'inv': '/dcinventory/api/dcinventory/inventory/',
    'inv_attributes': '/dcinventory/api/dcinventory/inventoryAttributes/',
    'inventory_sync': '/dcinventory/api/dcinventory/inventorySync/',
    'inventory_sync_batch': '/dcinventory/api/dcinventory/inventorySyncBatch/',
    'location': '/dcinventory/api/dcinventory/location/',
    'location_item_assignment': '/dcinventory/api/dcinventory/locationItemAssignment/',
    'location_count_info': '/dcinventory/api/dcinventory/locationCountInfo/',
    'location_capacity_usage': '/dcinventory/api/dcinventory/locationCapacityUsage/',
    'location_mask': '/dcinventory/api/dcinventory/locationMask/',
    'location_template': '/dcinventory/api/dcinventory/locationTemplate/',
    'location_wizard': '/dcinventory/api/dcinventory/locationWizard/',
    'physical_entity_code':'/dcinventory/api/dcinventory/physicalEntityCode/',
    'pix_level':'/dcinventory/api/dcinventory/pixLevel/',
    'product_status':'/dcinventory/api/dcinventory/productStatus/',
    'putaway_condition_code':'/dcinventory/api/dcinventory/putawayConditionCode/',
    'quantity_conversion_uom':'/dcinventory/api/dcinventory/quantityConversionUomType/',
    'recall_inventory_criteria':'/dcinventory/api/dcinventory/recallInventoryCriteria/',
    'sku_dedication_type':'/dcinventory/api/dcinventory/skuDedicationType/',
    'staging_location_type':'/dcinventory/api/dcinventory/stagingLocationType/',
    'storage_location_type':'/dcinventory/api/dcinventory/storageLocationType/',
    'storage_uom':'/dcinventory/api/dcinventory/storageUom/',
    'yard_slot':'/dcinventory/api/dcinventory/yardSlot/',
    'zone': '/dcinventory/api/dcinventory/zone/',
    'zone_capacity':'/dcinventory/api/dcinventory/zoneCapacity/',
    'zone_status': '/dcinventory/api/dcinventory/zoneStatus/',
    'zone_type': '/dcinventory/api/dcinventory/zoneType/',
    'zone_printer_xref': '/dcinventory/api/dcinventory/zonePrinterXref/',
}
search_services = {
    'search_allocatable_inventory':'/dcinventory/api/dcinventory/allocatableInventory',
    'search_ilpn_status_code' : '/dcinventory/api/dcinventory/ilpnStatus/search',
    'search_ilpn_inv': '/dcinventory/api/dcinventory/ilpn/ilpninventorysearch',
    'search_inv_attributes_status': '/dcinventory/api/dcinventory/attributeStatus/search',
    'search_inventory_by_loc': '/dcinventory/api/dcinventory/inventory/inventorysearchAggregateByLocation',
    'search_item': '/dcinventory/api/itemlistener/item/search',
    'search_task_status':'/dcinventory/api/task/taskStatus/search',

}

get_services = {
    'get_allocation':'/dcinventory/api/dcinventory/allocation/',
    'get_ilpn_status_code' : '/dcinventory/api/dcinventory/ilpnStatus/',
    'get_inv_attributes_status': '/dcinventory/api/dcinventory/attributeStatus/',
    'get_inv_search': '/dcinventory/api/dcinventory/inventory/inventorysearch/',
    'get_inventory_by_loc': '/dcinventory/api/dcinventory/inventorysearchAggregateByLocation/',
    'get_item': '/dcinventory/api/itemlistener/item/',
    'get_task_status':'/dcinventory/api/task/taskStatus/',
}

import_services = {
    'post_inv_search': '/dcinventory/api/dcinventory/inventory/inventorysearch',
    'post_load_allocatable_inventory':'/dcinventory/api/dcinventory/loadInventory/allocatableInventory',
    'post_update_ilpn_and_inventory': '/dcinventory/api/dcinventory/ilpn/updateIlpnAndInventory',
    'post_adjust_inventory': '/dcinventory/api/dcinventory/inventory/adjustInventory',
    'post_absolute_adjust_inventory': '/dcinventory/api/dcinventory/inventory/adjustAbsoluteQuantity',
    'post_location_rebuild': '/dcinventory/api/dcinventory/rebuild/rebuildInventory',
}


