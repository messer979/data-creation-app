"""
Active Inventory Transfer Module
Converts the active_inventory.py script into a callable function with logging
"""

from pymawm import ActiveWM
import sqlite3
import pandas as pd
import math
import requests
import os
import re
import sys
import logging
import time
from copy import deepcopy
import json
from typing import Dict, List, Callable, Any
import io
import contextlib


class InventoryTransferLogger:
    """Custom logger that captures output for Streamlit display"""
    
    def __init__(self):
        self.logs = []
        self.current_step = ""
    
    def log(self, message: str, level: str = "INFO"):
        """Add a log message"""
        timestamp = time.strftime("%H:%M:%S")
        log_entry = {
            "timestamp": timestamp,
            "level": level,
            "message": message,
            "step": self.current_step
        }
        self.logs.append(log_entry)
    
    def set_step(self, step: str):
        """Set the current processing step"""
        self.current_step = step
        self.log(f"Starting: {step}", "STEP")
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
    
    def info(self, message: str):
        """Log an info message"""
        self.log(message, "INFO")
    
    def success(self, message: str):
        """Log a success message"""
        self.log(message, "SUCCESS")
    
    def get_logs(self) -> List[Dict]:
        """Get all log entries"""
        return self.logs
    
    def clear(self):
        """Clear all logs"""
        self.logs = []
        self.current_step = ""


