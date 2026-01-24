"""
Image Augmentation Module
Developed by Prathamesh for Crop Disease Detection

Provides various image augmentation techniques for data enhancement
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import random
from typing import Tuple, List, Optional, Union
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageAugmentation:
    """
    Image augmentation class with various transformation techniques
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize ImageAugmentation
        
        Args:
            seed: Random seed for reproducible augmentations
        """
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        logger.info("ImageAugmentation initialized")
    
    def rotate_image(self, image: np.ndarray, angle: float = None) -> np.ndarray:
        """
        Rotate image by specified angle
        
        Args:
            image: Input image as numpy array
            angle: Rotation angle in degrees (random if None)
            
        Returns:
            Rotated image
        """
        try:
            if angle is None:
                angle = random.uniform(-30, 30)  # Random rotation between -30 to 30 degrees
            
            height, width = image.shape[:2]
            center = (width // 2, height // 2)
            
            # Get rotation matrix
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Apply rotation
            rotated = cv2.warpAffine(image, rotation_matrix, (width, height), 
                                   borderMode=cv2.BORDER_REFLECT)
            
            logger.debug(f"Rotated image by {angle:.2f} degrees")
            return rotated
            
        except Exception as e:
            logger.error(f"Error rotating image: {e}")
            return image
    
    def flip_image(self, image: np.ndarray, flip_type: str = 'random') -> np.ndarray:
        """
        Flip image horizontally, vertically, or both
        
        Args:
            image: Input image as numpy array
            flip_type: 'horizontal', 'vertical', 'both', or 'random'
            
        Returns:
            Flipped image
        """
        try:
            if flip_type == 'random':
                flip_type = random.choice(['horizontal', 'vertical', 'both', 'none'])
            
            if flip_type == 'horizontal':
                flipped = cv2.flip(image, 1)
            elif flip_type == 'vertical':
                flipped = cv2.flip(image, 0)
            elif flip_type == 'both':
                flipped = cv2.flip(image, -1)
            else:
                flipped = image
            
            logger.debug(f"Applied {flip_type} flip")
            return flipped
            
        except Exception as e:
            logger.error(f"Error flipping image: {e}")
            return image
    
    def adjust_brightness(self, image: np.ndarray, factor: float = None) -> np.ndarray:
        """
        Adjust image brightness
        
        Args:
            image: Input image as numpy array
            factor: Brightness factor (random if None)
            
        Returns:
            Brightness adjusted image
        """
        try:
            if factor is None:
                factor = random.uniform(0.7, 1.3)  # Random brightness between 0.7 to 1.3
            
            # Convert to PIL for brightness adjustment
            pil_image = Image.fromarray(image)
            enhancer = ImageEnhance.Brightness(pil_image)
            enhanced = enhancer.enhance(factor)
            
            result = np.array(enhanced)
            logger.debug(f"Adjusted brightness by factor {factor:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error adjusting brightness: {e}")
            return image
    
    def adjust_contrast(self, image: np.ndarray, factor: float = None) -> np.ndarray:
        """
        Adjust image contrast
        
        Args:
            image: Input image as numpy array
            factor: Contrast factor (random if None)
            
        Returns:
            Contrast adjusted image
        """
        try:
            if factor is None:
                factor = random.uniform(0.8, 1.2)  # Random contrast between 0.8 to 1.2
            
            # Convert to PIL for contrast adjustment
            pil_image = Image.fromarray(image)
            enhancer = ImageEnhance.Contrast(pil_image)
            enhanced = enhancer.enhance(factor)
            
            result = np.array(enhanced)
            logger.debug(f"Adjusted contrast by factor {factor:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error adjusting contrast: {e}")
            return image
    
    def adjust_saturation(self, image: np.ndarray, factor: float = None) -> np.ndarray:
        """
        Adjust image saturation
        
        Args:
            image: Input image as numpy array
            factor: Saturation factor (random if None)
            
        Returns:
            Saturation adjusted image
        """
        try:
            if factor is None:
                factor = random.uniform(0.8, 1.2)  # Random saturation between 0.8 to 1.2
            
            # Convert to PIL for saturation adjustment
            pil_image = Image.fromarray(image)
            enhancer = ImageEnhance.Color(pil_image)
            enhanced = enhancer.enhance(factor)
            
            result = np.array(enhanced)
            logger.debug(f"Adjusted saturation by factor {factor:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Error adjusting saturation: {e}")
            return image
    
    def add_noise(self, image: np.ndarray, noise_type: str = 'gaussian') -> np.ndarray:
        """
        Add noise to image
        
        Args:
            image: Input image as numpy array
            noise_type: Type of noise ('gaussian', 'salt_pepper', 'speckle')
            
        Returns:
            Noisy image
        """
        try:
            if noise_type == 'gaussian':
                # Gaussian noise
                mean = 0
                std = random.uniform(5, 15)
                noise = np.random.normal(mean, std, image.shape).astype(np.uint8)
                noisy = cv2.add(image, noise)
                
            elif noise_type == 'salt_pepper':
                # Salt and pepper noise
                prob = random.uniform(0.01, 0.05)
                noisy = image.copy()
                
                # Salt noise
                salt_coords = np.random.random(image.shape[:2]) < prob/2
                noisy[salt_coords] = 255
                
                # Pepper noise
                pepper_coords = np.random.random(image.shape[:2]) < prob/2
                noisy[pepper_coords] = 0
                
            elif noise_type == 'speckle':
                # Speckle noise
                noise = np.random.randn(*image.shape) * 0.1
                noisy = image + image * noise
                noisy = np.clip(noisy, 0, 255).astype(np.uint8)
            
            else:
                noisy = image
            
            logger.debug(f"Added {noise_type} noise")
            return noisy
            
        except Exception as e:
            logger.error(f"Error adding noise: {e}")
            return image
    
    def blur_image(self, image: np.ndarray, blur_type: str = 'gaussian') -> np.ndarray:
        """
        Apply blur to image
        
        Args:
            image: Input image as numpy array
            blur_type: Type of blur ('gaussian', 'motion', 'median')
            
        Returns:
            Blurred image
        """
        try:
            if blur_type == 'gaussian':
                kernel_size = random.choice([3, 5, 7])
                blurred = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
                
            elif blur_type == 'motion':
                # Motion blur
                kernel_size = random.randint(5, 15)
                angle = random.uniform(0, 180)
                
                # Create motion blur kernel
                kernel = np.zeros((kernel_size, kernel_size))
                kernel[int((kernel_size-1)/2), :] = np.ones(kernel_size)
                kernel = kernel / kernel_size
                
                # Rotate kernel
                M = cv2.getRotationMatrix2D((kernel_size/2, kernel_size/2), angle, 1)
                kernel = cv2.warpAffine(kernel, M, (kernel_size, kernel_size))
                
                blurred = cv2.filter2D(image, -1, kernel)
                
            elif blur_type == 'median':
                kernel_size = random.choice([3, 5, 7])
                blurred = cv2.medianBlur(image, kernel_size)
            
            else:
                blurred = image
            
            logger.debug(f"Applied {blur_type} blur")
            return blurred
            
        except Exception as e:
            logger.error(f"Error applying blur: {e}")
            return image
    
    def crop_and_resize(self, image: np.ndarray, crop_ratio: float = None) -> np.ndarray:
        """
        Randomly crop and resize image
        
        Args:
            image: Input image as numpy array
            crop_ratio: Ratio of image to crop (random if None)
            
        Returns:
            Cropped and resized image
        """
        try:
            if crop_ratio is None:
                crop_ratio = random.uniform(0.8, 0.95)  # Crop 80-95% of image
            
            height, width = image.shape[:2]
            
            # Calculate crop dimensions
            crop_height = int(height * crop_ratio)
            crop_width = int(width * crop_ratio)
            
            # Random crop position
            start_y = random.randint(0, height - crop_height)
            start_x = random.randint(0, width - crop_width)
            
            # Crop image
            cropped = image[start_y:start_y + crop_height, start_x:start_x + crop_width]
            
            # Resize back to original size
            resized = cv2.resize(cropped, (width, height), interpolation=cv2.INTER_LANCZOS4)
            
            logger.debug(f"Cropped {crop_ratio:.2f} of image and resized")
            return resized
            
        except Exception as e:
            logger.error(f"Error cropping and resizing: {e}")
            return image
    
    def random_augmentation(self, image: np.ndarray, num_augmentations: int = 3) -> np.ndarray:
        """
        Apply random combination of augmentations
        
        Args:
            image: Input image as numpy array
            num_augmentations: Number of augmentations to apply
            
        Returns:
            Augmented image
        """
        try:
            augmented = image.copy()
            
            # Available augmentation functions
            augmentations = [
                lambda img: self.rotate_image(img),
                lambda img: self.flip_image(img),
                lambda img: self.adjust_brightness(img),
                lambda img: self.adjust_contrast(img),
                lambda img: self.adjust_saturation(img),
                lambda img: self.add_noise(img, random.choice(['gaussian', 'salt_pepper'])),
                lambda img: self.blur_image(img, random.choice(['gaussian', 'median'])),
                lambda img: self.crop_and_resize(img)
            ]
            
            # Randomly select and apply augmentations
            selected_augmentations = random.sample(augmentations, 
                                                 min(num_augmentations, len(augmentations)))
            
            for aug_func in selected_augmentations:
                augmented = aug_func(augmented)
            
            logger.debug(f"Applied {len(selected_augmentations)} random augmentations")
            return augmented
            
        except Exception as e:
            logger.error(f"Error applying random augmentations: {e}")
            return image
    
    def augment_batch(self, images: List[np.ndarray], 
                     augmentations_per_image: int = 1) -> List[np.ndarray]:
        """
        Apply augmentations to a batch of images
        
        Args:
            images: List of input images
            augmentations_per_image: Number of augmented versions per image
            
        Returns:
            List of augmented images
        """
        augmented_images = []
        
        for image in images:
            # Add original image
            augmented_images.append(image)
            
            # Add augmented versions
            for _ in range(augmentations_per_image):
                augmented = self.random_augmentation(image)
                augmented_images.append(augmented)
        
        logger.info(f"Generated {len(augmented_images)} images from {len(images)} originals")
        return augmented_images

# Example usage
if __name__ == "__main__":
    # Test the ImageAugmentation
    augmenter = ImageAugmentation(seed=42)
    
    # Create a test image (replace with actual image loading)
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Test individual augmentations
    rotated = augmenter.rotate_image(test_image, 15)
    flipped = augmenter.flip_image(test_image, 'horizontal')
    bright = augmenter.adjust_brightness(test_image, 1.2)
    
    # Test random augmentation
    augmented = augmenter.random_augmentation(test_image, num_augmentations=3)
    
    print("Image augmentation tests completed successfully!")
    print(f"Original shape: {test_image.shape}")
    print(f"Augmented shape: {augmented.shape}")