#!/usr/bin/env python3
"""
Configuration Validator for Tech Dashboard
Validates the interests.json configuration file format and content.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfigValidator:
    def __init__(self, config_path: str = "config/interests.json"):
        self.config_path = config_path
        self.required_fields = {
            'interests': dict,
            'learning_goals': list,
            'current_focus': list
        }
        
        self.valid_interest_categories = {
            'programming_languages',
            'frameworks', 
            'cybersecurity',
            'ai_ml',
            'devops',
            'other',
            'web_development',
            'mobile_development',
            'data_science',
            'blockchain',
            'cloud_computing'
        }
    
    def load_config(self) -> Optional[Dict[str, Any]]:
        """Load and parse the configuration file"""
        try:
            if not Path(self.config_path).exists():
                logger.error(f"Configuration file not found: {self.config_path}")
                return None
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            logger.info(f"✅ Configuration file loaded successfully")
            return config
            
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON format in {self.config_path}: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error loading configuration: {e}")
            return None
    
    def validate_structure(self, config: Dict[str, Any]) -> bool:
        """Validate the basic structure of the configuration"""
        logger.info("🔍 Validating configuration structure...")
        
        is_valid = True
        
        # Check required fields
        for field, expected_type in self.required_fields.items():
            if field not in config:
                logger.error(f"❌ Missing required field: {field}")
                is_valid = False
            elif not isinstance(config[field], expected_type):
                logger.error(f"❌ Field '{field}' should be of type {expected_type.__name__}, got {type(config[field]).__name__}")
                is_valid = False
            else:
                logger.info(f"✅ Field '{field}' is valid ({expected_type.__name__})")
        
        return is_valid
    
    def validate_interests(self, interests: Dict[str, Any]) -> bool:
        """Validate the interests section"""
        logger.info("🔍 Validating interests section...")
        
        is_valid = True
        
        if not interests:
            logger.warning("⚠️ Interests section is empty")
            return True
        
        for category, skills in interests.items():
            # Check if category name is reasonable
            if category not in self.valid_interest_categories:
                logger.warning(f"⚠️ Unusual interest category: '{category}' (consider using standard categories)")
            
            # Check if skills is a list
            if not isinstance(skills, list):
                logger.error(f"❌ Skills for category '{category}' should be a list, got {type(skills).__name__}")
                is_valid = False
                continue
            
            # Check if skills list is not empty
            if not skills:
                logger.warning(f"⚠️ No skills listed for category '{category}'")
                continue
            
            # Check individual skills
            for skill in skills:
                if not isinstance(skill, str):
                    logger.error(f"❌ Skill '{skill}' in category '{category}' should be a string")
                    is_valid = False
                elif not skill.strip():
                    logger.error(f"❌ Empty skill found in category '{category}'")
                    is_valid = False
            
            logger.info(f"✅ Category '{category}' has {len(skills)} valid skills")
        
        return is_valid
    
    def validate_learning_goals(self, learning_goals: List[str]) -> bool:
        """Validate the learning goals section"""
        logger.info("🔍 Validating learning goals...")
        
        is_valid = True
        
        if not learning_goals:
            logger.warning("⚠️ No learning goals specified")
            return True
        
        for i, goal in enumerate(learning_goals, 1):
            if not isinstance(goal, str):
                logger.error(f"❌ Learning goal #{i} should be a string, got {type(goal).__name__}")
                is_valid = False
            elif not goal.strip():
                logger.error(f"❌ Learning goal #{i} is empty")
                is_valid = False
            elif len(goal) < 10:
                logger.warning(f"⚠️ Learning goal #{i} seems too short: '{goal}'")
        
        logger.info(f"✅ Found {len(learning_goals)} learning goals")
        return is_valid
    
    def validate_current_focus(self, current_focus: List[str]) -> bool:
        """Validate the current focus section"""
        logger.info("🔍 Validating current focus...")
        
        is_valid = True
        
        if not current_focus:
            logger.warning("⚠️ No current focus areas specified")
            return True
        
        if len(current_focus) > 5:
            logger.warning(f"⚠️ Many focus areas ({len(current_focus)}) - consider limiting to 3-5 for better focus")
        
        for i, focus in enumerate(current_focus, 1):
            if not isinstance(focus, str):
                logger.error(f"❌ Focus area #{i} should be a string, got {type(focus).__name__}")
                is_valid = False
            elif not focus.strip():
                logger.error(f"❌ Focus area #{i} is empty")
                is_valid = False
        
        logger.info(f"✅ Found {len(current_focus)} current focus areas")
        return is_valid
    
    def validate_content_quality(self, config: Dict[str, Any]) -> bool:
        """Validate the quality and consistency of content"""
        logger.info("🔍 Validating content quality...")
        
        is_valid = True
        interests = config.get('interests', {})
        current_focus = config.get('current_focus', [])
        
        # Check if current focus areas relate to interests
        all_skills = []
        for category, skills in interests.items():
            if isinstance(skills, list):
                all_skills.extend(skills)
        
        # Simplified check - just warn if focus seems unrelated
        focus_coverage = 0
        for focus in current_focus:
            focus_words = focus.lower().split()
            if any(word in ' '.join(all_skills).lower() for word in focus_words):
                focus_coverage += 1
        
        if current_focus and focus_coverage == 0:
            logger.warning("⚠️ Current focus areas don't seem to relate to listed interests")
        
        logger.info("✅ Content quality validation completed")
        return is_valid
    
    def generate_stats(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Generate statistics about the configuration"""
        interests = config.get('interests', {})
        stats = {
            'total_categories': len(interests),
            'total_skills': sum(len(skills) if isinstance(skills, list) else 0 for skills in interests.values()),
            'total_learning_goals': len(config.get('learning_goals', [])),
            'total_focus_areas': len(config.get('current_focus', [])),
            'categories': list(interests.keys())
        }
        return stats
    
    def validate(self) -> bool:
        """Main validation method"""
        logger.info("🚀 Starting configuration validation...")
        
        # Load configuration
        config = self.load_config()
        if config is None:
            return False
        
        # Validate structure
        if not self.validate_structure(config):
            logger.error("❌ Configuration structure validation failed")
            return False
        
        # Validate individual sections
        validations = [
            self.validate_interests(config.get('interests', {})),
            self.validate_learning_goals(config.get('learning_goals', [])),
            self.validate_current_focus(config.get('current_focus', [])),
            self.validate_content_quality(config)
        ]
        
        if not all(validations):
            logger.error("❌ Configuration content validation failed")
            return False
        
        # Generate and display stats
        stats = self.generate_stats(config)
        logger.info("📊 Configuration Statistics:")
        logger.info(f"   📂 Categories: {stats['total_categories']}")
        logger.info(f"   🛠️ Skills: {stats['total_skills']}")
        logger.info(f"   🎯 Learning Goals: {stats['total_learning_goals']}")
        logger.info(f"   🔥 Focus Areas: {stats['total_focus_areas']}")
        
        logger.info("✅ Configuration validation completed successfully!")
        return True

def main():
    """Main entry point"""
    validator = ConfigValidator()
    
    if validator.validate():
        logger.info("🎉 Configuration is valid and ready to use!")
        sys.exit(0)
    else:
        logger.error("💥 Configuration validation failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()