"""
UI components for managing endpoint configurations
"""

import streamlit as st
import json
from typing import Dict, Any
from components.config_manager import ConfigurationManager

     
def render_endpoint_configuration_sidebar(config_manager: ConfigurationManager):
    """
    Render endpoint configuration in sidebar
      Args:
        config_manager: ConfigurationManager instance
    """

    with st.sidebar:
        st.subheader("🔧 Endpoint Configuration")
        
        # Show configuration management options
        with st.expander("Manage Endpoints", expanded=False):
            
              # Global Configuration Section
            st.markdown("### 🌐 Global Configuration")
            
            # Base URL configuration
            current_base_url = config_manager.get_base_url()
            new_base_url = st.text_input(
                "Base URL",
                value=current_base_url,
                help="The base URL for all API endpoints",
                key="global_base_url"
            )            # Shared token configuration
            current_token = config_manager.get_shared_token()
            # Remove 'Bearer ' prefix for display
            display_token = current_token.replace('Bearer ', '') if current_token.startswith('Bearer ') else current_token
            new_token = st.text_input(
                "Bearer Token",
                value=display_token,
                type="password",
                help="Environment API token",
                key="global_shared_token",
            )
            
            # Organization configuration
            current_organization = config_manager.get_selected_organization()
            new_organization = st.text_input(
                "Selected Organization",
                value=current_organization,
                help="Organization value for API headers",
                key="global_organization"
            )
              # Facility configuration
            current_facility = config_manager.get_selected_facility()            
            new_facility = st.text_input(
                "Selected Facility",
                value=current_facility,
                help="Facility value for API headers",
                key="global_facility"
            )
            
            try:
                config_saved = False
                if new_base_url != current_base_url:
                    config_manager.set_base_url(new_base_url)
                    config_saved = True
                if new_token != display_token:
                    config_manager.set_shared_token(new_token)
                    config_saved = True
                if new_organization != current_organization:
                    config_manager.set_selected_organization(new_organization)
                    config_saved = True
                if new_facility != current_facility:
                    config_manager.set_selected_facility(new_facility)
                    config_saved = True
                if config_saved:
                    st.rerun()
            except ValueError as e:
                # Show production URL error
                st.error(str(e))
            except Exception as e:
                st.error(f"Error saving configuration: {e}")
                        
            st.markdown("---")
            
            # Template-specific configuration
            st.markdown("### 📋 Template-Specific Configuration")
            
            # Template selection for configuration
            available_templates = config_manager.get_all_templates()
            if available_templates:
                selected_template = st.selectbox(
                    "Configure Template", 
                    available_templates,
                    key="config_template_select"
                )
                
                if selected_template:
                    render_template_endpoint_config(config_manager, selected_template)
            
            st.markdown("---")
              # Import/Export functionality
            st.markdown("### 📤 Export Configuration")
            
            # Export options
            st.download_button(
                label="💾 Download Full Config",
                data=config_manager.export_full_config(),
                help="Download the full configuration including all endpoints and global settings",
                file_name="full_config.json",
                mime="application/json",
                key="download_full"
            )
            
            # Reset option
            if st.button("🔄 Reset All", help="Reset all configurations to defaults"):
                config_manager.clear_all_user_config()
                st.success("All configurations reset to defaults!")
                st.rerun()
            
            # Import configuration
            st.markdown("### 📥 Import Configuration")
            st.markdown("**Upload Configuration File:**")
            st.session_state.uploading = False
            uploaded_file = st.file_uploader(
                "Choose config file", 
                type=['json'],
                key="config_upload",
                help="Upload a previously exported configuration file (supports both formats)"
            )
            
            # Initialize session state for file processing tracking
            if "last_processed_file" not in st.session_state:
                st.session_state.last_processed_file = None
            
            if uploaded_file is not None:
                if st.session_state.last_processed_file != uploaded_file.file_id:
                    try:
                        config_content = uploaded_file.read().decode('utf-8')
                        
                        # Try to determine the format
                        import json
                        config_data = json.loads(config_content)
                        # Check if it's the new full format
                        if isinstance(config_data, dict):
                            # Full configuration format
                            st.info("📦 Detected full configuration format - importing global settings and endpoints")
                            import_success = config_manager.import_full_config(config_content)
                        
                        if import_success:
                            # Mark this file as processed
                            st.session_state.last_processed_file = uploaded_file.file_id
                            st.session_state.uploading = False
                            # Delay the rerun to allow success message to display
                            st.rerun()
                        else:
                            st.error("Failed to import configuration")
                            
                    except json.JSONDecodeError:
                        st.error("Invalid JSON file format")
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
                else:
                    # File already processed, show status
                    st.success("Configuration imported successfully!")


