"""
Leaf Segmentation Module
Developed by Prathamesh for Crop Disease Detection

Provides advanced leaf segmentation techniques for isolating plant leaves from background
"""

import cv2
import numpy as np
from sklearn.cluster import KMeans
from typing import Tuple, Optional, List
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LeafSegmentation:
    """
    Advanced leaf segmentation class for crop disease detection
    """
    
    def __init__(self):
        """Initialize LeafSegmentation"""
        logger.info("LeafSegmentation initialized")
    
    def color_based_segmentation(self, image: np.ndarray, 
                                method: str = 'hsv_threshold') -> np.ndarray:
        """
        Segment leaf using color-based methods
        
        Args:
            image: Input image as numpy array (RGB)
            method: Segmentation method ('hsv_threshold', 'lab_threshold', 'rgb_threshold')
            
        Returns:
            Binary mask of leaf region
        """
        try:
            if method == 'hsv_threshold':
                # Convert to HSV color space
                hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
                
                # Define green color range for healthy leaves
                lower_green1 = np.array([35, 40, 40])
                upper_green1 = np.array([85, 255, 255])
                
                # Define yellow-green range for diseased leaves
                lower_green2 = np.array([15, 40, 40])
                upper_green2 = np.array([35, 255, 255])
                
                # Create masks
                mask1 = cv2.inRange(hsv, lower_green1, upper_green1)
                mask2 = cv2.inRange(hsv, lower_green2, upper_green2)
                
                # Combine masks
                mask = cv2.bitwise_or(mask1, mask2)
                
            elif method == 'lab_threshold':
                # Convert to LAB color space
                lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
                
                # Use A channel (green-red axis)
                a_channel = lab[:, :, 1]
                
                # Threshold for green regions (negative A values)
                _, mask = cv2.threshold(a_channel, 127, 255, cv2.THRESH_BINARY_INV)
                
            elif method == 'rgb_threshold':
                # Simple RGB thresholding
                # Green channel should be higher than red and blue
                r, g, b = cv2.split(image)
                
                # Create mask where green is dominant
                mask1 = g > r
                mask2 = g > b
                mask3 = g > 50  # Minimum green intensity
                
                mask = np.logical_and(np.logical_and(mask1, mask2), mask3).astype(np.uint8) * 255
                
            else:
                logger.warning(f"Unknown color segmentation method: {method}")
                mask = np.ones(image.shape[:2], dtype=np.uint8) * 255
            
            logger.debug(f"Applied {method} color segmentation")
            return mask
            
        except Exception as e:
            logger.error(f"Error in color-based segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def kmeans_segmentation(self, image: np.ndarray, k: int = 3) -> np.ndarray:
        """
        Segment leaf using K-means clustering
        
        Args:
            image: Input image as numpy array (RGB)
            k: Number of clusters
            
        Returns:
            Segmented image with leaf region highlighted
        """
        try:
            # Reshape image for K-means
            data = image.reshape((-1, 3))
            data = np.float32(data)
            
            # Apply K-means clustering
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
            _, labels, centers = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
            
            # Convert back to uint8 and reshape
            centers = np.uint8(centers)
            segmented_data = centers[labels.flatten()]
            segmented_image = segmented_data.reshape(image.shape)
            
            # Find the cluster that represents leaf (greenest cluster)
            green_scores = []
            for center in centers:
                # Calculate green dominance score
                r, g, b = center
                green_score = g - (r + b) / 2
                green_scores.append(green_score)
            
            # Get the cluster with highest green score
            leaf_cluster = np.argmax(green_scores)
            
            # Create mask for leaf cluster
            mask = (labels.flatten() == leaf_cluster).astype(np.uint8) * 255
            mask = mask.reshape(image.shape[:2])
            
            logger.debug(f"Applied K-means segmentation with k={k}")
            return mask
            
        except Exception as e:
            logger.error(f"Error in K-means segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def edge_based_segmentation(self, image: np.ndarray) -> np.ndarray:
        """
        Segment leaf using edge detection and contour analysis
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            Binary mask of leaf region
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Apply Gaussian blur to reduce noise
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            
            # Apply Canny edge detection
            edges = cv2.Canny(blurred, 50, 150)
            
            # Morphological operations to close gaps
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            closed = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Create mask
            mask = np.zeros(gray.shape, dtype=np.uint8)
            
            if contours:
                # Find the largest contour (assuming it's the leaf)
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Fill the contour
                cv2.fillPoly(mask, [largest_contour], 255)
            
            logger.debug("Applied edge-based segmentation")
            return mask
            
        except Exception as e:
            logger.error(f"Error in edge-based segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def watershed_segmentation(self, image: np.ndarray) -> np.ndarray:
        """
        Segment leaf using watershed algorithm
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            Binary mask of leaf region
        """
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            
            # Apply threshold to get binary image
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Noise removal
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)
            
            # Sure background area
            sure_bg = cv2.dilate(opening, kernel, iterations=3)
            
            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
            _, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
            
            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            unknown = cv2.subtract(sure_bg, sure_fg)
            
            # Marker labelling
            _, markers = cv2.connectedComponents(sure_fg)
            
            # Add one to all labels so that sure background is not 0, but 1
            markers = markers + 1
            
            # Mark the region of unknown with zero
            markers[unknown == 255] = 0
            
            # Apply watershed
            markers = cv2.watershed(image, markers)
            
            # Create mask (exclude background and boundaries)
            mask = np.zeros(gray.shape, dtype=np.uint8)
            mask[markers > 1] = 255
            
            logger.debug("Applied watershed segmentation")
            return mask
            
        except Exception as e:
            logger.error(f"Error in watershed segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def grabcut_segmentation(self, image: np.ndarray, 
                           rect: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Segment leaf using GrabCut algorithm
        
        Args:
            image: Input image as numpy array (RGB)
            rect: Rectangle (x, y, width, height) for initial segmentation
            
        Returns:
            Binary mask of leaf region
        """
        try:
            # If no rectangle provided, use center region
            if rect is None:
                height, width = image.shape[:2]
                margin = min(width, height) // 6
                rect = (margin, margin, width - 2*margin, height - 2*margin)
            
            # Initialize mask
            mask = np.zeros(image.shape[:2], np.uint8)
            
            # Initialize background and foreground models
            bgd_model = np.zeros((1, 65), np.float64)
            fgd_model = np.zeros((1, 65), np.float64)
            
            # Apply GrabCut
            cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)
            
            # Create final mask
            mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
            result_mask = mask2 * 255
            
            logger.debug("Applied GrabCut segmentation")
            return result_mask
            
        except Exception as e:
            logger.error(f"Error in GrabCut segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def adaptive_segmentation(self, image: np.ndarray) -> np.ndarray:
        """
        Adaptive segmentation that combines multiple methods
        
        Args:
            image: Input image as numpy array (RGB)
            
        Returns:
            Binary mask of leaf region
        """
        try:
            # Apply multiple segmentation methods
            hsv_mask = self.color_based_segmentation(image, 'hsv_threshold')
            kmeans_mask = self.kmeans_segmentation(image, k=3)
            edge_mask = self.edge_based_segmentation(image)
            
            # Combine masks using voting
            combined = (hsv_mask.astype(np.float32) + 
                       kmeans_mask.astype(np.float32) + 
                       edge_mask.astype(np.float32)) / 3
            
            # Threshold combined result
            _, final_mask = cv2.threshold(combined.astype(np.uint8), 127, 255, cv2.THRESH_BINARY)
            
            # Post-processing: remove small noise and fill holes
            final_mask = self.post_process_mask(final_mask)
            
            logger.debug("Applied adaptive segmentation")
            return final_mask
            
        except Exception as e:
            logger.error(f"Error in adaptive segmentation: {e}")
            return np.ones(image.shape[:2], dtype=np.uint8) * 255
    
    def post_process_mask(self, mask: np.ndarray) -> np.ndarray:
        """
        Post-process segmentation mask to remove noise and fill holes
        
        Args:
            mask: Binary mask
            
        Returns:
            Cleaned mask
        """
        try:
            # Remove small noise
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            cleaned = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Fill holes
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
            
            # Find contours and keep only the largest one
            contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                
                # Create new mask with only the largest contour
                result = np.zeros_like(mask)
                cv2.fillPoly(result, [largest_contour], 255)
                
                return result
            
            return cleaned
            
        except Exception as e:
            logger.error(f"Error in post-processing mask: {e}")
            return mask
    
    def extract_leaf_region(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Extract leaf region from image using mask
        
        Args:
            image: Original image
            mask: Binary mask of leaf region
            
        Returns:
            Image with leaf region extracted
        """
        try:
            # Apply mask to image
            result = cv2.bitwise_and(image, image, mask=mask)
            
            # Optional: Set background to white
            background = np.ones_like(image) * 255
            background_mask = cv2.bitwise_not(mask)
            background_region = cv2.bitwise_and(background, background, mask=background_mask)
            
            final_result = cv2.add(result, background_region)
            
            logger.debug("Extracted leaf region")
            return final_result
            
        except Exception as e:
            logger.error(f"Error extracting leaf region: {e}")
            return image
    
    def segment_and_extract(self, image: np.ndarray, 
                          method: str = 'adaptive') -> Tuple[np.ndarray, np.ndarray]:
        """
        Complete segmentation and extraction pipeline
        
        Args:
            image: Input image as numpy array (RGB)
            method: Segmentation method to use
            
        Returns:
            Tuple of (segmented_image, mask)
        """
        try:
            # Apply segmentation
            if method == 'adaptive':
                mask = self.adaptive_segmentation(image)
            elif method == 'hsv':
                mask = self.color_based_segmentation(image, 'hsv_threshold')
            elif method == 'kmeans':
                mask = self.kmeans_segmentation(image)
            elif method == 'edge':
                mask = self.edge_based_segmentation(image)
            elif method == 'watershed':
                mask = self.watershed_segmentation(image)
            elif method == 'grabcut':
                mask = self.grabcut_segmentation(image)
            else:
                logger.warning(f"Unknown segmentation method: {method}")
                mask = self.adaptive_segmentation(image)
            
            # Extract leaf region
            segmented_image = self.extract_leaf_region(image, mask)
            
            logger.info(f"Completed segmentation using {method} method")
            return segmented_image, mask
            
        except Exception as e:
            logger.error(f"Error in segmentation pipeline: {e}")
            return image, np.ones(image.shape[:2], dtype=np.uint8) * 255

# Example usage
if __name__ == "__main__":
    # Test the LeafSegmentation
    segmenter = LeafSegmentation()
    
    # Create a test image (replace with actual image loading)
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Test segmentation
    segmented, mask = segmenter.segment_and_extract(test_image, method='adaptive')
    
    print("Leaf segmentation tests completed successfully!")
    print(f"Original shape: {test_image.shape}")
    print(f"Segmented shape: {segmented.shape}")
    print(f"Mask shape: {mask.shape}")
    print(f"Leaf pixels: {np.sum(mask > 0)}")