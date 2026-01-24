"""
Image Loader Module
Developed by Prathamesh for Crop Disease Detection

Handles image loading, validation, and basic preprocessing
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageOps
from typing import Tuple, Optional, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageLoader:
    """
    Image loader with validation and preprocessing capabilities
    """
    
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp']
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    MIN_RESOLUTION = (224, 224)  # Minimum image resolution
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224)):
        """
        Initialize ImageLoader
        
        Args:
            target_size: Target size for resizing images (width, height)
        """
        self.target_size = target_size
        logger.info(f"ImageLoader initialized with target size: {target_size}")
    
    def validate_image(self, image_path: str) -> bool:
        """
        Validate image file
        
        Args:
            image_path: Path to image file
            
        Returns:
            bool: True if valid, False otherwise
        """
        try:
            # Check if file exists
            if not os.path.exists(image_path):
                logger.error(f"Image file not found: {image_path}")
                return False
            
            # Check file size
            file_size = os.path.getsize(image_path)
            if file_size > self.MAX_FILE_SIZE:
                logger.error(f"Image file too large: {file_size} bytes")
                return False
            
            # Check file extension
            _, ext = os.path.splitext(image_path.lower())
            if ext not in self.SUPPORTED_FORMATS:
                logger.error(f"Unsupported image format: {ext}")
                return False
            
            # Try to open and validate image
            with Image.open(image_path) as img:
                # Check image mode
                if img.mode not in ['RGB', 'RGBA', 'L']:
                    logger.error(f"Unsupported image mode: {img.mode}")
                    return False
                
                # Check minimum resolution
                if img.size[0] < self.MIN_RESOLUTION[0] or img.size[1] < self.MIN_RESOLUTION[1]:
                    logger.error(f"Image resolution too low: {img.size}")
                    return False
            
            logger.info(f"Image validation successful: {image_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error validating image {image_path}: {e}")
            return False
    
    def load_image(self, image_path: str, as_array: bool = True) -> Optional[Union[np.ndarray, Image.Image]]:
        """
        Load and preprocess image
        
        Args:
            image_path: Path to image file
            as_array: Return as numpy array if True, PIL Image if False
            
        Returns:
            Loaded image as numpy array or PIL Image, None if failed
        """
        try:
            # Validate image first
            if not self.validate_image(image_path):
                return None
            
            # Load image using PIL
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
                logger.info(f"Converted image mode to RGB")
            
            # Fix orientation using EXIF data
            img = ImageOps.exif_transpose(img)
            
            # Resize image
            img = img.resize(self.target_size, Image.Resampling.LANCZOS)
            logger.info(f"Resized image to {self.target_size}")
            
            if as_array:
                # Convert to numpy array
                img_array = np.array(img, dtype=np.uint8)
                logger.info(f"Loaded image as array with shape: {img_array.shape}")
                return img_array
            else:
                logger.info(f"Loaded image as PIL Image")
                return img
                
        except Exception as e:
            logger.error(f"Error loading image {image_path}: {e}")
            return None
    
    def load_image_cv2(self, image_path: str) -> Optional[np.ndarray]:
        """
        Load image using OpenCV (for advanced processing)
        
        Args:
            image_path: Path to image file
            
        Returns:
            Image as numpy array in BGR format, None if failed
        """
        try:
            if not self.validate_image(image_path):
                return None
            
            # Load image using OpenCV
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"Failed to load image with OpenCV: {image_path}")
                return None
            
            # Resize image
            img = cv2.resize(img, self.target_size, interpolation=cv2.INTER_LANCZOS4)
            
            logger.info(f"Loaded image with OpenCV, shape: {img.shape}")
            return img
            
        except Exception as e:
            logger.error(f"Error loading image with OpenCV {image_path}: {e}")
            return None
    
    def batch_load_images(self, image_paths: list, as_array: bool = True) -> list:
        """
        Load multiple images in batch
        
        Args:
            image_paths: List of image file paths
            as_array: Return as numpy arrays if True, PIL Images if False
            
        Returns:
            List of loaded images
        """
        loaded_images = []
        
        for image_path in image_paths:
            img = self.load_image(image_path, as_array=as_array)
            if img is not None:
                loaded_images.append(img)
            else:
                logger.warning(f"Failed to load image: {image_path}")
        
        logger.info(f"Batch loaded {len(loaded_images)}/{len(image_paths)} images")
        return loaded_images
    
    def get_image_info(self, image_path: str) -> Optional[dict]:
        """
        Get detailed information about an image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with image information
        """
        try:
            if not os.path.exists(image_path):
                return None
            
            with Image.open(image_path) as img:
                info = {
                    'filename': os.path.basename(image_path),
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'width': img.size[0],
                    'height': img.size[1],
                    'file_size': os.path.getsize(image_path),
                    'has_transparency': img.mode in ['RGBA', 'LA'] or 'transparency' in img.info
                }
                
                # Get EXIF data if available
                if hasattr(img, '_getexif') and img._getexif() is not None:
                    info['has_exif'] = True
                else:
                    info['has_exif'] = False
                
                return info
                
        except Exception as e:
            logger.error(f"Error getting image info {image_path}: {e}")
            return None

# Example usage
if __name__ == "__main__":
    # Test the ImageLoader
    loader = ImageLoader(target_size=(224, 224))
    
    # Test image loading (replace with actual image path)
    test_image_path = "test_image.jpg"
    
    if os.path.exists(test_image_path):
        # Load image
        img_array = loader.load_image(test_image_path, as_array=True)
        if img_array is not None:
            print(f"Successfully loaded image with shape: {img_array.shape}")
        
        # Get image info
        info = loader.get_image_info(test_image_path)
        if info:
            print(f"Image info: {info}")
    else:
        print("Test image not found. Please provide a valid image path for testing.")