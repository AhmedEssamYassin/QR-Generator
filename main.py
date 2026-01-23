import sys
import logging
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ui.main_window import QRGeneratorView
from core.controller import QRGeneratorController
from core.models import QRGeneratorModel
from services.settings_service import SettingsService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qr_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Application entry point"""
    try:
        logger.info("=" * 60)
        logger.info("QR Code Generator Pro - Starting")
        logger.info("=" * 60)
        
        # Initialize services
        settingsService = SettingsService()
        
        # Initialize MVC components
        model = QRGeneratorModel()
        controller = QRGeneratorController(model, settingsService)
        view = QRGeneratorView(controller, settingsService)
        
        # Connect view to controller
        controller.setView(view)
        
        # Run application
        logger.info("Application initialized successfully")
        view.mainloop()
        
    except Exception as e:
        logger.critical(f"Application crashed: {e}", exc_info=True)
        raise
    finally:
        logger.info("Application terminated")


if __name__ == "__main__":
    main()