def render_template_endpoint_config(config_manager: ConfigurationManager, template_name: str):
    """
    Render configuration form for a specific template
    
    Args:
        config_manager: ConfigurationManager instance
        template_name: Name of the template to configure
    """
    st.markdown(f"**Configure: {template_name.replace('_', ' ').title()}**")
    
    # Get current configuration
    current_config = config_manager.get_template_config(template_name)
    
    # Display current payload wrapping settings
    type_value = current_config.get('type', 'none')
    wrapper_value = current_config.get('dataWrapper', False)
    
    # Show payload structure preview
    if type_value == 'xint' and wrapper_value:
        payload_preview = '{"Payload": {"data": [records]}}'
        preview_color = "blue"
    elif type_value == 'xint':
        payload_preview = '{"Payload": [records]}'
        preview_color = "green"
    elif wrapper_value:
        payload_preview = '{"data": [records]}'
        preview_color = "orange"
    else:
        payload_preview = '[records]'
        preview_color = "gray"
    
    
    # Configuration form
    with st.form(key=f"config_form_{template_name}"):
        endpoint = st.text_input(
            "Endpoint URL",
            value=current_config.get('endpoint', ''),
            help="The API endpoint URL for this template type"
        )
          # Type selection for payload wrapping
        type_options = ["none", "xint", "array"]
        current_type = current_config.get('type', 'none')
        selected_type = st.selectbox(
            "Payload Type",
            options=type_options,
            index=type_options.index(current_type) if current_type in type_options else 0,
            help="Type of payload wrapping:\n• 'xint' wraps in {\"Payload\": ...} for XINT endpoints\n• 'array' sends as array (same as none currently)\n• 'none' sends raw data without wrapper"
        )
        
        # Add explanation for each type
        data_wrapper = st.checkbox(
            "Data Wrapper",
            value=current_config.get('dataWrapper', False),
            help="When enabled, wraps records in {\"data\": [records]} structure"
        )
                
        # Show real-time preview of payload structure
        st.markdown("**Payload Preview:**")
        if selected_type == 'xint' and data_wrapper:
            preview_text = '```json\n{"Payload": {"data": [records]}}\n```'
            preview_color = "blue"
        elif selected_type == 'xint':
            preview_text = '```json\n{"Payload": [records]}\n```'
            preview_color = "green"
        elif data_wrapper:
            preview_text = '```json\n{"data": [records]}\n```'
            preview_color = "orange"
        else:
            preview_text = '```json\n[records]\n```'
            preview_color = "gray"
        
        st.markdown(preview_text)
        
        # Description
        description = st.text_input(
            "Description",
            value=current_config.get('description', f'Endpoint for {template_name} data'),
            help="Description of this endpoint configuration"
        )        
        # Form buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.form_submit_button("💾 Save", type="primary"):
                try:
                    # Validate configuration
                    if not endpoint.strip():
                        st.error("❌ Endpoint URL cannot be empty")
                        return
                    
                    # Show warning for certain combinations
                    if selected_type == "array" and data_wrapper:
                        st.warning("⚠️ Array type with data wrapper may result in double-wrapping")
                    
                    new_config = {
                        'endpoint': endpoint,
                        'type': selected_type if selected_type != 'none' else None,
                        'dataWrapper': data_wrapper,
                        'description': description
                    }
                    
                    # Remove None values to keep config clean
                    new_config = {k: v for k, v in new_config.items() if v is not None}
                    
                    # Save configuration
                    config_manager.update_template_config(template_name, new_config)
                    st.success(f"✅ Configuration saved for {template_name}!")
                    
                    # Show what was saved
                    st.json(new_config)
                    
                    st.rerun()
                    
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in additional headers")
                except Exception as e:
                    st.error(f"Error saving configuration: {e}")
        
        with col2:
            if st.form_submit_button("🔄 Reset"):
                config_manager.reset_template_config(template_name)
                st.success(f"Configuration reset to default for {template_name}!")
                st.rerun()
        
