"""
Texture Analysis Module
Developed by Prathamesh for Crop Disease Detection

Provides advanced texture analysis techniques for feature extraction from leaf images
"""

import cv2
import numpy as np
from skimage.feature import local_binary_pattern, graycomatrix, graycoprops
from skimage.filters import gabor
from scipy import ndimage
from typing import Tuple, Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TextureAnalyzer:
    """
    Advanced texture analysis class for extracting texture features from leaf images
    """
    
    def __init__(self):
        """Initialize TextureAnalyzer"""
        logger.info("TextureAnalyzer initialized")
    
    def extract_lbp_features(self, image: np.ndarray, 
                           radius: int = 3, n_points: int = 24) -> Dict[str, float]:
        """
        Extract Local Binary Pattern (LBP) features
        
        Args:
            image: Input grayscale image
            radius: Radius of circle of sampling points
            n_points: Number of sampling points
            
        Returns:
            Dictionary of LBP features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Compute LBP
            lbp = local_binary_pattern(gray, n_points, radius, method='uniform')
            
            # Calculate histogram
            hist, _ = np.histogram(lbp.ravel(), bins=n_points + 2, 
                                 range=(0, n_points + 2), density=True)
            
            # Extract statistical features
            features = {
                'lbp_mean': float(np.mean(lbp)),
                'lbp_std': float(np.std(lbp)),
                'lbp_skewness': float(self._calculate_skewness(lbp)),
                'lbp_kurtosis': float(self._calculate_kurtosis(lbp)),
                'lbp_energy': float(np.sum(hist ** 2)),
                'lbp_entropy': float(-np.sum(hist * np.log2(hist + 1e-10))),
                'lbp_uniformity': float(np.sum(hist ** 2)),
                'lbp_contrast': float(np.sum((np.arange(len(hist)) ** 2) * hist))
            }
            
            # Add histogram bins as features
            for i, val in enumerate(hist):
                features[f'lbp_hist_{i}'] = float(val)
            
            logger.debug(f"Extracted LBP features with radius={radius}, n_points={n_points}")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting LBP features: {e}")
            return {}
    
    def extract_glcm_features(self, image: np.ndarray, 
                            distances: List[int] = [1, 2, 3],
                            angles: List[float] = [0, 45, 90, 135]) -> Dict[str, float]:
        """
        Extract Gray-Level Co-occurrence Matrix (GLCM) features
        
        Args:
            image: Input grayscale image
            distances: List of pixel distances
            angles: List of angles in degrees
            
        Returns:
            Dictionary of GLCM features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Convert angles to radians
            angles_rad = [np.radians(angle) for angle in angles]
            
            # Compute GLCM
            glcm = graycomatrix(gray, distances=distances, angles=angles_rad, 
                              levels=256, symmetric=True, normed=True)
            
            # Extract GLCM properties
            properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation']
            features = {}
            
            for prop in properties:
                values = graycoprops(glcm, prop)
                
                # Calculate statistics across distances and angles
                features[f'glcm_{prop}_mean'] = float(np.mean(values))
                features[f'glcm_{prop}_std'] = float(np.std(values))
                features[f'glcm_{prop}_min'] = float(np.min(values))
                features[f'glcm_{prop}_max'] = float(np.max(values))
            
            logger.debug(f"Extracted GLCM features with {len(distances)} distances and {len(angles)} angles")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting GLCM features: {e}")
            return {}
    
    def extract_gabor_features(self, image: np.ndarray,
                             frequencies: List[float] = [0.1, 0.3, 0.5],
                             angles: List[float] = [0, 45, 90, 135]) -> Dict[str, float]:
        """
        Extract Gabor filter features
        
        Args:
            image: Input grayscale image
            frequencies: List of frequencies for Gabor filters
            angles: List of angles in degrees
            
        Returns:
            Dictionary of Gabor features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            features = {}
            
            for freq in frequencies:
                for angle in angles:
                    # Apply Gabor filter
                    real, _ = gabor(gray, frequency=freq, theta=np.radians(angle))
                    
                    # Extract statistical features
                    prefix = f'gabor_f{freq}_a{angle}'
                    features[f'{prefix}_mean'] = float(np.mean(real))
                    features[f'{prefix}_std'] = float(np.std(real))
                    features[f'{prefix}_energy'] = float(np.sum(real ** 2))
                    features[f'{prefix}_entropy'] = float(self._calculate_entropy(real))
            
            logger.debug(f"Extracted Gabor features with {len(frequencies)} frequencies and {len(angles)} angles")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting Gabor features: {e}")
            return {}
    
    def extract_wavelet_features(self, image: np.ndarray, 
                               wavelet: str = 'db4', levels: int = 3) -> Dict[str, float]:
        """
        Extract wavelet transform features
        
        Args:
            image: Input grayscale image
            wavelet: Wavelet type
            levels: Number of decomposition levels
            
        Returns:
            Dictionary of wavelet features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Simple wavelet-like decomposition using filters
            features = {}
            
            # Apply different filters to simulate wavelet decomposition
            # Low-pass filter (approximation)
            kernel_low = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16
            approx = cv2.filter2D(gray, -1, kernel_low)
            
            # High-pass filters (details)
            kernel_high_h = np.array([[-1, 2, -1], [-2, 4, -2], [-1, 2, -1]]) / 4
            kernel_high_v = np.array([[-1, -2, -1], [2, 4, 2], [-1, -2, -1]]) / 4
            kernel_high_d = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]) / 4
            
            detail_h = cv2.filter2D(gray, -1, kernel_high_h)
            detail_v = cv2.filter2D(gray, -1, kernel_high_v)
            detail_d = cv2.filter2D(gray, -1, kernel_high_d)
            
            # Extract features from each component
            components = {
                'approx': approx,
                'detail_h': detail_h,
                'detail_v': detail_v,
                'detail_d': detail_d
            }
            
            for name, component in components.items():
                features[f'wavelet_{name}_mean'] = float(np.mean(component))
                features[f'wavelet_{name}_std'] = float(np.std(component))
                features[f'wavelet_{name}_energy'] = float(np.sum(component ** 2))
                features[f'wavelet_{name}_entropy'] = float(self._calculate_entropy(component))
            
            logger.debug(f"Extracted wavelet-like features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting wavelet features: {e}")
            return {}
    
    def extract_fractal_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        Extract fractal dimension features
        
        Args:
            image: Input grayscale image
            
        Returns:
            Dictionary of fractal features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Box-counting method for fractal dimension
            def box_count(image, box_size):
                # Threshold image
                binary = image > np.mean(image)
                
                # Count boxes containing at least one pixel
                h, w = binary.shape
                count = 0
                
                for i in range(0, h, box_size):
                    for j in range(0, w, box_size):
                        box = binary[i:i+box_size, j:j+box_size]
                        if np.any(box):
                            count += 1
                
                return count
            
            # Calculate fractal dimension using different box sizes
            box_sizes = [2, 4, 8, 16, 32]
            counts = []
            
            for size in box_sizes:
                if size < min(gray.shape):
                    count = box_count(gray, size)
                    counts.append(count)
                else:
                    counts.append(0)
            
            # Calculate fractal dimension (slope of log-log plot)
            valid_indices = [i for i, c in enumerate(counts) if c > 0]
            if len(valid_indices) > 1:
                log_sizes = np.log([box_sizes[i] for i in valid_indices])
                log_counts = np.log([counts[i] for i in valid_indices])
                
                # Linear regression to find slope
                coeffs = np.polyfit(log_sizes, log_counts, 1)
                fractal_dim = -coeffs[0]
            else:
                fractal_dim = 0.0
            
            features = {
                'fractal_dimension': float(fractal_dim),
                'fractal_complexity': float(np.std(counts) / (np.mean(counts) + 1e-10))
            }
            
            logger.debug("Extracted fractal features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting fractal features: {e}")
            return {}
    
    def extract_statistical_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        Extract basic statistical texture features
        
        Args:
            image: Input grayscale image
            
        Returns:
            Dictionary of statistical features
        """
        try:
            # Convert to grayscale if needed
            if len(image.shape) == 3:
                gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            else:
                gray = image
            
            # Basic statistics
            features = {
                'mean': float(np.mean(gray)),
                'std': float(np.std(gray)),
                'variance': float(np.var(gray)),
                'skewness': float(self._calculate_skewness(gray)),
                'kurtosis': float(self._calculate_kurtosis(gray)),
                'min': float(np.min(gray)),
                'max': float(np.max(gray)),
                'range': float(np.max(gray) - np.min(gray)),
                'median': float(np.median(gray)),
                'percentile_25': float(np.percentile(gray, 25)),
                'percentile_75': float(np.percentile(gray, 75)),
                'iqr': float(np.percentile(gray, 75) - np.percentile(gray, 25))
            }
            
            # Histogram features
            hist, _ = np.histogram(gray, bins=256, range=(0, 256), density=True)
            features['entropy'] = float(-np.sum(hist * np.log2(hist + 1e-10)))
            features['energy'] = float(np.sum(hist ** 2))
            
            logger.debug("Extracted statistical features")
            return features
            
        except Exception as e:
            logger.error(f"Error extracting statistical features: {e}")
            return {}
    
    def extract_all_texture_features(self, image: np.ndarray) -> Dict[str, float]:
        """
        Extract comprehensive texture features using all methods
        
        Args:
            image: Input image (RGB or grayscale)
            
        Returns:
            Dictionary containing all texture features
        """
        try:
            all_features = {}
            
            # Extract different types of features
            lbp_features = self.extract_lbp_features(image)
            glcm_features = self.extract_glcm_features(image)
            gabor_features = self.extract_gabor_features(image)
            wavelet_features = self.extract_wavelet_features(image)
            fractal_features = self.extract_fractal_features(image)
            statistical_features = self.extract_statistical_features(image)
            
            # Combine all features
            all_features.update(lbp_features)
            all_features.update(glcm_features)
            all_features.update(gabor_features)
            all_features.update(wavelet_features)
            all_features.update(fractal_features)
            all_features.update(statistical_features)
            
            logger.info(f"Extracted {len(all_features)} texture features")
            return all_features
            
        except Exception as e:
            logger.error(f"Error extracting all texture features: {e}")
            return {}
    
    def _calculate_skewness(self, data: np.ndarray) -> float:
        """Calculate skewness of data"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 3)
    
    def _calculate_kurtosis(self, data: np.ndarray) -> float:
        """Calculate kurtosis of data"""
        mean = np.mean(data)
        std = np.std(data)
        if std == 0:
            return 0.0
        return np.mean(((data - mean) / std) ** 4) - 3
    
    def _calculate_entropy(self, data: np.ndarray) -> float:
        """Calculate entropy of data"""
        hist, _ = np.histogram(data, bins=256, density=True)
        hist = hist[hist > 0]  # Remove zero entries
        return -np.sum(hist * np.log2(hist))
    
    def analyze_texture_regions(self, image: np.ndarray, 
                              mask: Optional[np.ndarray] = None,
                              region_size: int = 32) -> List[Dict[str, float]]:
        """
        Analyze texture in different regions of the image
        
        Args:
            image: Input image
            mask: Optional mask to limit analysis region
            region_size: Size of analysis regions
            
        Returns:
            List of feature dictionaries for each region
        """
        try:
            if mask is None:
                mask = np.ones(image.shape[:2], dtype=np.uint8) * 255
            
            h, w = image.shape[:2]
            region_features = []
            
            # Analyze overlapping regions
            step = region_size // 2
            
            for y in range(0, h - region_size, step):
                for x in range(0, w - region_size, step):
                    # Extract region
                    region = image[y:y+region_size, x:x+region_size]
                    region_mask = mask[y:y+region_size, x:x+region_size]
                    
                    # Check if region has enough valid pixels
                    if np.sum(region_mask > 0) > (region_size * region_size * 0.5):
                        # Apply mask to region
                        masked_region = cv2.bitwise_and(region, region, mask=region_mask)
                        
                        # Extract features for this region
                        features = self.extract_all_texture_features(masked_region)
                        features['region_x'] = x
                        features['region_y'] = y
                        
                        region_features.append(features)
            
            logger.info(f"Analyzed {len(region_features)} texture regions")
            return region_features
            
        except Exception as e:
            logger.error(f"Error analyzing texture regions: {e}")
            return []

# Example usage
if __name__ == "__main__":
    # Test the TextureAnalyzer
    analyzer = TextureAnalyzer()
    
    # Create a test image
    test_image = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    
    # Extract all texture features
    features = analyzer.extract_all_texture_features(test_image)
    
    print("Texture analysis tests completed successfully!")
    print(f"Extracted {len(features)} texture features")
    print("Sample features:")
    for i, (key, value) in enumerate(list(features.items())[:10]):
        print(f"  {key}: {value:.4f}")
    
    # Test region analysis
    regions = analyzer.analyze_texture_regions(test_image, region_size=64)
    print(f"Analyzed {len(regions)} regions")