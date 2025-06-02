import streamlit as st

@st.dialog("Generation Template Guide", width="large")
def guide_modal():
    # Modal content
    st.markdown("""
    Generation templates allow you to define how data should be generated for a base template like item or asn.
    **Generation Template Structure:**
    
    **StaticFields:** Fields with fixed values for all records
    ```json
    "StaticFields": {
        "Status": "ACTIVE",
        "Version": 1,
        "IsEnabled": true
    }
    ```
    
    **DynamicFields:** Fields with auto-incrementing prefixes
    ```json
    "DynamicFields": {
        "ItemId": "CM_ITEM",
        "OrderId": "ORDER"
    }
    ```
    
    **RandomFields:** Fields with random values based on type
    ```json
    "RandomFields": [
        {
            "FieldName": "Quantity",
            "FieldType": "int(1,100)"
        },
        {
            "FieldName": "Price", 
            "FieldType": "float(10.0,999.99)"
        },
        {
            "FieldName": "City",
            "FieldType": "choice(Atlanta,New York,Chicago)"
        },
        {
            "FieldName": "CreatedDate",
            "FieldType": "datetime(now)"
        }
    ]
    ```
    
    **LinkedFields:** Fields that copy values from other fields
    ```json
    "LinkedFields": {
        "ItemId": ["PrimaryBarCode", "Description"]
    }
    ```
    
    **Field Types:**
    - `int(min,max)` - Random integer
    - `float(min,max)` - Random decimal  
    - `string(length)` - Random string
    - `choice(opt1,opt2,opt3)` - Random choice
    - `datetime(now|future|past)` - Date/time
    - `boolean` - True/false
    - `uuid` - UUID string
    
    **Nested Fields:** Use dot notation for nested objects/arrays
    - `Address.City` - City in Address object
    - `Items.0.Quantity` - Quantity in first item of Items array
    """)
    
    st.markdown("---")