class ActiveInventoryTransfer:
    """Handles active inventory transfer between environments"""
    
    def __init__(self, logger: InventoryTransferLogger):
        self.logger = logger
    
    def is_production(self, url: str) -> bool:
        """Check if environment is production"""
        regex = r"\/\/(\w+)"
        match = re.findall(regex, url)
        if len(match) == 1:
            return match[0].endswith('p')
        return False
    
    def write_inv(self, table_name: str, response: List[Dict]):
        """Write inventory data to SQLite database"""
        conn = sqlite3.connect('staging_table.db')
        cursor = conn.cursor()
        try:
            df = pd.DataFrame(response)
            df = df.filter(["OnHand", "LocationId", "ItemId"])
            df.to_sql(table_name, conn, index=False, if_exists='append')
            self.logger.info(f"Wrote {len(df)} records to {table_name}")
        except Exception as e:
            self.logger.error(f"Error writing to database: {repr(e)}")
        finally:
            conn.close()
    
    def transfer_inventory(self, config: Dict[str, Any]) -> bool:
        """
        Main function to transfer inventory between environments
        
        Args:
            config: Dictionary containing all configuration parameters
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Validate configuration
            required_keys = [
                'zone', 'download_batch_size', 'upload_batch_size',
                'from_env', 'from_org', 'from_facility', 'from_token',
                'to_env', 'to_org', 'to_facility', 'to_token'
            ]
            
            missing_keys = [key for key in required_keys if key not in config]
            if missing_keys:
                self.logger.error(f"Missing required config keys: {', '.join(missing_keys)}")
                return False
            
            # Extract configuration
            zone = config['zone']
            download_batch_size = int(config['download_batch_size'])
            upload_batch_size = int(config['upload_batch_size'])
            
            from_env = config['from_env']
            from_org = config['from_org']
            from_facility = config['from_facility']
            from_token = config['from_token']
            
            to_env = config['to_env']
            to_org = config['to_org']
            to_facility = config['to_facility']
            to_token = config['to_token']
            
            self.logger.set_step("Environment Setup")
            
            # Setup environments
            from_environment = f"https://{from_env}.sce.manh.com"
            active_from = ActiveWM(
                environment=from_environment,
                default_org=from_org,
                default_facility=from_facility,
                manual_token=from_token
            )
            active_from.verbose = False
            
            to_environment = f"https://{to_env}.sce.manh.com"
            active_to = ActiveWM(
                environment=to_environment,
                default_org=to_org,
                default_facility=to_facility,
                manual_token=to_token
            )
            active_to.verbose = False
            
            # Production check
            if self.is_production(active_to.wm_app):
                self.logger.error("Cannot import to production environment")
                return False
            
            self.logger.success(f"Connected to environments: {from_env} -> {to_env}")
            
            # Download inventory data
            self.logger.set_step("Downloading Inventory Data")
            
            data = {
                "LocationQuery": {"Query": f"Zone ={zone} and InventoryReservationTypeId=LOCATION"},
                "Size": 1
            }
            res = active_from.dci.post_inv_search(data)
            total = res.header['totalCount']
            number_of_batches = math.ceil(int(total) / download_batch_size)
            
            self.logger.info(f"Found {total} inventory records to transfer")
            self.logger.info(f"Will process in {number_of_batches} batches of {download_batch_size}")
            
            # Download in batches
            for i in range(number_of_batches):
                self.logger.info(f"Downloading batch {i+1} of {number_of_batches}")
                data = {
                    "LocationQuery": {"Query": f"Zone ={zone} and InventoryReservationTypeId=LOCATION"},
                    "Size": download_batch_size,
                    "Page": i
                }
                res = active_from.dci.post_inv_search(data)
                self.write_inv(f"inventory_transfer_{zone}", res.data)
                time.sleep(2)
            
            # Download and sync items
            self.logger.set_step("Processing Items")
            
            conn = sqlite3.connect('staging_table.db')
            df = pd.read_sql_query(f"select distinct ItemId from inventory_transfer_{zone}", conn)
            conn.close()
            items = list(df.ItemId)
            
            total_items = len(items)
            item_batches = math.ceil(total_items / 50)
            self.logger.info(f"Processing {total_items} unique items in {item_batches} batches")
            
            for i in range(item_batches):
                self.logger.info(f"Processing item batch {i+1} of {item_batches}")
                item_query = items[50*i:50*(i+1)]
                data = {"query": f"ItemId in ({','.join(item_query)})", "size": 50}
                
                res = active_from.itm.search_item(**data)
                self.logger.info(f"Retrieved {len(res.data)} items from source")
                
                res_save = active_to.itm.bulk_import_item(res.data)
                self.logger.info(f"Imported items to target environment")
            
            # Sync items
            self.logger.info("Running item sync")
            res = active_to.itm.custom_search('POST', '/item-master/api/item-master/item/v2/sync', data={})
            self.logger.success("Item sync completed")
            
            # Upload inventory adjustments
            self.logger.set_step("Uploading Inventory Adjustments")
            
            conn = sqlite3.connect('staging_table.db')
            df = pd.read_sql_query(f"select * from inventory_transfer_{zone}", conn)
            records = df.to_dict(orient='records')
            conn.close()
            
            # Prepare inventory adjustment records
            add_inv_template = {
                "SourceContainerId": "DMG-RTN-SORT",
                "SourceLocationId": "DMG-RTN-SORT",
                "SourceContainerType": "LOCATION",
                "TransactionType": "INVENTORY_ADJUSTMENT",
                "ItemId": "32480V4",
                "Quantity": "200",
                "PixEventName": "INVENTORY_ADJUSTMENT",
                "PixTransactionType": "ADJUST_UI"
            }
            
            out_records = []
            for rec in records:
                add_inv = deepcopy(add_inv_template)
                add_inv["SourceContainerId"] = rec["LocationId"]
                add_inv["SourceLocationId"] = rec["LocationId"]
                add_inv["ItemId"] = rec["ItemId"]
                add_inv["Quantity"] = rec["OnHand"]
                out_records.append(add_inv)
            
            total_adjustments = len(out_records)
            adjustment_batches = math.ceil(total_adjustments / upload_batch_size)
            self.logger.info(f"Uploading {total_adjustments} inventory adjustments in {adjustment_batches} batches")
            
            # Save output for reference
            with open('output_inventory.json', 'w') as f:
                json.dump(out_records, f, indent=4)
            self.logger.info("Saved inventory adjustments to output_inventory.json")
            
            # Upload in batches
            current_start = 0
            current_end = current_start + upload_batch_size
            failed_batches = 0
            
            while current_start < total_adjustments:
                batch_end = min(current_end, total_adjustments)
                self.logger.info(f"Uploading batch {current_start}-{batch_end}")
                
                data = out_records[current_start:batch_end]
                
                try:
                    res = active_to.dci.post_absolute_adjust_inventory(json.dumps(data))
                    
                    if res.full_response.status_code != 200:
                        self.logger.error(f"Batch failed with status {res.full_response.status_code}")
                        failed_batches += 1
                    else:
                        self.logger.success(f"Batch {current_start}-{batch_end} uploaded successfully")
                    
                    # Check for failed records
                    try:
                        if res.full_response.json()['data']['FailedRecords']:
                            failed_count = len(res.full_response.json()['data']['FailedRecords'])
                            self.logger.warning(f"Batch had {failed_count} failed records")
                            
                            os.makedirs('Failed', exist_ok=True)
                            with open(f'Failed/batch_{current_start}-{batch_end}.log', 'w') as f:
                                json.dump(res.full_response.json()['data']['FailedRecords'], f, indent=4)
                    except (TypeError, KeyError):
                        pass
                        
                except (requests.exceptions.SSLError, requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
                    self.logger.error(f"Network error: {str(e)}. Retrying in 20 seconds...")
                    time.sleep(20)
                    continue
                
                current_start += upload_batch_size
                current_end += upload_batch_size
            
            # Summary
            self.logger.set_step("Transfer Complete")
            success_batches = adjustment_batches - failed_batches
            self.logger.success(f"Transfer completed: {success_batches}/{adjustment_batches} batches successful")
            
            if failed_batches > 0:
                self.logger.warning(f"{failed_batches} batches had failures - check Failed/ directory")
            
            return failed_batches == 0
            
        except Exception as e:
            self.logger.error(f"Transfer failed: {str(e)}")
            return False


def run_inventory_transfer(config: Dict[str, Any], logger: InventoryTransferLogger) -> bool:
    """
    Main entry point for inventory transfer
    
    Args:
        config: Configuration dictionary
        logger: Logger instance for capturing output
        
    Returns:
        bool: True if successful, False otherwise
    """
    transfer = ActiveInventoryTransfer(logger)
    return transfer.transfer_inventory(config)
