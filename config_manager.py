"""
Configuration manager for handling template-to-endpoint mappings
Supports default configurations and user-customized configurations with session state
"""

import json
import streamlit as st
from typing import Dict, Any, Optional
import os
import re
from copy import deepcopy


class ConfigurationManager:
    """Manages template-to-endpoint configuration with session state persistence"""
    
    def __init__(self, config_file: str = "configuration.json"):
        self.config_file = config_file
        self.default_endpoints = {}
        self.default_headers = {}
        self.user_config = {}
        self.base_url = ""
        self.shared_token = "Bearer YOUR_API_TOKEN"
        self.selected_organization = "organization"
        self.selected_facility = "facility"
        
        self.load_default_endpoints()
        self.load_user_config()
        
    def load_default_endpoints(self):
        """Load default configuration from JSON file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.default_endpoints = config_data.get('default_endpoints', {})
                    self.base_url = config_data.get('base_url', 'https://api.example.com')
                    self.default_headers = config_data.get('default_headers', {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer YOUR_API_TOKEN'
                    })
                    
                    # Extract shared token from default headers if available
                    if 'Authorization' in self.default_headers:
                        self.shared_token = self.default_headers['Authorization']
                    # Extract organization and facility from default headers if available
                    if 'SelectedOrganization' in self.default_headers:
                        self.selected_organization = self.default_headers['SelectedOrganization']
                    if 'SelectedLocation' in self.default_headers:
                        self.selected_facility = self.default_headers['SelectedLocation']
            else:
                st.warning(f"Configuration file {self.config_file} not found. Using empty default config.")
                self.default_endpoints = {}
                self.base_url = 'https://api.example.com'
                self.default_headers = {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer YOUR_API_TOKEN'
                }
        except Exception as e:
            st.error(f"Error loading configuration file: {e}")
            self.default_endpoints = {}
            self.base_url = 'https://api.example.com'
            self.default_headers = {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer YOUR_API_TOKEN'
            }
    
    def load_user_config(self):
        """Load user-customized configuration from session state"""
        # Load from session state
        self.user_config = st.session_state.get('user_endpoint_config', self.default_endpoints)
        # Load other settings from session state
        self.base_url = st.session_state.get('base_url', self.base_url)
        self.shared_token = st.session_state.get('shared_token', self.shared_token)
        self.selected_organization = st.session_state.get('selected_organization', self.selected_organization)
        self.selected_facility = st.session_state.get('selected_facility', self.selected_facility)
        
    def save_user_config(self):
        """Save user configuration to session state"""
        # Save to session state
        st.session_state.user_endpoint_config = self.user_config
        st.session_state.base_url = self.base_url
        st.session_state.shared_token = self.shared_token
        st.session_state.selected_organization = self.selected_organization
        st.session_state.selected_facility = self.selected_facility

    def get_template_config(self, template_name: str) -> Dict[str, Any]:
        """
        Get configuration for a specific template
        User config takes precedence over default config
        Headers are merged from default_headers
        
        Args:
            template_name: Name of the template
            
        Returns:
            Dictionary with endpoint configuration
        """
        # Check user config first, then fall back to default
        if template_name in self.user_config:
            config = deepcopy(self.user_config[template_name])
        elif template_name in self.default_endpoints:
            config = deepcopy(self.default_endpoints[template_name])
        else:
            # Return a basic default if template not found
            config = {
                "endpoint": "/data",
                "method": "POST",
                "description": f"Default endpoint for {template_name}"
            }
        
        # Always ensure headers are present by merging with default headers
        if 'headers' not in config:
            config['headers'] = deepcopy(getattr(self, 'default_headers', {
                'Content-Type': 'application/json',
                'Authorization': self.shared_token
            }))
        else:
            # Merge default headers with template-specific headers
            merged_headers = deepcopy(getattr(self, 'default_headers', {}))
            merged_headers.update(config['headers'])
            config['headers'] = merged_headers
        
        return config
    
    def update_template_config(self, template_name: str, config: Dict[str, Any]):
        """
        Update configuration for a specific template
        
        Args:
            template_name: Name of the template
            config: New configuration dictionary
        """
        self.user_config[template_name] = config
        self.save_user_config()
    
    def reset_template_config(self, template_name: str):
        """
        Reset template configuration to default
        
        Args:
            template_name: Name of the template to reset
        """
        if template_name in self.user_config:
            del self.user_config[template_name]
            self.save_user_config()
    
    def get_all_templates(self) -> list:
        """Get list of all available templates from both default and user config"""
        all_templates = set()
        all_templates.update(self.default_endpoints.keys())
        all_templates.update(self.user_config.keys())
        return sorted(list(all_templates))
    
    def has_custom_config(self, template_name: str) -> bool:
        """Check if template has custom user configuration"""
        return template_name in self.user_config
        
    def export_full_config(self) -> str:
        """Export complete configuration including global settings and endpoint configurations"""
        full_config = {
            "version": "2.0",
            "export_timestamp": st.session_state.get('export_timestamp', ''),
            "global_settings": {
                "base_url": self.base_url,
                "shared_token": self.shared_token,
                "selected_organization": self.selected_organization,
                "selected_facility": self.selected_facility
            },
            "endpoint_configurations": self.user_config        }
        return json.dumps(full_config, indent=2)
        
    def _import_full_config(self, config_data: dict) -> bool:
        print('running fulle import')
        try:
            if "base_url" in config_data:
                self.base_url = config_data["base_url"]
            if "Authorization" in config_data['default_headers']:
                self.shared_token = config_data['default_headers']['Authorization']
            if "SelectedOrganization" in config_data['default_headers']:
                self.selected_organization = config_data['default_headers']["SelectedOrganization"]
            if "SelectedLocation" in config_data['default_headers']:
                self.selected_facility = config_data['default_headers']["SelectedLocation"]
            
            # Import endpoint configurations if present
            if "default_endpoints" in config_data:
                endpoint_configs = config_data["default_endpoints"]
                # Validate endpoint configurations
                for template_name, config in endpoint_configs.items():
                    if not isinstance(config, dict):
                        raise ValueError(f"Invalid config for template {template_name}")
                    if 'endpoint' not in config:
                        raise ValueError(f"Missing endpoint for template {template_name}")
                
                self.user_config.update(endpoint_configs)
            
            # Save all changes
            self.save_user_config()
            return True
            
        except Exception as e:
            st.error(f"Error importing full configuration: {e}")
            return False
    
    def _import_endpoint_configs_only(self, imported_config: dict) -> bool:
        """Import legacy endpoint-only configuration format"""
        try:
            # Validate the structure
            for template_name, config in imported_config.items():
                if not isinstance(config, dict):
                    raise ValueError(f"Invalid config for template {template_name}")
                if 'endpoint' not in config:
                    raise ValueError(f"Missing endpoint for template {template_name}")
            
            self.user_config.update(imported_config)
            self.save_user_config()
            return True
            
        except Exception as e:
            st.error(f"Error importing endpoint configurations: {e}")
            return False
    
    def import_full_config(self, config_json: str) -> bool:
        """
        Import complete configuration including global settings and endpoint configurations
        
        Args:
            config_json: JSON string with full configuration
            
        Returns:
            True if successful, False if error
        """
        try:
            imported_config = json.loads(config_json)
            return self._import_full_config(imported_config)
        except Exception as e:
            st.error(f"Error importing full configuration: {e}")
            return False
        
    def clear_all_user_config(self):
        """Clear all user customizations from session state"""
        self.user_config.clear()
        
        # Clear session state
        if 'user_endpoint_config' in st.session_state:
            del st.session_state.user_endpoint_config
        if 'base_url' in st.session_state:
            del st.session_state.base_url
        if 'shared_token' in st.session_state:
            del st.session_state.shared_token
        if 'selected_organization' in st.session_state:
            del st.session_state.selected_organization
        if 'selected_facility' in st.session_state:
            del st.session_state.selected_facility
        
        # Reset to defaults
        self.load_default_endpoints()
    
    def get_base_url(self) -> str:
        """Get the base URL for API endpoints"""
        return self.base_url

    def _validate_base_url(self, base_url: str) -> bool:
        """
        Validate base URL to prevent production URLs
        
        Args:
            base_url: URL to validate
            
        Returns:
            True if URL is safe, False if it's a production URL
            
        Raises:
            ValueError: If URL contains production pattern
        """
        # Check for 'p' right before '.sce' in the domain
        production_pattern = r'p\.sce\.'
        if re.search(production_pattern, base_url, re.IGNORECASE):
            raise ValueError(
                "🚫 PRODUCTION URL DETECTED!\n\n"
                "This appears to be a production environment URL (contains 'p.sce.').\n"
                "Using this data creation tool on production systems is UNSAFE and PROHIBITED.\n\n"
                "Please use a development or test environment URL instead."
            )
        return True
    
    def set_base_url(self, base_url: str):
        """Set the base URL for API endpoints with production validation"""
        try:
            # Validate URL before setting
            self._validate_base_url(base_url)
            self.base_url = base_url
            self.save_user_config()
        except ValueError as e:
            # Re-raise the validation error to be handled by the UI
            raise e
    
    def get_shared_token(self) -> str:
        """Get the shared API token"""
        return self.shared_token
    
    def set_shared_token(self, token: str):
        """Set the shared API token for all templates"""
        # Ensure token has Bearer prefix if not already present
        if not token.startswith('Bearer '):
            token = f'Bearer {token}'
        self.shared_token = token
        self.save_user_config()
    
    def get_relative_endpoint_for_template(self, template_name: str) -> str:
        """Get just the relative endpoint path for a template"""
        config = self.get_template_config(template_name)
        return config.get('endpoint', '/data')
    
    def get_endpoint_for_template(self, template_name: str) -> str:
        """Get the full endpoint URL for a template"""
        config = self.get_template_config(template_name)
        relative_endpoint = config.get('endpoint', '/data')
        return f"{self.base_url}{relative_endpoint}"
    
    def get_headers_for_template(self, template_name: str) -> Dict[str, str]:
        """Get the headers for a template with shared token, organization, and facility"""
        config = self.get_template_config(template_name)
        headers = config.get('headers', deepcopy(self.default_headers)).copy()
        
        # Always use the shared token, organization, and facility, overriding any template-specific values
        headers['Authorization'] = self.shared_token
        headers['SelectedOrganization'] = self.selected_organization
        headers['SelectedLocation'] = self.selected_facility
        return headers
    
    def get_method_for_template(self, template_name: str) -> str:
        """Get HTTP method for a template"""
        config = self.get_template_config(template_name)
        return config.get('method', 'POST')
    
    def get_selected_organization(self) -> str:
        """Get the selected organization"""
        return self.selected_organization
    
    def set_selected_organization(self, organization: str):
        """Set the selected organization"""
        self.selected_organization = organization
        self.save_user_config()
    
    def get_selected_facility(self) -> str:
        """Get the selected facility"""
        return self.selected_facility
    
    def set_selected_facility(self, facility: str):
        """Set the selected facility"""
        self.selected_facility = facility
        self.save_user_config()
