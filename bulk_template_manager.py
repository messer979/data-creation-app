"""
Bulk Template Manager
Handles bulk export and import of all generation templates
"""

import json
import os
import streamlit as st
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from template_generator import TemplateGenerator


class BulkTemplateManager:
    """Manages bulk operations for generation templates"""
    
    @staticmethod
    def export_all_templates(template_generator: TemplateGenerator) -> Tuple[str, Dict[str, Any]]:
        """
        Export all generation templates as a single JSON structure
        
        Args:
            template_generator: TemplateGenerator instance
            
        Returns:
            Tuple of (JSON string, templates dict)
        """
        templates_export = {
            "metadata": {
                "export_date": datetime.now().isoformat(),
                "export_tool": "Data Creation Tool - Bulk Template Manager",
                "template_count": len(template_generator.generation_templates)
            },
            "templates": []
        }
        
        # Convert templates to array format with metadata
        for template_name, template_content in template_generator.generation_templates.items():
            template_entry = {
                "name": template_name,
                "content": template_content
            }
            templates_export["templates"].append(template_entry)
        
        # Sort templates by name for consistency
        templates_export["templates"].sort(key=lambda x: x["name"])
        
        return json.dumps(templates_export, indent=2), templates_export
    
    @staticmethod
    def import_all_templates(template_generator: TemplateGenerator, 
                           import_data: str, 
                           overwrite_existing: bool = True) -> Tuple[bool, str, List[str], List[str]]:
        """
        Import generation templates from JSON string into current session (no file writes)
        
        Args:
            template_generator: TemplateGenerator instance
            import_data: JSON string containing templates
            overwrite_existing: Whether to overwrite existing templates
            
        Returns:
            Tuple of (success, message, imported_templates, skipped_templates)
        """
        try:
            # Parse the import data
            parsed_data = json.loads(import_data)
            
            # Validate structure
            if not isinstance(parsed_data, dict):
                return False, "Invalid format: Root must be an object", [], []
            
            if "templates" not in parsed_data:
                return False, "Invalid format: Missing 'templates' array", [], []
            
            if not isinstance(parsed_data["templates"], list):
                return False, "Invalid format: 'templates' must be an array", [], []
            
            imported_templates = []
            skipped_templates = []
            
            # Process each template
            for template_entry in parsed_data["templates"]:
                if not isinstance(template_entry, dict):
                    continue
                
                if "name" not in template_entry or "content" not in template_entry:
                    continue
                
                template_name = template_entry["name"]
                template_content = template_entry["content"]
                
                # Validate template content structure
                if not BulkTemplateManager._validate_template_structure(template_content):
                    skipped_templates.append(f"{template_name} (invalid structure)")
                    continue
                
                # Check if template already exists
                if template_name in template_generator.generation_templates and not overwrite_existing:
                    skipped_templates.append(f"{template_name} (already exists)")
                    continue
                
                # Update template in session memory only (no file write)
                try:
                    template_generator.generation_templates[template_name] = template_content
                    imported_templates.append(template_name)
                    
                except Exception as e:
                    skipped_templates.append(f"{template_name} (session error: {str(e)})")
            
            # No file reload needed since we're updating session directly
            
            message = f"Import completed. {len(imported_templates)} templates imported to session"
            if skipped_templates:
                message += f", {len(skipped_templates)} skipped"
            
            return True, message, imported_templates, skipped_templates
            
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON format: {str(e)}", [], []
        except Exception as e:
            return False, f"Import error: {str(e)}", [], []
    
    @staticmethod
    def _validate_template_structure(template: Any) -> bool:
        """
        Validate that a template has the required structure
        
        Args:
            template: Template content to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(template, dict):
            return False
        
        required_sections = ["StaticFields", "DynamicFields", "RandomFields", "LinkedFields"]
        
        for section in required_sections:
            if section not in template:
                return False
        
        # Validate RandomFields structure
        if not isinstance(template["RandomFields"], list):
            return False
        
        for field in template["RandomFields"]:
            if not isinstance(field, dict) or "FieldName" not in field or "FieldType" not in field:
                return False
        
        # Validate other sections are dicts
        for section in ["StaticFields", "DynamicFields", "LinkedFields"]:
            if not isinstance(template[section], dict):
                return False
        
        return True
    
    @staticmethod
    def render_bulk_template_manager(template_generator: TemplateGenerator):
        """
        Render the bulk template management UI
        
        Args:
            template_generator: TemplateGenerator instance
        """        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📤 Export All Templates")
            st.write(f"Export all {len(template_generator.generation_templates)} generation templates as a single JSON file.")
            json_str, export_data = BulkTemplateManager.export_all_templates(template_generator)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generation_templates_export_{timestamp}.json"

            st.download_button(
                label="📥 Download Templates Export",
                data=json_str,
                file_name=filename,
                mime="application/json",
                use_container_width=True,
                help=f"Download all {len(template_generator.generation_templates)} templates"
            )

        
        with col2:
            st.markdown("### 📤 Import Templates")
            st.write("Import generation templates from a JSON file.")
            
            # File uploader
            uploaded_file = st.file_uploader(
                "Choose templates JSON file", 
                type=['json'],
                help="Upload a JSON file containing generation templates"
            )
            if 'last_gen_file' not in st.session_state:
                st.session_state.last_gen_file = None
            
            if uploaded_file is not None:
                if st.session_state.last_gen_file == uploaded_file.file_id:
                    st.success("File successfully imported!")
                    
                try:
                    # Read the uploaded file
                    content = uploaded_file.read().decode('utf-8')
                    
                    # Preview the import
                    try:
                        parsed_preview = json.loads(content)
                        if "templates" in parsed_preview and isinstance(parsed_preview["templates"], list):
                            st.info(f"📋 Ready to import {len(parsed_preview['templates'])} templates")
                            
                            # Show template names
                            with st.expander("🔍 Preview Templates", expanded=False):
                                for template in parsed_preview["templates"]:
                                    if isinstance(template, dict) and "name" in template:
                                        exists = template["name"] in template_generator.generation_templates
                                        status = "⚠️ Exists" if exists else "✅ New"
                                        st.write(f"• {template['name']} {status}")
                        else:
                            st.error("Invalid template format")
                            st.stop()
                    except json.JSONDecodeError:
                        st.error("Invalid JSON format")
                        st.stop()
                    
                    # Import button
                    if st.button("🔼 Import Templates", use_container_width=True):
                        success, message, imported, skipped = BulkTemplateManager.import_all_templates(
                            template_generator, content
                        )
                        
                        if success:
                            st.session_state.last_gen_file = uploaded_file.file_id
                            
                            if imported:
                                st.rerun()
                        else:
                            st.error(f"❌ {message}")
                            
                except Exception as e:
                    st.error(f"Error reading file: {str(e)}")
        
        # Current templates summary
        st.markdown("---")
        st.markdown("### 📊 Current Templates")
        
        if template_generator.generation_templates:
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Templates", len(template_generator.generation_templates))
            
            with col2:
                # Calculate total fields across all templates
                total_fields = 0
                for template in template_generator.generation_templates.values():
                    if isinstance(template, dict):
                        total_fields += len(template.get("StaticFields", {}))
                        total_fields += len(template.get("DynamicFields", {}))
                        total_fields += len(template.get("RandomFields", []))
                        total_fields += len(template.get("LinkedFields", {}))
                st.metric("Total Fields", total_fields)
            
            with col3:
                # Show templates directory
                st.metric("Templates Directory", template_generator.templates_dir)
            
            # List all templates
            with st.expander("📝 Template List", expanded=False):
                for template_name in sorted(template_generator.generation_templates.keys()):
                    template = template_generator.generation_templates[template_name]
                    field_count = 0
                    if isinstance(template, dict):
                        field_count += len(template.get("StaticFields", {}))
                        field_count += len(template.get("DynamicFields", {}))
                        field_count += len(template.get("RandomFields", []))
                        field_count += len(template.get("LinkedFields", {}))
                    
                    st.write(f"• **{template_name}** ({field_count} fields)")
        else:
            st.info("No templates currently loaded.")
