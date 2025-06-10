"""
Test version of inventory transfer using HTTP requests to dummy server
"""

import requests
import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime
import threading
from dataclasses import dataclass
import logging

@dataclass
class TransferConfig:
    """Configuration for inventory transfer"""
    source_url: str
    target_url: str
    source_zones: List[str]
    target_zone: str
    page_size: int = 100
    max_pages: int = 100

class TestInventoryTransferLogger:
    """Logger for UI display"""
    
    def __init__(self):
        self.logs = []
        self.lock = threading.Lock()
    
    def log(self, level: str, message: str):
        """Add a log message"""
        with self.lock:
            timestamp = datetime.now().strftime("%H:%M:%S")
            log_entry = {
                "timestamp": timestamp,
                "level": level,
                "message": message
            }
            self.logs.append(log_entry)
            print(f"[{timestamp}] {level}: {message}")
    
    def error(self, message: str):
        self.log("ERROR", message)
    
    def success(self, message: str):
        self.log("SUCCESS", message)
    
    def warning(self, message: str):
        self.log("WARNING", message)
    
    def step(self, message: str):
        self.log("STEP", message)
    
    def info(self, message: str):
        self.log("INFO", message)
    
    def get_logs(self) -> List[Dict]:
        """Get all logs"""
        with self.lock:
            return self.logs.copy()
    
    def clear_logs(self):
        """Clear all logs"""
        with self.lock:
            self.logs.clear()

