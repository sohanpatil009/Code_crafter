import os
import sys
import numpy as np
from PIL import Image
import tensorflow as tf
from config import Config

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom modules
from preprocessing.image_loader import ImageLoader
from preprocessing.normalization import ImageNormalizer
from features.extractor import FeatureExtractor
from models.cnn_model import CNNModel

class MLService:
    """Machine Learning service for disease prediction with advanced preprocessing"""
    
    def __init__(self):
        self.model_path = Config.MODEL_PATH
        self.image_size = Config.IMAGE_SIZE
        self.disease_classes = Config.DISEASE_CLASSES
        self.model = None
        
        # Initialize preprocessing modules
        self.image_loader = ImageLoader(target_size=self.image_size)
        self.normalizer = ImageNormalizer()
        self.feature_extractor = FeatureExtractor()
        
        self.load_model()
    
    def load_model(self):
        """Load trained ML model"""
        try:
            if os.path.exists(self.model_path):
                self.model = tf.keras.models.load_model(self.model_path)
                print(f"✅ Model loaded from: {self.model_path}")
            else:
                print(f"⚠️ Model not found at: {self.model_path}")
                print("⚠️ Using mock predictions for testing")
                self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """Advanced image preprocessing pipeline"""
        try:
            # Load and validate image
            img_array = self.image_loader.load_image(image_path, as_array=True)
            if img_array is None:
                print(f"❌ Failed to load image: {image_path}")
                return None
            
            # Apply advanced preprocessing
            processed = self.normalizer.preprocess_for_model(
                img_array,
                target_size=self.image_size,
                normalization='imagenet',
                enhance=True
            )
            
            # Add batch dimension
            processed = np.expand_dims(processed, axis=0)
            
            print(f"✅ Image preprocessed successfully: {processed.shape}")
            return processed
            
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def extract_features(self, image_path: str) -> dict:
        """Extract comprehensive features from image"""
        try:
            # Load original image for feature extraction
            img_array = self.image_loader.load_image(image_path, as_array=True)
            if img_array is None:
                return {}
            
            # Extract comprehensive features
            features = self.feature_extractor.extract_comprehensive_features(
                img_array,
                segment_leaf=True,
                segmentation_method='adaptive'
            )
            
            print(f"✅ Extracted {len(features)} features")
            return features
            
        except Exception as e:
            print(f"❌ Error extracting features: {e}")
            return {}
    
    def predict(self, image_path: str) -> dict:
        """Predict disease from image with comprehensive analysis"""
        try:
            # Preprocess image for model
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return None
            
            # Extract features for additional analysis
            features = self.extract_features(image_path)
            
            # Make prediction
            if self.model is not None:
                predictions = self.model.predict(processed_image)
                predicted_class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_idx])
                disease_name = self.disease_classes[predicted_class_idx]
                
                # Get top predictions
                top_predictions = self._get_top_predictions(predictions[0])
            else:
                # Mock prediction for testing
                import random
                disease_name = random.choice(self.disease_classes)
                confidence = random.uniform(0.75, 0.98)
                top_predictions = [
                    {'disease': disease_name, 'confidence': confidence * 100},
                    {'disease': random.choice(self.disease_classes), 'confidence': random.uniform(0.1, 0.3) * 100},
                    {'disease': random.choice(self.disease_classes), 'confidence': random.uniform(0.05, 0.15) * 100}
                ]
            
            # Prepare result with additional information
            result = {
                'disease_name': disease_name,
                'confidence': round(confidence * 100, 2),
                'all_predictions': top_predictions,
                'image_analysis': {
                    'leaf_segmented': features.get('segmentation_method', 'none') != 'none',
                    'leaf_area_ratio': features.get('leaf_area_ratio', 0.0),
                    'dominant_color': self._get_dominant_color(features),
                    'texture_complexity': self._get_texture_complexity(features),
                    'shape_analysis': self._get_shape_analysis(features)
                },
                'processing_info': {
                    'preprocessing_applied': True,
                    'features_extracted': len(features),
                    'model_used': 'CNN' if self.model else 'Mock'
                }
            }
            
            return result
            
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None
    
    def _get_dominant_color(self, features: dict) -> str:
        """Determine dominant color from features"""
        try:
            green_ratio = features.get('green_ratio', 0)
            red_ratio = features.get('red_ratio', 0)
            
            if green_ratio > 0.4:
                return 'green'
            elif red_ratio > 0.35:
                return 'red/brown'
            else:
                return 'mixed'
        except:
            return 'unknown'
    
    def _get_texture_complexity(self, features: dict) -> str:
        """Determine texture complexity from features"""
        try:
            lbp_entropy = features.get('lbp_entropy', 0)
            
            if lbp_entropy > 3.5:
                return 'high'
            elif lbp_entropy > 2.5:
                return 'medium'
            else:
                return 'low'
        except:
            return 'unknown'
    
    def _get_shape_analysis(self, features: dict) -> dict:
        """Get shape analysis from features"""
        try:
            return {
                'circularity': round(features.get('circularity', 0), 3),
                'aspect_ratio': round(features.get('aspect_ratio', 0), 3),
                'solidity': round(features.get('solidity', 0), 3)
            }
        except:
            return {'circularity': 0, 'aspect_ratio': 0, 'solidity': 0}
    
    def _get_top_predictions(self, predictions, top_k: int = 3) -> list:
        """Get top K predictions with confidence scores"""
        if predictions is None:
            return []
        
        try:
            top_indices = np.argsort(predictions)[-top_k:][::-1]
            top_predictions = [
                {
                    'disease': self.disease_classes[idx],
                    'confidence': round(float(predictions[idx]) * 100, 2)
                }
                for idx in top_indices
            ]
            return top_predictions
        except Exception as e:
            print(f"❌ Error getting top predictions: {e}")
            return []
    
    def get_disease_classes(self) -> list:
        """Get list of all disease classes"""
        return self.disease_classes

# Global ML service instance
ml_service = MLService()
