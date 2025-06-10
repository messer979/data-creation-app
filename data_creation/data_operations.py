"""
Data generation operations and business logic
"""

import streamlit as st
from typing import List, Dict, Any
from data_creation.api_operations import send_data_to_api
from components.config_manager import ConfigurationManager

def handle_generate_button_click(selected_template: str,
                                count: int,
                                template_params: Dict[str, Any],
                                send_to_api: bool,
                                config_manager: ConfigurationManager,
                                batch_size: int,
                                template_editor_result: Dict[str, Any] = None) -> bool:
    """
    Handle the generate data button click logic
    
    Args:
        selected_template: Selected template name
        count: Number of records to generate
        template_params: Template-specific parameters
        send_to_api: Whether to send data to API
        config_manager: Configuration manager for endpoints        
        batch_size: Batch size for API calls
        template_editor_result: Result from template editor with edited template and validation status
    
    Returns:
        bool: True if generation was successful, False otherwise
    """
    with st.spinner("Generating data..."):
        try:
            # Store original template for restoration later
            original_template = None
            template_generator = st.session_state.data_gen.get_template_generator()
            
            # If template has been edited, use it temporarily for generation without saving
            if (template_editor_result and 
                template_editor_result.get('is_valid', False) and
                template_editor_result.get('template_changed', False)):
                
                # Store original template
                original_template = template_generator.generation_templates.get(selected_template)
                
                # Temporarily update the in-memory template for generation
                template_generator.generation_templates[selected_template] = template_editor_result['template']
                
            
            # Always use generation template system for data creation
            generated_data = st.session_state.data_gen.generate_data(
                selected_template, count, **template_params
            )
            
            # Restore original template if it was temporarily modified
            if original_template is not None:
                template_generator.generation_templates[selected_template] = original_template
                
        except ValueError as e:
            st.error(f"❌ Error generating data: {str(e)}")
            st.info("Please check that the required template file exists in the 'templates' directory.")
            return False
        
        if generated_data:
            # Store in session state
            st.session_state.generated_data = generated_data
            st.session_state.data_type = selected_template
            st.success(f"✅ Generated {len(generated_data)} records!")
              # Send to API if requested
            if send_to_api:
                # Get template-specific endpoint, headers, and configuration
                api_endpoint = config_manager.get_endpoint_for_template(selected_template)
                api_headers = config_manager.get_headers_for_template(selected_template)
                template_config = config_manager.get_template_config(selected_template)
                
                api_results = send_data_to_api(
                    generated_data, 
                    api_endpoint, 
                    api_headers,
                    batch_size,
                    template_config
                )
                st.session_state.api_results = api_results
                return True
    
    return False


def extract_template_parameters(selected_template: str) -> Dict[str, Any]:
    """
    Extract template-specific parameters from Streamlit widgets
    
    Args:
        selected_template: Selected template name
    
    Returns:
        Dictionary of template parameters
    """
    params = {}
    
    if selected_template == 'facility':
        params['base_name'] = st.session_state.get('facility_base_name', 'STORE')
        
    elif selected_template == 'item':
        params['prefix'] = st.session_state.get('item_prefix', 'ITEM')
        
    elif selected_template == 'po':
        vendor_ids_input = st.session_state.get('vendor_ids_input', 'VENDOR001,VENDOR002')
        item_ids_input = st.session_state.get('item_ids_input', 'ITEM001,ITEM002')
        params['vendor_ids'] = [v.strip() for v in vendor_ids_input.split(',') if v.strip()]
        params['item_ids'] = [i.strip() for i in item_ids_input.split(',') if i.strip()]
        params['facility_id'] = st.session_state.get('facility_id', 'FACILITY01')
    
    return params