class TestActiveInventoryTransfer:
    """Test version of active inventory transfer using HTTP requests"""
    
    def __init__(self, logger: TestInventoryTransferLogger):
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        })
    
    def _make_request(self, url: str, method: str = 'POST', data: Any = None) -> Optional[Dict]:
        """Make HTTP request with error handling"""
        try:
            if method.upper() == 'POST':
                response = self.session.post(url, json=data, timeout=30)
            else:
                response = self.session.get(url, timeout=30)
            
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timeout for {url}")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.error(f"Connection error for {url}")
            return None
        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error {e.response.status_code} for {url}")
            return None
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON response from {url}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error for {url}: {str(e)}")
            return None
    
    def _get_inventory_by_zone(self, base_url: str, zone: str, page_size: int = 100, max_pages: int = 100) -> List[Dict]:
        """Fetch inventory data by zone from dummy server"""
        self.logger.step(f"Fetching inventory from zone {zone}")
        
        all_inventory = []
        page = 0
        
        while page < max_pages:
            query_data = {
                "LocationQuery": {
                    "Query": f"Zone ={zone} and InventoryReservationTypeId=LOCATION"
                },
                "Size": page_size,
                "Page": page
            }
            
            self.logger.info(f"Fetching page {page + 1} for zone {zone}")
            
            result = self._make_request(f"{base_url}/inventory/search", data=query_data)
            if not result:
                self.logger.error(f"Failed to fetch page {page + 1} for zone {zone}")
                break
            
            data = result.get('data', [])
            if not data:
                self.logger.info(f"No more data on page {page + 1} for zone {zone}")
                break
            
            all_inventory.extend(data)
            
            # Check if we have more pages
            header = result.get('header', {})
            total_count = header.get('totalCount', 0)
            current_page = header.get('currentPage', page)
            page_size_actual = header.get('pageSize', page_size)
            
            self.logger.info(f"Retrieved {len(data)} records (Total: {len(all_inventory)}/{total_count})")
            
            if len(all_inventory) >= total_count or len(data) < page_size_actual:
                break
            
            page += 1
            time.sleep(0.1)  # Small delay between requests
        
        self.logger.success(f"Retrieved {len(all_inventory)} total records from zone {zone}")
        return all_inventory
    
    def _get_item_details(self, base_url: str, item_ids: List[str]) -> Dict[str, Dict]:
        """Fetch item details for multiple items"""
        if not item_ids:
            return {}
        
        self.logger.step(f"Fetching details for {len(item_ids)} items")
        
        # Split into chunks of 50
        chunk_size = 50
        all_items = {}
        
        for i in range(0, len(item_ids), chunk_size):
            chunk = item_ids[i:i + chunk_size]
            
            query = f"ItemId in ({','.join(chunk)})"
            query_data = {
                "query": query,
                "size": len(chunk)
            }
            
            self.logger.info(f"Fetching item details chunk {i//chunk_size + 1}")
            
            result = self._make_request(f"{base_url}/item/search", data=query_data)
            if not result:
                self.logger.warning(f"Failed to fetch item details for chunk {i//chunk_size + 1}")
                continue
            
            items = result.get('data', [])
            for item in items:
                item_id = item.get('ItemId')
                if item_id:
                    all_items[item_id] = item
            
            time.sleep(0.1)  # Small delay between requests
        
        self.logger.success(f"Retrieved details for {len(all_items)} items")
        return all_items
    
    def _import_items_to_target(self, base_url: str, items: List[Dict]) -> bool:
        """Import items to target system"""
        if not items:
            return True
        
        self.logger.step(f"Importing {len(items)} items to target system")
        
        result = self._make_request(f"{base_url}/item/bulk-import", data=items)
        if not result:
            self.logger.error("Failed to import items to target system")
            return False
        
        imported_count = result.get('imported_count', 0)
        failed_count = result.get('failed_count', 0)
        
        if failed_count > 0:
            self.logger.warning(f"Imported {imported_count} items, {failed_count} failed")
        else:
            self.logger.success(f"Successfully imported {imported_count} items")
        
        return True
    
    def _sync_items(self, base_url: str) -> bool:
        """Sync items in target system"""
        self.logger.step("Syncing items in target system")
        
        result = self._make_request(f"{base_url}/item/sync", data={})
        if not result:
            self.logger.error("Failed to sync items in target system")
            return False
        
        self.logger.success("Items synchronized successfully")
        return True
    
    def _create_inventory_adjustments(self, target_url: str, inventory_data: List[Dict], target_zone: str) -> bool:
        """Create inventory adjustments in target system"""
        if not inventory_data:
            return True
        
        self.logger.step(f"Creating {len(inventory_data)} inventory adjustments in zone {target_zone}")
        
        # Prepare adjustment data
        adjustments = []
        for record in inventory_data:
            adjustment = {
                "ItemId": record.get('ItemId'),
                "LocationId": f"{target_zone}-{record.get('LocationId', '').split('-')[-1]}",
                "OnHand": record.get('OnHand', 0),
                "ReservationTypeId": "LOCATION",
                "Zone": target_zone,
                "AdjustmentType": "ABSOLUTE",
                "Reason": "ZONE_TRANSFER"
            }
            adjustments.append(adjustment)
        
        # Split into chunks for processing
        chunk_size = 100
        total_processed = 0
        total_failed = 0
        
        for i in range(0, len(adjustments), chunk_size):
            chunk = adjustments[i:i + chunk_size]
            
            self.logger.info(f"Processing adjustment chunk {i//chunk_size + 1} ({len(chunk)} records)")
            
            result = self._make_request(f"{target_url}/inventory/adjust", data=chunk)
            if not result:
                self.logger.error(f"Failed to process adjustment chunk {i//chunk_size + 1}")
                total_failed += len(chunk)
                continue
            
            data = result.get('data', {})
            successful = data.get('SuccessfulRecords', 0)
            failed_records = data.get('FailedRecords', [])
            
            total_processed += successful
            total_failed += len(failed_records)
            
            if failed_records:
                for failed in failed_records[:3]:  # Show first 3 failures
                    self.logger.warning(f"Failed adjustment: {failed.get('error', 'Unknown error')}")
            
            self.logger.info(f"Chunk processed: {successful} successful, {len(failed_records)} failed")
            time.sleep(0.2)  # Small delay between chunks
        
        if total_failed > 0:
            self.logger.warning(f"Adjustments completed: {total_processed} successful, {total_failed} failed")
        else:
            self.logger.success(f"All {total_processed} adjustments completed successfully")
        
        return total_failed == 0
    
    def transfer_inventory(self, config: TransferConfig) -> bool:
        """Transfer inventory from source zones to target zone"""
        try:
            self.logger.info("Starting inventory transfer process")
            self.logger.info(f"Source: {config.source_url}")
            self.logger.info(f"Target: {config.target_url}")
            self.logger.info(f"Source zones: {', '.join(config.source_zones)}")
            self.logger.info(f"Target zone: {config.target_zone}")
            
            # Test connectivity
            self.logger.step("Testing server connectivity")
            
            source_health = self._make_request(f"{config.source_url}/health", method='GET')
            target_health = self._make_request(f"{config.target_url}/health", method='GET')
            
            if not source_health:
                self.logger.error("Cannot connect to source server")
                return False
            
            if not target_health:
                self.logger.error("Cannot connect to target server")
                return False
            
            self.logger.success("Server connectivity verified")
            
            # Collect all inventory from source zones
            all_inventory = []
            for zone in config.source_zones:
                zone_inventory = self._get_inventory_by_zone(
                    config.source_url, 
                    zone, 
                    config.page_size, 
                    config.max_pages
                )
                all_inventory.extend(zone_inventory)
            
            if not all_inventory:
                self.logger.warning("No inventory found in source zones")
                return True
            
            self.logger.success(f"Total inventory records collected: {len(all_inventory)}")
            
            # Get unique item IDs
            unique_item_ids = list(set(record.get('ItemId') for record in all_inventory if record.get('ItemId')))
            self.logger.info(f"Found {len(unique_item_ids)} unique items")
            
            # Get item details from source
            item_details = self._get_item_details(config.source_url, unique_item_ids)
            
            # Import items to target (if needed)
            if item_details:
                items_to_import = list(item_details.values())
                if not self._import_items_to_target(config.target_url, items_to_import):
                    self.logger.error("Failed to import items to target")
                    return False
                
                # Sync items
                if not self._sync_items(config.target_url):
                    self.logger.error("Failed to sync items")
                    return False
            
            # Create inventory adjustments
            if not self._create_inventory_adjustments(config.target_url, all_inventory, config.target_zone):
                self.logger.error("Failed to create all inventory adjustments")
                return False
            
            self.logger.success("Inventory transfer completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Unexpected error during transfer: {str(e)}")
            return False
