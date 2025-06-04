import streamlit as st

@st.dialog("Data Creation Tool - Help Guide", width="large")
def guide_modal():
    """Comprehensive help guide for the Data Creation Tool"""
    
    # Create tabs for different help sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Overview", 
        "🔧 Endpoint Config", 
        "📝 Generation Templates", 
        "🛠️ Template Manager"
    ])
    
    with tab1:
        st.markdown("""
        ## 🚀 Data Creation Tool Overview
        
        *This tool was built heavily relying on AI. Please report any issues or suggestions to cmesser.*
        
        ### Key Features:
        - **Generate structured test data** from JSON templates
        - **Send data to APIs** with configurable endpoints and authentication
        - **Customize data patterns** using generation templates
        - **Manage multiple templates** with bulk operations
        - **Configure API endpoints** per template type
        
        ### Basic Workflow:
        1. **Select a data template** (ASN, PO, Items, etc.)
        2. **Configure generation parameters** (count, template settings)
        3. **Set up API endpoints** (optional)
        4. **Generate and send data** to your target system
        
        ### Main Sections:
        - **📊 Data Generation**: Main interface for creating data
        - **🔧 Endpoint Config**: Configure API endpoints and authentication
        - **📝 Generation Templates**: Define how data should be generated
        - **🛠️ Template Manager**: Manage and edit templates
        """)
    
    with tab2:
        st.markdown("""
        ## 🔧 Endpoint Configuration
        
        The Endpoint Configuration section allows you to set up API endpoints for each template type.
        
        ### Configuration Options:
        
        **🌐 Global Settings:**
        - **Base URL**: The root URL for your API (e.g., `https://api.example.com`)
        - **Auth Token**: Authentication token for API requests
        - **Organization**: Default organization value
        - **Facility**: Default facility value
        
        **📡 Template-Specific Endpoints:**
        - **Endpoint URL**: Specific endpoint path for each template type
        - **Payload Wrapping**: Choose how data is packaged:
          - **XINT Mode**: Wraps data in `{"Payload": {...}}`
          - **Data Wrapper**: Wraps records in `{"data": [records]}`
          - **Raw Mode**: Sends data as direct array
        
        ### How to Configure:
        1. **Set Global Settings** in the sidebar
        2. **Configure specific endpoints** for each template type
        3. **Choose payload format** based on your API requirements
        4. **Test connections** using the preview functionality
        
        ### Authentication:
        - Set your auth token in the global configuration
        - Token is automatically included in all API requests
        - Supports Bearer token authentication
        """)
    
    with tab3:
        st.markdown("""
        ## 📝 Generation Templates
        
        Generation templates define how data should be generated for base templates. They control field values, randomization, and data patterns.
        
        ### Template Structure:
        
        **📌 StaticFields:** Fixed values for all records
        ```json
        "StaticFields": {
            "Status": "ACTIVE",
            "Version": 1,
            "IsEnabled": true
        }
        ```
        
        **🔢 DynamicFields:** Auto-incrementing values
        ```json
        "DynamicFields": {
            "ItemId": "CM_ITEM",
            "OrderId": "ORDER_{{dttm}}"
        }
        ```
        - `{{dttm}}` gets replaced with current date MMDD format
        - Fields increment automatically: `CM_ITEM_001`, `CM_ITEM_002`, etc.
        - **Array fields** increment per-record: Each ASN's lines start at 1
        
        **🎲 RandomFields:** Random values based on type
        ```json
        "RandomFields": [
            {
                "FieldName": "Quantity",
                "FieldType": "int(1,100)"
            },
            {
                "FieldName": "Price",
                "FieldType": "float(10.0,99.99,2)"
            },
            {
                "FieldName": "City",
                "FieldType": "choice(Atlanta,New York,Chicago)"
            },
            {
                "FieldName": "CreatedDate",
                "FieldType": "datetime(future)"
            }
        ]
        ```
        
        **🔗 LinkedFields:** Copy values between fields
        ```json
        "LinkedFields": {
            "ItemId": ["PrimaryBarCode", "Description"]
        }
        ```
        
        **📊 ArrayLengths:** Define array sizes for automatic expansion
        ```json
        "ArrayLengths": {
            "AsnLine": 2,
            "OrderLines": 3
        }
        ```
        - When defined, `AsnLine.ItemId` automatically applies to all array elements
        - No need to manually specify `AsnLine.0.ItemId`, `AsnLine.1.ItemId`
          ### Field Types:
        - `int(min,max)` - Random integer
        - `float(min,max,precision)` - Random decimal with specified precision
        - `string(length)` - Random alphanumeric string
        - `choice(opt1,opt2,opt3)` - Random selection from options
        - `choiceUnique(opt1,opt2,opt3)` - Unique selection within array siblings (auto-fallback when exhausted)
        - `datetime(now|future|past)` - Date/time generation
        - `boolean` - True/false values
        - `uuid` - UUID string generation
        
        ### Nested Fields:
        Use dot notation for nested objects and arrays:
        - `Address.City` - City field in Address object
        - `AsnLine.ItemId` - ItemId in AsnLine array (auto-expands with ArrayLengths)
        """)
    
    with tab4:
        st.markdown("""
        ## 🛠️ Template Manager
        
        The Template Manager provides tools for managing, editing, and organizing your generation templates.
        
        ### Features:
        
        **📝 Template Editing:**
        - **Visual editor** for generation templates
        - **JSON syntax validation** with error checking
        - **Live preview** of template structure
        - **Field validation** for proper formatting
        
        **📥📤 Bulk Operations:**
        - **Export templates** to backup files
        - **Import templates** from backup files
        - **Bulk editing** across multiple templates
        - **Template validation** during import/export
        
        **🔍 Template Analysis:**
        - **View template structure** and field definitions
        - **Dependency checking** for linked fields
        - **Array configuration** validation
        - **Field type verification**
        
        ### How to Use:
        
        **Editing Templates:**
        1. Click **🛠️ Template Manager** in the sidebar
        2. **Select a template** to edit
        3. **Modify the JSON** structure as needed
        4. **Validate and save** your changes
        
        **Bulk Management:**
        1. Use **Export** to backup your templates
        2. **Edit multiple templates** offline if needed
        3. Use **Import** to restore or update templates
        4. **Validate** templates after import
        
        **Best Practices:**
        - **Backup templates** before major changes
        - **Test templates** with small record counts first
        - **Use consistent naming** for fields across templates
        - **Document custom field types** and their purposes
        - **Validate ArrayLengths** match your base template structure
        
        ### Template Validation:
        The manager automatically checks for:
        - **Valid JSON syntax**
        - **Required field structures**
        - **Field type formatting**
        - **ArrayLengths consistency**
        - **LinkedFields dependencies**
        """)
    
    st.markdown("---")
    st.markdown("💡 **Tip**: Use the different tabs above to learn about specific features of the Data Creation Tool.")
    st.markdown("🔄 **Need help?** Try generating a small batch of records first to test your configuration.")

