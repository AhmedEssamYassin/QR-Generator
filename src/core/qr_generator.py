import logging
from PIL import Image
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    CircleModuleDrawer,
    GappedSquareModuleDrawer
)
from core.models import ErrorCorrection, QRStyle

logger = logging.getLogger(__name__)


class QRGenerator:
    """QR code generation engine"""
    
    @staticmethod
    def generate(
        content: str,
        errorCorrection: ErrorCorrection,
        boxSize: int,
        border: int,
        fgColor: str,
        bgColor: str,
        style: QRStyle
    ) -> Image.Image:
        """Generate QR code image with specified parameters"""
        try:
            # Library specific keyword arguments (error_correction, box_size) must remain snake_case
            qr = qrcode.QRCode(
                version=1,
                error_correction=errorCorrection.value[0],
                box_size=boxSize,
                border=border,
            )
            qr.add_data(content)
            qr.make(fit=True)
            
            # Apply style
            moduleDrawer = None
            if style == QRStyle.ROUNDED:
                moduleDrawer = RoundedModuleDrawer()
            elif style == QRStyle.CIRCLE:
                moduleDrawer = CircleModuleDrawer()
            elif style == QRStyle.GAPPED:
                moduleDrawer = GappedSquareModuleDrawer()
            
            if moduleDrawer:
                img = qr.make_image(
                    image_factory=StyledPilImage,
                    fill_color=fgColor,
                    back_color=bgColor,
                    module_drawer=moduleDrawer
                )
            else:
                img = qr.make_image(fill_color=fgColor, back_color=bgColor)
            
            logger.info(f"QR code generated: {len(content)} chars")
            return img
            
        except Exception as e:
            logger.error(f"QR generation failed: {e}")
            raise
    
    @staticmethod
    def addLogo(qrImage: Image.Image, logoPath: str, logoSizeRatio: float = 0.3) -> Image.Image:
        """Add logo to center of QR code"""
        try:
            qrImg = qrImage.copy()
            logo = Image.open(logoPath)
            
            # Calculate logo size
            qrWidth, qrHeight = qrImg.size
            logoSize = int(min(qrWidth, qrHeight) * logoSizeRatio)
            
            # Resize logo
            logo.thumbnail((logoSize, logoSize), Image.Resampling.LANCZOS)
            
            # Add white background
            logoBg = Image.new('RGB', logo.size, 'white')
            logoBg.paste(logo, (0, 0), logo if logo.mode == 'RGBA' else None)
            
            # Calculate position
            logoPos = ((qrWidth - logoSize) // 2, (qrHeight - logoSize) // 2)
            
            # Paste logo
            qrImg.paste(logoBg, logoPos)
            
            logger.info(f"Logo added: {logoPath}")
            return qrImg
            
        except Exception as e:
            logger.error(f"Failed to add logo: {e}")
            raise