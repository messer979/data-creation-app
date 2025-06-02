"""
Template-based data generation engine
Interprets generation templates to create randomized data with controlled patterns
"""

import json
import os
from typing import Dict, Any, List, Optional
from template_functions import create_record_from_template


class TemplateGenerator:
    """Generates data based on generation template specifications"""
    
    def __init__(self, generation_templates_dir: str = "generation_templates"):
        self.templates_dir = generation_templates_dir
        self.generation_templates = {}
        self.load_generation_templates()
    
    def load_generation_templates(self):
        """Load all generation templates from the templates directory"""
        if not os.path.exists(self.templates_dir):
            return
        
        for filename in os.listdir(self.templates_dir):
            if filename.endswith('.json'):
                template_name = filename.replace('.json', '')
                try:
                    with open(os.path.join(self.templates_dir, filename), 'r') as f:
                        self.generation_templates[template_name] = json.load(f)
                except Exception as e:
                    print(f"Error loading generation template {filename}: {e}")
    
    def generate_records(self, template_name: str, count: int, base_template: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate records based on generation template using functional approach
        
        Args:
            template_name: Name of the generation template
            count: Number of records to generate
            base_template: Base JSON template structure
            
        Returns:
            List of generated records
        """
        if template_name not in self.generation_templates:
            raise ValueError(f"Generation template '{template_name}' not found")
        
        generation_template = self.generation_templates[template_name]
        records = []
        
        # Track dynamic field counters across all records
        dynamic_counters = {}
        
        for i in range(count):
            record = create_record_from_template(
                base_template,
                generation_template,
                i,
                dynamic_counters
            )
            records.append(record)
        
        return records
    
    def get_available_templates(self) -> List[str]:
        """Get list of available generation templates"""
        return list(self.generation_templates.keys())
    
    def get_template_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific generation template"""
        return self.generation_templates.get(template_name)
