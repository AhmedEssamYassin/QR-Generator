import logging
import os
from PIL import Image

logger = logging.getLogger(__name__)


class FileService:
    """Service for file operations"""
    
    @staticmethod
    def saveImage(image: Image.Image, filePath: str) -> None:
        """Save image to file"""
        try:
            # Determine format from extension
            ext = os.path.splitext(filePath)[1].lower()
            formatMap = {
                '.png': 'PNG',
                '.jpg': 'JPEG',
                '.jpeg': 'JPEG',
                '.bmp': 'BMP',
                '.gif': 'GIF'
            }
            fileFormat = formatMap.get(ext, 'PNG')
            
            # Convert RGBA to RGB for JPEG
            if fileFormat == 'JPEG' and image.mode == 'RGBA':
                rgbImage = Image.new('RGB', image.size, (255, 255, 255))
                rgbImage.paste(image, mask=image.split()[3])
                rgbImage.save(filePath, format=fileFormat, quality=95)
            else:
                image.save(filePath, format=fileFormat)
            
            logger.info(f"Image saved: {filePath}")
            
        except Exception as e:
            logger.error(f"Failed to save image: {e}")
            raise
    
    @staticmethod
    def loadImage(filePath: str) -> Image.Image:
        """Load image from file"""
        try:
            image = Image.open(filePath)
            logger.info(f"Image loaded: {filePath}")
            return image
        except Exception as e:
            logger.error(f"Failed to load image: {e}")
            raise
    
    @staticmethod
    def ensureDirectory(directory: str) -> None:
        """Ensure directory exists"""
        try:
            os.makedirs(directory, exist_ok=True)
        except Exception as e:
            logger.error(f"Failed to create directory: {e}")
            raise