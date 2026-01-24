import json
import logging
import os, platform
from typing import List, Dict
from core.models import QRConfig

logger = logging.getLogger(__name__)


class HistoryService:
    """Service for managing QR generation history"""
    
    def __init__(self, historyFile: str = "qr_history.json", maxEntries: int = 100):
        # 1. Determine system-specific user data directory
        if platform.system() == "Windows":
            base_dir = os.getenv('APPDATA')
        else:
            base_dir = os.path.expanduser("~/.config")
            
        # 2. Create the application folder if it doesn't exist
        self.app_dir = os.path.join(base_dir, "QRGeneratorPro")
        os.makedirs(self.app_dir, exist_ok=True)
        
        # 3. Set the full path
        self.historyFile = os.path.join(self.app_dir, historyFile)
        
        self.maxEntries = maxEntries
        self.history: List[Dict] = self._load()
    
    def _load(self) -> List[Dict]:
        """Load history from file"""
        try:
            if os.path.exists(self.historyFile):
                with open(self.historyFile, 'r', encoding='utf-8') as f:
                    history = json.load(f)
                    logger.info(f"Loaded {len(history)} history entries")
                    return history
        except Exception as e:
            logger.error(f"Failed to load history: {e}")
        return []
    
    def _save(self) -> None:
        """Save history to file"""
        try:
            with open(self.historyFile, 'w', encoding='utf-8') as f:
                json.dump(self.history[-self.maxEntries:], f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.history)} history entries")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")
    
    def add(self, config: QRConfig) -> None:
        """Add entry to history"""
        # Note: Using .toDict() and .qrType based on previous QRConfig conversion
        self.history.append(config.toDict())
        self._save()
        logger.info(f"Added history entry: {config.qrType}")
    
    def getAll(self) -> List[Dict]:
        """Get all history entries"""
        return self.history.copy()
    
    def getRecent(self, count: int = 10) -> List[Dict]:
        """Get recent history entries"""
        return self.history[-count:]
    
    def clear(self) -> None:
        """Clear all history"""
        self.history.clear()
        self._save()
        logger.info("History cleared")
    
    def deleteEntry(self, index: int) -> None:
        """Delete specific entry"""
        if 0 <= index < len(self.history):
            del self.history[index]
            self._save()
            logger.info(f"Deleted history entry at index {index}")