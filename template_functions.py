"""
Functional template processing utilities
Contains pure functions for applying generation template rules to data
"""

import json
import random
import string
import uuid
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from copy import deepcopy


def apply_static_fields(record: Dict[str, Any], static_fields: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply static field values to a record
    
    Args:
        record: The record to modify
        static_fields: Dictionary of field_name -> static_value
    
    Returns:
        Modified record
    """
    for field, value in static_fields.items():
        set_nested_field(record, field, value)
    return record


def process_dynamic_field_keywords(prefix: str) -> str:
    """
    Process keyword variables in dynamic field prefixes
    
    Args:
        prefix: The prefix string that may contain keyword variables
    
    Returns:
        Processed prefix with keyword variables replaced
    """
    processed = prefix
    
    # Replace {{dttm}} with current date in MMDD format
    if '{{dttm}}' in processed:
        current_date = datetime.now().strftime('%m%d')
        processed = processed.replace('{{dttm}}', current_date)
    return processed


def apply_dynamic_fields(record: Dict[str, Any], 
                        dynamic_fields: Dict[str, str], 
                        dynamic_counters: Dict[str, int]) -> Dict[str, Any]:
    """
    Apply dynamic (incremental) field values to a record
    
    Args:
        record: The record to modify
        dynamic_fields: Dictionary of field_name -> prefix (supports {{dttm}} for current date MMDD)
        dynamic_counters: Mutable dictionary tracking counters for each field
    
    Returns:
        Modified record
    """
    for field, prefix in dynamic_fields.items():
        if field not in dynamic_counters:
            dynamic_counters[field] = 1
        else:
            dynamic_counters[field] += 1
        
        # Process keyword variables in prefix
        processed_prefix = process_dynamic_field_keywords(prefix)
        
        generated_value = f"{processed_prefix}_{dynamic_counters[field]:03d}"
        set_nested_field(record, field, generated_value)
    
    return record


def apply_random_fields(record: Dict[str, Any], random_fields: List[Dict[str, str]]) -> Dict[str, Any]:
    """
    Apply random field values to a record
    
    Args:
        record: The record to modify
        random_fields: List of field specifications with FieldName and FieldType
    
    Returns:
        Modified record
    """
    for field_spec in random_fields:
        field_name = field_spec['FieldName']
        field_type = field_spec['FieldType']
        random_value = generate_random_value(field_type)
        set_nested_field(record, field_name, random_value)
    
    return record


def apply_linked_fields(record: Dict[str, Any], linked_fields: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Apply linked field values derived from other fields
    
    Args:
        record: The record to modify
        linked_fields: Dictionary of source_field -> [linked_field_names]
    
    Returns:
        Modified record
    """
    for source_field, linked_field_names in linked_fields.items():
        source_value = get_nested_field(record, source_field)
        if source_value:
            for linked_field in linked_field_names:
                linked_value = generate_linked_value(source_value, linked_field)
                set_nested_field(record, linked_field, linked_value)
    
    return record


def set_nested_field(obj: Dict[str, Any], field_path: str, value: Any) -> None:
    """
    Set a nested field using dot notation
    
    Args:
        obj: Object to modify
        field_path: Dot notation path (e.g., "AsnLine.ItemId")
        value: Value to set
    """
    parts = field_path.split('.')
    current = obj
    
    for part in parts[:-1]:
        if isinstance(current, dict):
            if part not in current:
                current[part] = {}
            current = current[part]
        else:
            # This shouldn't happen in well-formed paths
            raise ValueError(f"Expected dict but found {type(current)} at path part '{part}'")
    
    # Set the final value
    final_field = parts[-1]
    if isinstance(current, dict):
        current[final_field] = value
    else:
        raise ValueError(f"Expected dict but found {type(current)} for field '{final_field}'")


def get_nested_field(obj: Dict[str, Any], field_path: str) -> Any:
    """
    Get a nested field using dot notation
    
    Args:
        obj: Object to read from
        field_path: Dot notation path (e.g., "AsnLine.ItemId")
    
    Returns:
        Field value or None if not found
    """
    parts = field_path.split('.')
    current = obj
    
    for part in parts:
        # Handle dictionary key access only
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    
    return current


def generate_random_value(field_type: str) -> Any:
    """
    Generate a random value based on field type specification
    
    Args:
        field_type: Type specification string (e.g., "float(2,3)", "string(12)", "boolean")
    
    Returns:
        Generated random value    """    # Parse field type patterns
    if field_type.startswith('float('):
        # Try float(low,high,precision) first - with whitespace handling
        match = re.match(r'float\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*,\s*(\d+)\s*\)', field_type)
        if match:
            low_val, high_val, precision = float(match.group(1)), float(match.group(2)), int(match.group(3))
            return round(random.uniform(low_val, high_val), precision)
        
        # Try float(low,high) with default precision - with whitespace handling
        match = re.match(r'float\(\s*([0-9.]+)\s*,\s*([0-9.]+)\s*\)', field_type)
        if match:
            low_val, high_val = float(match.group(1)), float(match.group(2))
            return round(random.uniform(low_val, high_val), 2)  # Default to 2 decimal places
    
    elif field_type == 'float':
        # Simple float type without parameters (0.0 to 100.0 with 2 decimal places)
        return round(random.uniform(0.0, 100.0), 2)
    
    elif field_type.startswith('int('):
        # int(min,max) - with whitespace handling
        match = re.match(r'int\(\s*(\d+)\s*,\s*(\d+)\s*\)', field_type)
        if match:
            min_val, max_val = int(match.group(1)), int(match.group(2))
            return random.randint(min_val, max_val)
    
    elif field_type.startswith('string('):
        # string(length) - with whitespace handling
        match = re.match(r'string\(\s*(\d+)\s*\)', field_type)
        if match:
            length = int(match.group(1))
            return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    
    elif field_type == 'boolean':
        return random.choice([True, False])
    
    elif field_type.startswith('datetime('):
        # datetime(now), datetime(past), datetime(future) - with whitespace handling
        match = re.match(r'datetime\(\s*(\w+)\s*\)', field_type)
        if match:
            time_type = match.group(1)            
            if time_type == 'now':
                return datetime.now().isoformat()
            elif time_type == 'past':
                days_ago = random.randint(1, 365)
                past_date = datetime.now() - timedelta(days=days_ago)
                return past_date.isoformat()
            elif time_type == 'future':
                days_ahead = random.randint(1, 365)
                future_date = datetime.now() + timedelta(days=days_ahead)
                return future_date.isoformat()
    
    elif field_type.startswith('choice('):
        # choice(option1,option2,option3) - with whitespace handling
        match = re.match(r'choice\(\s*([^)]+)\s*\)', field_type)
        if match:
            choices = [choice.strip() for choice in match.group(1).split(',')]
            return random.choice(choices)
    
    elif field_type == 'uuid':
        return str(uuid.uuid4())
    
    elif field_type == 'email':
        domains = ['example.com', 'test.com', 'demo.org']
        username = ''.join(random.choices(string.ascii_lowercase, k=8))
        return f"{username}@{random.choice(domains)}"
    
    # Default fallback
    return f"RANDOM_{random.randint(1000, 9999)}"


def generate_linked_value(source_value: str, linked_field: str) -> str:
    """
    Generate linked field values based on source field
    
    Args:
        source_value: Value from the source field
        linked_field: Name of the field to generate
    
    Returns:
        Generated linked value
    """
    return f"{source_value}"


def deep_copy_template(obj: Any) -> Any:
    """
    Deep copy object while preserving placeholder strings and structure
    
    Args:
        obj: Object to copy
    
    Returns:
        Deep copy of the object
    """
    if isinstance(obj, dict):
        return {k: deep_copy_template(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [deep_copy_template(item) for item in obj]
    else:
        return obj


def create_record_from_template(base_template: Dict[str, Any], 
                              generation_template: Dict[str, Any],
                              index: int,
                              dynamic_counters: Dict[str, int]) -> Dict[str, Any]:
    """
    Create a single record by applying generation template rules to base template
    
    Args:
        base_template: Base JSON template structure
        generation_template: Generation rules template
        index: Record index (0-based)
        dynamic_counters: Mutable dictionary tracking dynamic field counters
    
    Returns:
        Generated record
    """    # Start with a deep copy of the base template
    record = deep_copy_template(base_template)
    
    # Get array lengths configuration
    array_lengths = generation_template.get('ArrayLengths', {})
    
    # Initialize arrays to the specified lengths before processing fields
    for array_name, array_length in array_lengths.items():
        if array_name in record and isinstance(record[array_name], list):
            # Expand existing array
            current_length = len(record[array_name])
            if current_length < array_length:
                # Use the first element as a template for new elements
                template_element = record[array_name][0] if current_length > 0 else {}
                for i in range(current_length, array_length):
                    record[array_name].append(deep_copy_template(template_element))
            elif current_length > array_length:
                # Truncate array if it's longer than needed
                record[array_name] = record[array_name][:array_length]
        elif array_name not in record:
            # Create new array with empty objects
            record[array_name] = [{} for _ in range(array_length)]
    
    # Apply static fields with array handling
    if 'StaticFields' in generation_template:
        record = apply_static_fields_with_arrays(record, generation_template['StaticFields'], array_lengths)
    
    # Apply dynamic fields with array handling
    if 'DynamicFields' in generation_template:
        record = apply_dynamic_fields_with_arrays(record, generation_template['DynamicFields'], dynamic_counters, array_lengths)
    
    # Apply random fields with array handling
    if 'RandomFields' in generation_template:
        record = apply_random_fields_with_arrays(record, generation_template['RandomFields'], array_lengths)
    
    # Apply linked fields with array handling
    if 'LinkedFields' in generation_template:
        record = apply_linked_fields_with_arrays(record, generation_template['LinkedFields'], array_lengths)
    
    return record


def expand_fields_for_arrays(fields: Dict[str, Any], array_lengths: Dict[str, int]) -> Dict[str, Any]:
    """
    Since arrays are handled iteratively, just return fields as-is
    
    Args:
        fields: Dictionary of field definitions
        array_lengths: Dictionary of array_name -> length mappings (not used)
    
    Returns:
        Original fields dictionary unchanged
    """
    return fields


def expand_random_fields_for_arrays(random_fields: List[Dict[str, str]], array_lengths: Dict[str, int]) -> List[Dict[str, str]]:
    """
    Since arrays are handled iteratively, just return random fields as-is
    
    Args:
        random_fields: List of random field specifications
        array_lengths: Dictionary of array_name -> length mappings (not used)
    
    Returns:
        Original random fields list unchanged
    """
    return random_fields


def expand_linked_fields_for_arrays(linked_fields: Dict[str, List[str]], array_lengths: Dict[str, int]) -> Dict[str, List[str]]:
    """
    Since arrays are handled iteratively, just return linked fields as-is
    
    Args:
        linked_fields: Dictionary of source_field -> [linked_field_names]
        array_lengths: Dictionary of array_name -> length mappings (not used)
    
    Returns:
        Original linked fields dictionary unchanged
    """
    return linked_fields


def apply_static_fields_with_arrays(record: Dict[str, Any], 
                                   static_fields: Dict[str, Any], 
                                   array_lengths: Dict[str, int]) -> Dict[str, Any]:
    """
    Apply static field values to a record, handling array fields by iterating over array elements
    
    Args:
        record: The record to modify
        static_fields: Dictionary of field_name -> static_value
        array_lengths: Dictionary of array_name -> length mappings
    
    Returns:
        Modified record
    """
    for field, value in static_fields.items():
        if '.' in field:
            # Check if this field references an array
            array_field = None
            for array_name in array_lengths.keys():
                if field.startswith(f"{array_name}."):
                    array_field = array_name
                    break
            
            if array_field and array_field in record and isinstance(record[array_field], list):
                # This is an array field - apply to all array elements
                field_suffix = field[len(array_field) + 1:]  # Remove "ArrayName." prefix
                for array_element in record[array_field]:
                    if isinstance(array_element, dict):
                        set_nested_field(array_element, field_suffix, value)
            else:
                # Regular nested field
                set_nested_field(record, field, value)
        else:
            # Simple field
            set_nested_field(record, field, value)
    
    return record


def apply_dynamic_fields_with_arrays(record: Dict[str, Any], 
                                   dynamic_fields: Dict[str, str], 
                                   dynamic_counters: Dict[str, int],
                                   array_lengths: Dict[str, int]) -> Dict[str, Any]:
    """
    Apply dynamic field values to a record, handling array fields by iterating over array elements
    
    Args:
        record: The record to modify
        dynamic_fields: Dictionary of field_name -> prefix
        dynamic_counters: Mutable dictionary tracking counters for each field
        array_lengths: Dictionary of array_name -> length mappings
    
    Returns:
        Modified record
    """
    for field, prefix in dynamic_fields.items():
        # Process keyword variables in prefix
        processed_prefix = process_dynamic_field_keywords(prefix)
        
        if '.' in field:
            # Check if this field references an array
            array_field = None
            for array_name in array_lengths.keys():
                if field.startswith(f"{array_name}."):
                    array_field = array_name
                    break
            
            if array_field and array_field in record and isinstance(record[array_field], list):
                # This is an array field - increment per element within this record
                field_suffix = field[len(array_field) + 1:]  # Remove "ArrayName." prefix
                
                for i, array_element in enumerate(record[array_field]):
                    if isinstance(array_element, dict):
                        # For array elements, use per-record indexing (1-based)
                        element_value = f"{processed_prefix}_{i + 1:03d}"
                        set_nested_field(array_element, field_suffix, element_value)
            else:
                # Regular nested field - use global counter
                if field not in dynamic_counters:
                    dynamic_counters[field] = 1
                else:
                    dynamic_counters[field] += 1
                
                generated_value = f"{processed_prefix}_{dynamic_counters[field]:03d}"
                set_nested_field(record, field, generated_value)
        else:
            # Simple field - use global counter
            if field not in dynamic_counters:
                dynamic_counters[field] = 1
            else:
                dynamic_counters[field] += 1
            
            generated_value = f"{processed_prefix}_{dynamic_counters[field]:03d}"
            set_nested_field(record, field, generated_value)
    
    return record


def apply_random_fields_with_arrays(record: Dict[str, Any], 
                                  random_fields: List[Dict[str, str]],
                                  array_lengths: Dict[str, int]) -> Dict[str, Any]:
    """
    Apply random field values to a record, handling array fields by iterating over array elements
    
    Args:
        record: The record to modify
        random_fields: List of field specifications with FieldName and FieldType
        array_lengths: Dictionary of array_name -> length mappings
    
    Returns:
        Modified record
    """
    for field_spec in random_fields:
        field_name = field_spec['FieldName']
        field_type = field_spec['FieldType']
        
        if '.' in field_name:
            # Check if this field references an array
            array_field = None
            for array_name in array_lengths.keys():
                if field_name.startswith(f"{array_name}."):
                    array_field = array_name
                    break
            
            if array_field and array_field in record and isinstance(record[array_field], list):
                # This is an array field - apply to all array elements with different random values
                field_suffix = field_name[len(array_field) + 1:]  # Remove "ArrayName." prefix
                for array_element in record[array_field]:
                    if isinstance(array_element, dict):
                        random_value = generate_random_value(field_type)
                        set_nested_field(array_element, field_suffix, random_value)
            else:
                # Regular nested field
                random_value = generate_random_value(field_type)
                set_nested_field(record, field_name, random_value)
        else:
            # Simple field
            random_value = generate_random_value(field_type)
            set_nested_field(record, field_name, random_value)
    
    return record


def apply_linked_fields_with_arrays(record: Dict[str, Any], 
                                  linked_fields: Dict[str, List[str]],
                                  array_lengths: Dict[str, int]) -> Dict[str, Any]:
    """
    Apply linked field values derived from other fields, handling array fields by iterating over array elements
    
    Args:
        record: The record to modify
        linked_fields: Dictionary of source_field -> [linked_field_names]
        array_lengths: Dictionary of array_name -> length mappings
    
    Returns:
        Modified record
    """
    for source_field, linked_field_names in linked_fields.items():
        source_value = get_nested_field(record, source_field)
        if source_value:
            for linked_field in linked_field_names:
                linked_value = generate_linked_value(source_value, linked_field)
                
                if '.' in linked_field:
                    # Check if this field references an array
                    array_field = None
                    for array_name in array_lengths.keys():
                        if linked_field.startswith(f"{array_name}."):
                            array_field = array_name
                            break
                    
                    if array_field and array_field in record and isinstance(record[array_field], list):
                        # This is an array field - apply to all array elements
                        field_suffix = linked_field[len(array_field) + 1:]  # Remove "ArrayName." prefix
                        for array_element in record[array_field]:
                            if isinstance(array_element, dict):
                                set_nested_field(array_element, field_suffix, linked_value)
                    else:
                        # Regular nested field
                        set_nested_field(record, linked_field, linked_value)
                else:
                    # Simple field
                    set_nested_field(record, linked_field, linked_value)
    
    return record
