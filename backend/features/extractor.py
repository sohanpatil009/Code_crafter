"""
Feature Extractor Module
Developed by Prathamesh for Crop Disease Detection

Main feature extraction class that combines all feature extraction techniques
"""

import cv2
import numpy as np
from typing import Dict, List, Tuple, Optional, Union
import logging
from .segmentation import LeafSegmentation
from .texture_analysis import TextureAnalyzer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FeatureExtractor:
    """
    Main feature extraction class that combines segmentation and texture analysis
    """
    
    def __init__(self):
        """Initialize FeatureExtractor with all sub-modules"""
        self.segmenter = LeafSegmentation()
        self.texture_analyzer = TextureAnalyzer()
        logger.info("FeatureExtractor initialized with all sub-modules")
    
    def extract_color_features(self, image: np.ndarray, 
                             mask: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Extract color-based features from image
        
        Args:
            image: Input image (RGB)
            mask: Optional mask to limit analysis region
            
        Returns:
            Dictionary of color features
        """
        try:
            if mask is not None:
                # Apply mask to image
                masked_image = cv2.bitwise_and(image, image, mask=mask)
                # Get only the masked pixels
                pixels = masked_image[mask > 0]
            else:
                pixels = image.reshape(-1, 3)
            
            if len(pixels) == 0:
                logger.warning("No valid pixels found for color analysis")
                return {}
            
            features = {}
            
            # RGB statistics
            for i, channel in enumerate(['red', 'green', 'blue']):
                channel_data = pixels[:, i]
                features[f'{channel}_mean'] = float(np.mean(channel_data))
                features[f'{channel}_std'] = float(np.std(channel_data))
                features[f'{channel}_min'] = float(np.min(channel_data))
                features[f'{channel}_max'] = float(np.max(channel_data))
                features[f'{channel}_median'] = float(np.median(channel_data))
            
            # Color ratios
            r_mean = features['red_mean']
            g_mean = features['green_mean']
            b_mean = features['blue_mean']
            
            total = r_mean + g_mean + b_mean + 1e-10
            features['red_ratio'] = r_mean / total
            features['green_ratio'] = g_mean / total
            features['blue_ratio'] = b_mean / total
            
            # Green dominance (important for leaf analysis)
            features['green_dominance'] = g_mean - (r_mean + b_mean) / 2
            features['rg_ratio'] = r_mean / (g_mean + 1e-10)
            features['gb_ratio'] = g_mean / (b_mean + 1e-10)
            
            # Convert to other color spaces for additional features
            if mask is not None:
                roi_image = cv2.bitwise_and(image, image, mask=mask)
            else:
                roi_image = image
            
            # HSV features
            hsv = cv2.cvtColor(roi_image, cv2.COLOR_RGB2HSV)
            if mask is not None:
                hsv_pixels = hsv[mask > 0]
            else:
                hsv_pixels = hsv.reshape(-1, 3)
            
            if len(hsv_pixels) > 0:
                for i, channel in enumerate(['hue', 'saturation', 'value']):
                    channel_data = hsv_pixels[:, i]
                    features[f'hsv_{channel}_mean'] = float(np.mean(channel_data))
                    features[f'hsv_{channel}_std'] = float(np.std(channel_data))
            
            # LAB features
            lab = cv2.cvtColor(roi_image, cv2.COLOR_RGB2LAB)
            if mask is not None:
                lab_pixels = lab[mask > 0]
            else:
                lab_pixels = lab.reshape(-1, 3)
            
            if len(lab_pixels) > 0:
                for i, channel in enumerate(['l', 'a', 'b']):
                    channel_data = lab_pixels[:, i]
                    features[f'lab_{channel}_mean'] = float(np.mean(channel_data))
                    features[f'lab_{channel}_std'] = float(np.std(channel_data))
            
            logger.debug(f"Extracted {len(features)} color features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting color features: {e}")
            return {}
    
    def extract_shape_features(self, mask: np.ndarray) -> Dict[str, float]:
        """
        Extract shape-based features from binary mask
        
        Args:
            mask: Binary mask of the object
            
        Returns:
            Dictionary of shape features
        """
        try:
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if not contours:
                logger.warning("No contours found for shape analysis")
                return {}
            
            # Use the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            
            features = {}
            
            # Basic shape properties
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            features['area'] = float(area)
            features['perimeter'] = float(perimeter)
            
            # Aspect ratio and bounding box
            x, y, w, h = cv2.boundingRect(largest_contour)
            features['bounding_box_width'] = float(w)
            features['bounding_box_height'] = float(h)
            features['aspect_ratio'] = float(w / (h + 1e-10))
            features['bounding_box_area'] = float(w * h)
            features['extent'] = float(area / (w * h + 1e-10))
            
            # Circularity and compactness
            if perimeter > 0:
                features['circularity'] = float(4 * np.pi * area / (perimeter ** 2))
                features['compactness'] = float(perimeter ** 2 / (4 * np.pi * area + 1e-10))
            else:
                features['circularity'] = 0.0
                features['compactness'] = 0.0
            
            # Convex hull properties
            hull = cv2.convexHull(largest_contour)
            hull_area = cv2.contourArea(hull)
            features['convex_hull_area'] = float(hull_area)
            features['solidity'] = float(area / (hull_area + 1e-10))
            
            # Equivalent diameter
            features['equivalent_diameter'] = float(np.sqrt(4 * area / np.pi))
            
            # Moments and centroid
            moments = cv2.moments(largest_contour)
            if moments['m00'] != 0:
                cx = moments['m10'] / moments['m00']
                cy = moments['m01'] / moments['m00']
                features['centroid_x'] = float(cx)
                features['centroid_y'] = float(cy)
                
                # Hu moments (shape descriptors)
                hu_moments = cv2.HuMoments(moments)
                for i, hu in enumerate(hu_moments.flatten()):
                    features[f'hu_moment_{i}'] = float(-np.sign(hu) * np.log10(np.abs(hu) + 1e-10))
            
            # Ellipse fitting
            if len(largest_contour) >= 5:
                ellipse = cv2.fitEllipse(largest_contour)
                (center_x, center_y), (major_axis, minor_axis), angle = ellipse
                
                features['ellipse_major_axis'] = float(major_axis)
                features['ellipse_minor_axis'] = float(minor_axis)
                features['ellipse_eccentricity'] = float(np.sqrt(1 - (minor_axis / (major_axis + 1e-10)) ** 2))
                features['ellipse_angle'] = float(angle)
            
            logger.debug(f"Extracted {len(features)} shape features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting shape features: {e}")
            return {}
    
    def extract_edge_features(self, image: np.ndarray, 
                            mask: Optional[np.ndarray] = None) -> Dict[str, float]:
        """
        Extract edge-based features from image
        
        Args:
            image: Input image (RGB or grayscale)
            mask: Optional mask to limit analysis region
            
        Returns:
            Dictionary of edge features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Apply mask if provided
            if mask is not None:
                gray = cv2.bitwise_and(gray, gray, mask=mask)
            
            features = {}
            
            # Canny edge detection
            edges_canny = cv2.Canny(gray, 50, 150)
            features['canny_edge_density'] = float(np.sum(edges_canny > 0) / edges_canny.size)
            
            # Sobel edge detection
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            sobel_magnitude = np.sqrt(sobelx**2 + sobely**2)
            
            features['sobel_mean'] = float(np.mean(sobel_magnitude))
            features['sobel_std'] = float(np.std(sobel_magnitude))
            features['sobel_max'] = float(np.max(sobel_magnitude))
            
            # Laplacian edge detection
            laplacian = cv2.Laplacian(gray, cv2.CV_64F)
            features['laplacian_mean'] = float(np.mean(np.abs(laplacian)))
            features['laplacian_std'] = float(np.std(laplacian))
            features['laplacian_variance'] = float(np.var(laplacian))
            
            # Edge direction analysis
            edge_angles = np.arctan2(sobely, sobelx)
            edge_angles_deg = np.degrees(edge_angles)
            
            # Histogram of edge directions
            hist, _ = np.histogram(edge_angles_deg, bins=8, range=(-180, 180))
            hist_normalized = hist / (np.sum(hist) + 1e-10)
            
            for i, val in enumerate(hist_normalized):
                features[f'edge_direction_bin_{i}'] = float(val)
            
            # Edge strength in different directions
            features['horizontal_edges'] = float(np.mean(np.abs(sobelx)))
            features['vertical_edges'] = float(np.mean(np.abs(sobely)))
            features['edge_anisotropy'] = float(features['horizontal_edges'] / (features['vertical_edges'] + 1e-10))
            
            logger.debug(f"Extracted {len(features)} edge features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting edge features: {e}")
            return {}
    
    def extract_comprehensive_features(self, image: np.ndarray,
                                     segment_leaf: bool = True,
                                     segmentation_method: str = 'adaptive') -> Dict[str, Union[float, np.ndarray]]:
        """
        Extract comprehensive features from image including segmentation
        
        Args:
            image: Input image (RGB)
            segment_leaf: Whether to perform leaf segmentation
            segmentation_method: Method for leaf segmentation
            
        Returns:
            Dictionary containing all extracted features
        """
        try:
            all_features = {}
            
            # Perform leaf segmentation if requested
            if segment_leaf:
                segmented_image, mask = self.segmenter.segment_and_extract(image, method=segmentation_method)
                all_features['segmentation_method'] = segmentation_method
                all_features['leaf_area_ratio'] = float(np.sum(mask > 0) / mask.size)
            else:
                segmented_image = image
                mask = np.ones(image.shape[:2], dtype=np.uint8) * 255
            
            # Extract different types of features
            logger.info("Extracting color features...")
            color_features = self.extract_color_features(image, mask)
            all_features.update(color_features)
            
            logger.info("Extracting shape features...")
            shape_features = self.extract_shape_features(mask)
            all_features.update(shape_features)
            
            logger.info("Extracting edge features...")
            edge_features = self.extract_edge_features(image, mask)
            all_features.update(edge_features)
            
            logger.info("Extracting texture features...")
            texture_features = self.texture_analyzer.extract_all_texture_features(segmented_image)
            all_features.update(texture_features)
            
            # Add metadata
            all_features['image_height'] = float(image.shape[0])
            all_features['image_width'] = float(image.shape[1])
            all_features['total_pixels'] = float(image.shape[0] * image.shape[1])
            
            logger.info(f"Extracted {len(all_features)} comprehensive features")
            return all_features
            
        except Exception as e:
            logger.error(f"Error extracting comprehensive features: {e}")
            return {}
    
    def extract_features_for_training(self, images: List[np.ndarray],
                                    labels: Optional[List[str]] = None,
                                    segment_leaves: bool = True) -> Tuple[np.ndarray, Optional[np.ndarray]]:
        """
        Extract features from multiple images for training
        
        Args:
            images: List of input images
            labels: Optional list of labels
            segment_leaves: Whether to perform leaf segmentation
            
        Returns:
            Tuple of (feature_matrix, label_array)
        """
        try:
            all_features = []
            
            for i, image in enumerate(images):
                logger.info(f"Processing image {i+1}/{len(images)}")
                
                # Extract features for this image
                features = self.extract_comprehensive_features(image, segment_leaf=segment_leaves)
                
                if features:
                    # Convert to feature vector
                    feature_vector = []
                    feature_names = []
                    
                    for key, value in features.items():
                        if isinstance(value, (int, float, np.integer, np.floating)):
                            feature_vector.append(float(value))
                            feature_names.append(key)
                    
                    all_features.append(feature_vector)
                else:
                    logger.warning(f"Failed to extract features from image {i}")
            
            if not all_features:
                logger.error("No features extracted from any image")
                return np.array([]), None
            
            # Convert to numpy array
            feature_matrix = np.array(all_features)
            
            # Handle labels
            label_array = None
            if labels is not None:
                label_array = np.array(labels[:len(all_features)])
            
            logger.info(f"Extracted feature matrix with shape: {feature_matrix.shape}")
            return feature_matrix, label_array
            
        except Exception as e:
            logger.error(f"Error extracting features for training: {e}")
            return np.array([]), None
    
    def get_feature_names(self) -> List[str]:
        """
        Get list of all possible feature names
        
        Returns:
            List of feature names
        """
        # This would return all possible feature names
        # For now, return a sample based on the extraction methods
        feature_names = []
        
        # Color features
        for channel in ['red', 'green', 'blue']:
            for stat in ['mean', 'std', 'min', 'max', 'median']:
                feature_names.append(f'{channel}_{stat}')
        
        # Add more feature names based on other extraction methods
        # This is a simplified version - in practice, you'd want to maintain
        # a comprehensive list of all possible features
        
        return feature_names
    
    def save_features(self, features: Dict[str, float], filepath: str) -> bool:
        """
        Save extracted features to file
        
        Args:
            features: Dictionary of features
            filepath: Path to save file
            
        Returns:
            Success status
        """
        try:
            import json
            
            # Convert numpy types to native Python types for JSON serialization
            serializable_features = {}
            for key, value in features.items():
                if isinstance(value, (np.integer, np.floating)):
                    serializable_features[key] = float(value)
                else:
                    serializable_features[key] = value
            
            with open(filepath, 'w') as f:
                json.dump(serializable_features, f, indent=2)
            
            logger.info(f"Features saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving features: {e}")
            return False

# Example usage
if __name__ == "__main__":
    # Test the FeatureExtractor
    extractor = FeatureExtractor()
    
    # Create a test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Extract comprehensive features
    features = extractor.extract_comprehensive_features(test_image, segment_leaf=True)
    
    print("Feature extraction tests completed successfully!")
    print(f"Extracted {len(features)} features")
    print("Sample features:")
    for i, (key, value) in enumerate(list(features.items())[:15]):
        print(f"  {key}: {value}")
    
    # Test batch processing
    test_images = [test_image, test_image]  # Duplicate for testing
    feature_matrix, _ = extractor.extract_features_for_training(test_images)
    print(f"Feature matrix shape: {feature_matrix.shape}")