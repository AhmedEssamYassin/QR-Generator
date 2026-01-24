import json
import logging
import os, platform
from typing import Any, Dict

logger = logging.getLogger(__name__)


class SettingsService:
    """Service for managing application settings"""
    
    DEFAULT_SETTINGS = {
        "theme": "dark",
        "last_save_directory": "",
        "default_box_size": 10,
        "default_border": 4,
        "window_width": 1000,
        "window_height": 700,
        "last_qr_type": "Text",
        "last_error_correction": "HIGH",
        "last_style": "Square"
    }
    
    def __init__(self, configFile: str = "qr_config.json"):
        # 1. Determine system-specific user data directory
        if platform.system() == "Windows":
            base_dir = os.getenv('APPDATA')  # e.g., C:\Users\Name\AppData\Roaming
        else:
            # Linux/Mac standard
            base_dir = os.path.expanduser("~/.config")
            
        # 2. Create the application folder if it doesn't exist
        self.app_dir = os.path.join(base_dir, "QRGeneratorPro")
        os.makedirs(self.app_dir, exist_ok=True)
        
        # 3. Set the full path
        self.configFile = os.path.join(self.app_dir, configFile)
        
        # 4. Load settings
        self.settings: Dict[str, Any] = self._load()
    
    def _load(self) -> Dict[str, Any]:
        """Load settings from file"""
        settings = self.DEFAULT_SETTINGS.copy()
        try:
            if os.path.exists(self.configFile):
                with open(self.configFile, 'r', encoding='utf-8') as f:
                    loaded = json.load(f)
                    settings.update(loaded)
                    logger.info("Settings loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
        return settings
    
    def _save(self) -> None:
        """Save settings to file"""
        try:
            with open(self.configFile, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=2)
            logger.info("Settings saved successfully")
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set setting value"""
        self.settings[key] = value
        self._save()
        logger.debug(f"Setting updated: {key} = {value}")
    
    def update(self, settingsDict: Dict[str, Any]) -> None:
        """Update multiple settings"""
        self.settings.update(settingsDict)
        self._save()
        logger.info(f"Updated {len(settingsDict)} settings")
    
    def reset(self) -> None:
        """Reset to default settings"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        self._save()
        logger.info("Settings reset to defaults")
    
    def getAll(self) -> Dict[str, Any]:
        """Get all settings"""
        return self.settings.copy()