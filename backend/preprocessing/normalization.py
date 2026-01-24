"""
Image Normalization Module
Developed by Prathamesh for Crop Disease Detection

Provides various image normalization and preprocessing techniques
"""

import cv2
import numpy as np
from PIL import Image
from typing import Tuple, Optional, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageNormalizer:
    """
    Image normalization class with various preprocessing techniques
    """
    
    def __init__(self):
        """Initialize ImageNormalizer"""
        logger.info("ImageNormalizer initialized")
    
    def normalize_pixel_values(self, image: np.ndarray, 
                             method: str = 'standard') -> np.ndarray:
        """
        Normalize pixel values using different methods
        
        Args:
            image: Input image as numpy array
            method: Normalization method ('standard', 'minmax', 'zscore', 'imagenet')
            
        Returns:
            Normalized image
        """
        try:
            image_float = image.astype(np.float32)
            
            if method == 'standard':
                # Standard normalization [0, 1]
                normalized = image_float / 255.0
                
            elif method == 'minmax':
                # Min-Max normalization
                min_val = np.min(image_float)
                max_val = np.max(image_float)
                normalized = (image_float - min_val) / (max_val - min_val)
                
            elif method == 'zscore':
                # Z-score normalization
                mean = np.mean(image_float)
                std = np.std(image_float)
                normalized = (image_float - mean) / (std + 1e-8)
                
            elif method == 'imagenet':
                # ImageNet normalization
                # First normalize to [0, 1]
                normalized = image_float / 255.0
                
                # ImageNet mean and std for RGB
                mean = np.array([0.485, 0.456, 0.406])
                std = np.array([0.229, 0.224, 0.225])
                
                # Apply ImageNet normalization
                normalized = (normalized - mean) / std
                
            else:
                logger.warning(f"Unknown normalization method: {method}")
                normalized = image_float / 255.0
            
            logger.debug(f"Applied {method} normalization")
            return normalized
            
        except Exception as e:
            logger.error(f"Error normalizing image: {e}")
            return image.astype(np.float32) / 255.0
    
    def histogram_equalization(self, image: np.ndarray, 
                             method: str = 'global') -> np.ndarray:
        """
        Apply histogram equalization to improve contrast
        
        Args:
            image: Input image as numpy array
            method: Equalization method ('global', 'adaptive', 'clahe')
            
        Returns:
            Equalized image
        """
        try:
            if len(image.shape) == 3:
                # Convert RGB to LAB color space
                lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
                l_channel = lab[:, :, 0]
            else:
                l_channel = image
            
            if method == 'global':
                # Global histogram equalization
                equalized = cv2.equalizeHist(l_channel)
                
            elif method == 'adaptive':
                # Adaptive histogram equalization
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
                equalized = clahe.apply(l_channel)
                
            elif method == 'clahe':
                # CLAHE (Contrast Limited Adaptive Histogram Equalization)
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
                equalized = clahe.apply(l_channel)
                
            else:
                logger.warning(f"Unknown equalization method: {method}")
                equalized = l_channel
            
            if len(image.shape) == 3:
                # Replace L channel and convert back to RGB
                lab[:, :, 0] = equalized
                result = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
            else:
                result = equalized
            
            logger.debug(f"Applied {method} histogram equalization")
            return result
            
        except Exception as e:
            logger.error(f"Error applying histogram equalization: {e}")
            return image
    
    def denoise_image(self, image: np.ndarray, method: str = 'bilateral') -> np.ndarray:
        """
        Remove noise from image
        
        Args:
            image: Input image as numpy array
            method: Denoising method ('bilateral', 'gaussian', 'median', 'nlm')
            
        Returns:
            Denoised image
        """
        try:
            if method == 'bilateral':
                # Bilateral filtering
                denoised = cv2.bilateralFilter(image, 9, 75, 75)
                
            elif method == 'gaussian':
                # Gaussian blur
                denoised = cv2.GaussianBlur(image, (5, 5), 0)
                
            elif method == 'median':
                # Median filtering
                denoised = cv2.medianBlur(image, 5)
                
            elif method == 'nlm':
                # Non-local means denoising
                if len(image.shape) == 3:
                    denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
                else:
                    denoised = cv2.fastNlMeansDenoising(image, None, 10, 7, 21)
                    
            else:
                logger.warning(f"Unknown denoising method: {method}")
                denoised = image
            
            logger.debug(f"Applied {method} denoising")
            return denoised
            
        except Exception as e:
            logger.error(f"Error denoising image: {e}")
            return image
    
    def enhance_edges(self, image: np.ndarray, method: str = 'unsharp') -> np.ndarray:
        """
        Enhance edges in the image
        
        Args:
            image: Input image as numpy array
            method: Enhancement method ('unsharp', 'laplacian', 'sobel')
            
        Returns:
            Edge-enhanced image
        """
        try:
            if method == 'unsharp':
                # Unsharp masking
                gaussian = cv2.GaussianBlur(image, (0, 0), 2.0)
                enhanced = cv2.addWeighted(image, 1.5, gaussian, -0.5, 0)
                
            elif method == 'laplacian':
                # Laplacian sharpening
                if len(image.shape) == 3:
                    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                else:
                    gray = image
                
                laplacian = cv2.Laplacian(gray, cv2.CV_64F)
                laplacian = np.uint8(np.absolute(laplacian))
                
                if len(image.shape) == 3:
                    enhanced = image.copy()
                    for i in range(3):
                        enhanced[:, :, i] = cv2.add(image[:, :, i], laplacian)
                else:
                    enhanced = cv2.add(image, laplacian)
                    
            elif method == 'sobel':
                # Sobel edge enhancement
                if len(image.shape) == 3:
                    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                else:
                    gray = image
                
                sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
                sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
                sobel = np.sqrt(sobelx**2 + sobely**2)
                sobel = np.uint8(sobel)
                
                if len(image.shape) == 3:
                    enhanced = image.copy()
                    for i in range(3):
                        enhanced[:, :, i] = cv2.add(image[:, :, i], sobel)
                else:
                    enhanced = cv2.add(image, sobel)
                    
            else:
                logger.warning(f"Unknown edge enhancement method: {method}")
                enhanced = image
            
            # Ensure values are in valid range
            enhanced = np.clip(enhanced, 0, 255).astype(np.uint8)
            
            logger.debug(f"Applied {method} edge enhancement")
            return enhanced
            
        except Exception as e:
            logger.error(f"Error enhancing edges: {e}")
            return image
    
    def color_space_conversion(self, image: np.ndarray, 
                             target_space: str = 'HSV') -> np.ndarray:
        """
        Convert image to different color space
        
        Args:
            image: Input image as numpy array (RGB)
            target_space: Target color space ('HSV', 'LAB', 'YUV', 'GRAY')
            
        Returns:
            Converted image
        """
        try:
            if target_space == 'HSV':
                converted = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
                
            elif target_space == 'LAB':
                converted = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
                
            elif target_space == 'YUV':
                converted = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)
                
            elif target_space == 'GRAY':
                converted = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
                
            else:
                logger.warning(f"Unknown color space: {target_space}")
                converted = image
            
            logger.debug(f"Converted to {target_space} color space")
            return converted
            
        except Exception as e:
            logger.error(f"Error converting color space: {e}")
            return image
    
    def preprocess_for_model(self, image: np.ndarray, 
                           target_size: Tuple[int, int] = (224, 224),
                           normalization: str = 'imagenet',
                           enhance: bool = True) -> np.ndarray:
        """
        Complete preprocessing pipeline for model input
        
        Args:
            image: Input image as numpy array
            target_size: Target size for resizing
            normalization: Normalization method
            enhance: Whether to apply enhancement
            
        Returns:
            Preprocessed image ready for model
        """
        try:
            processed = image.copy()
            
            # Resize if needed
            if processed.shape[:2] != target_size:
                processed = cv2.resize(processed, target_size, 
                                     interpolation=cv2.INTER_LANCZOS4)
                logger.debug(f"Resized to {target_size}")
            
            # Apply enhancements if requested
            if enhance:
                # Denoise
                processed = self.denoise_image(processed, method='bilateral')
                
                # Histogram equalization
                processed = self.histogram_equalization(processed, method='clahe')
                
                # Edge enhancement
                processed = self.enhance_edges(processed, method='unsharp')
            
            # Normalize pixel values
            processed = self.normalize_pixel_values(processed, method=normalization)
            
            logger.info("Completed preprocessing pipeline")
            return processed
            
        except Exception as e:
            logger.error(f"Error in preprocessing pipeline: {e}")
            # Fallback to basic normalization
            return self.normalize_pixel_values(image, method='standard')
    
    def batch_normalize(self, images: list, method: str = 'standard') -> list:
        """
        Normalize a batch of images
        
        Args:
            images: List of input images
            method: Normalization method
            
        Returns:
            List of normalized images
        """
        normalized_images = []
        
        for image in images:
            normalized = self.normalize_pixel_values(image, method=method)
            normalized_images.append(normalized)
        
        logger.info(f"Normalized batch of {len(images)} images")
        return normalized_images
    
    def get_image_statistics(self, image: np.ndarray) -> dict:
        """
        Get statistical information about the image
        
        Args:
            image: Input image as numpy array
            
        Returns:
            Dictionary with image statistics
        """
        try:
            stats = {
                'shape': image.shape,
                'dtype': str(image.dtype),
                'min': float(np.min(image)),
                'max': float(np.max(image)),
                'mean': float(np.mean(image)),
                'std': float(np.std(image)),
                'median': float(np.median(image))
            }
            
            if len(image.shape) == 3:
                # Channel-wise statistics
                for i, channel in enumerate(['R', 'G', 'B']):
                    stats[f'{channel}_mean'] = float(np.mean(image[:, :, i]))
                    stats[f'{channel}_std'] = float(np.std(image[:, :, i]))
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting image statistics: {e}")
            return {}

# Example usage
if __name__ == "__main__":
    # Test the ImageNormalizer
    normalizer = ImageNormalizer()
    
    # Create a test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Test normalization
    normalized = normalizer.normalize_pixel_values(test_image, method='imagenet')
    
    # Test preprocessing pipeline
    preprocessed = normalizer.preprocess_for_model(test_image, 
                                                  target_size=(224, 224),
                                                  normalization='imagenet',
                                                  enhance=True)
    
    # Get statistics
    stats = normalizer.get_image_statistics(test_image)
    
    print("Image normalization tests completed successfully!")
    print(f"Original shape: {test_image.shape}")
    print(f"Preprocessed shape: {preprocessed.shape}")
    print(f"Image statistics: {stats}")