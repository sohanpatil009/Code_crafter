"""
Model Prediction Module
Developed by Prathamesh for Crop Disease Detection

Provides comprehensive prediction capabilities for trained models
"""

import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image
import json
from typing import Dict, List, Tuple, Optional, Any, Union
import logging
import time

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cnn_model import CNNModel
from preprocessing.image_loader import ImageLoader
from preprocessing.normalization import ImageNormalizer
from features.extractor import FeatureExtractor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelPredictor:
    """
    Comprehensive model prediction class for crop disease detection
    """
    
    def __init__(self, model_path: str = None, class_names: List[str] = None,
                 confidence_threshold: float = 0.5):
        """
        Initialize ModelPredictor
        
        Args:
            model_path: Path to trained model file
            class_names: List of class names for prediction
            confidence_threshold: Minimum confidence threshold for predictions
        """
        self.model_path = model_path
        self.class_names = class_names or []
        self.confidence_threshold = confidence_threshold
        self.model = None
        
        # Initialize preprocessing modules
        self.image_loader = ImageLoader(target_size=(224, 224))
        self.normalizer = ImageNormalizer()
        self.feature_extractor = FeatureExtractor()
        
        # Prediction cache
        self.prediction_cache = {}
        self.cache_enabled = True
        
        logger.info(f"ModelPredictor initialized with model: {model_path}")
        logger.info(f"Confidence threshold: {confidence_threshold}")
    
    def load_model(self, model_path: str = None) -> bool:
        """
        Load trained model for prediction
        
        Args:
            model_path: Path to model file
            
        Returns:
            Success status
        """
        try:
            path = model_path or self.model_path
            if not path or not os.path.exists(path):
                logger.error(f"Model file not found: {path}")
                return False
            
            self.model = tf.keras.models.load_model(path)
            self.model_path = path
            
            # Warm up model with dummy prediction
            dummy_input = np.random.random((1, 224, 224, 3))
            _ = self.model.predict(dummy_input, verbose=0)
            
            logger.info(f"Model loaded and warmed up successfully from: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def predict_single_image(self, image_path: str, 
                           include_features: bool = False,
                           include_preprocessing_info: bool = False) -> Dict[str, Any]:
        """
        Predict disease for a single image
        
        Args:
            image_path: Path to image file
            include_features: Whether to include extracted features
            include_preprocessing_info: Whether to include preprocessing details
            
        Returns:
            Prediction results dictionary
        """
        try:
            if self.model is None:
                logger.error("Model not loaded. Call load_model() first.")
                return {}
            
            start_time = time.time()
            
            # Check cache
            cache_key = f"{image_path}_{include_features}_{include_preprocessing_info}"
            if self.cache_enabled and cache_key in self.prediction_cache:
                logger.info("Returning cached prediction")
                return self.prediction_cache[cache_key]
            
            # Load and preprocess image
            processed_image, preprocessing_info = self._preprocess_image(image_path)
            if processed_image is None:
                return {'error': 'Failed to preprocess image'}
            
            # Make prediction
            predictions = self.model.predict(processed_image, verbose=0)
            prediction_probs = predictions[0]
            
            # Get top predictions
            top_predictions = self._get_top_predictions(prediction_probs, top_k=5)
            
            # Get primary prediction
            primary_prediction = top_predictions[0] if top_predictions else None
            
            # Build result dictionary
            result = {
                'success': True,
                'image_path': image_path,
                'prediction_time': time.time() - start_time,
                'primary_prediction': primary_prediction,
                'top_predictions': top_predictions,
                'confidence_above_threshold': primary_prediction['confidence'] >= self.confidence_threshold if primary_prediction else False,
                'model_info': {
                    'model_path': self.model_path,
                    'confidence_threshold': self.confidence_threshold,
                    'num_classes': len(self.class_names)
                }
            }
            
            # Add features if requested
            if include_features:
                features = self._extract_image_features(image_path)
                result['extracted_features'] = features
            
            # Add preprocessing info if requested
            if include_preprocessing_info:
                result['preprocessing_info'] = preprocessing_info
            
            # Cache result
            if self.cache_enabled:
                self.prediction_cache[cache_key] = result
            
            logger.info(f"Prediction completed in {result['prediction_time']:.3f}s")
            return result
            
        except Exception as e:
            logger.error(f"Error predicting single image: {e}")
            return {'error': str(e), 'success': False}
    
    def predict_batch_images(self, image_paths: List[str],
                           batch_size: int = 32,
                           include_features: bool = False) -> List[Dict[str, Any]]:
        """
        Predict diseases for multiple images in batches
        
        Args:
            image_paths: List of image file paths
            batch_size: Batch size for prediction
            include_features: Whether to include extracted features
            
        Returns:
            List of prediction results
        """
        try:
            if self.model is None:
                logger.error("Model not loaded. Call load_model() first.")
                return []
            
            results = []
            total_images = len(image_paths)
            
            logger.info(f"Processing {total_images} images in batches of {batch_size}")
            
            for i in range(0, total_images, batch_size):
                batch_paths = image_paths[i:i + batch_size]
                batch_results = self._process_batch(batch_paths, include_features)
                results.extend(batch_results)
                
                logger.info(f"Processed batch {i//batch_size + 1}/{(total_images-1)//batch_size + 1}")
            
            logger.info(f"Batch prediction completed for {total_images} images")
            return results
            
        except Exception as e:
            logger.error(f"Error in batch prediction: {e}")
            return []
    
    def _process_batch(self, image_paths: List[str], 
                      include_features: bool = False) -> List[Dict[str, Any]]:
        """Process a batch of images"""
        try:
            batch_images = []
            valid_paths = []
            
            # Load and preprocess batch
            for image_path in image_paths:
                processed_image, _ = self._preprocess_image(image_path)
                if processed_image is not None:
                    batch_images.append(processed_image[0])  # Remove batch dimension
                    valid_paths.append(image_path)
                else:
                    logger.warning(f"Failed to preprocess: {image_path}")
            
            if not batch_images:
                return []
            
            # Convert to batch array
            batch_array = np.array(batch_images)
            
            # Make batch prediction
            start_time = time.time()
            predictions = self.model.predict(batch_array, verbose=0)
            prediction_time = time.time() - start_time
            
            # Process results
            results = []
            for i, (image_path, prediction_probs) in enumerate(zip(valid_paths, predictions)):
                top_predictions = self._get_top_predictions(prediction_probs, top_k=5)
                primary_prediction = top_predictions[0] if top_predictions else None
                
                result = {
                    'success': True,
                    'image_path': image_path,
                    'prediction_time': prediction_time / len(batch_images),  # Average time per image
                    'primary_prediction': primary_prediction,
                    'top_predictions': top_predictions,
                    'confidence_above_threshold': primary_prediction['confidence'] >= self.confidence_threshold if primary_prediction else False
                }
                
                # Add features if requested
                if include_features:
                    features = self._extract_image_features(image_path)
                    result['extracted_features'] = features
                
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing batch: {e}")
            return []
    
    def _preprocess_image(self, image_path: str) -> Tuple[Optional[np.ndarray], Dict[str, Any]]:
        """
        Preprocess image for model input
        
        Args:
            image_path: Path to image file
            
        Returns:
            Tuple of (preprocessed_image, preprocessing_info)
        """
        try:
            # Load image
            img_array = self.image_loader.load_image(image_path, as_array=True)
            if img_array is None:
                return None, {'error': 'Failed to load image'}
            
            # Get image info
            img_info = self.image_loader.get_image_info(image_path)
            
            # Preprocess for model
            processed = self.normalizer.preprocess_for_model(
                img_array,
                target_size=(224, 224),
                normalization='imagenet',
                enhance=True
            )
            
            # Add batch dimension
            processed = np.expand_dims(processed, axis=0)
            
            # Preprocessing info
            preprocessing_info = {
                'original_size': img_info.get('size', (0, 0)) if img_info else (0, 0),
                'target_size': (224, 224),
                'normalization': 'imagenet',
                'enhancement_applied': True,
                'preprocessing_successful': True
            }
            
            return processed, preprocessing_info
            
        except Exception as e:
            logger.error(f"Error preprocessing image {image_path}: {e}")
            return None, {'error': str(e), 'preprocessing_successful': False}
    
    def _get_top_predictions(self, prediction_probs: np.ndarray, 
                           top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Get top K predictions with confidence scores
        
        Args:
            prediction_probs: Prediction probabilities array
            top_k: Number of top predictions to return
            
        Returns:
            List of top predictions
        """
        try:
            # Get top K indices
            top_indices = np.argsort(prediction_probs)[-top_k:][::-1]
            
            top_predictions = []
            for idx in top_indices:
                confidence = float(prediction_probs[idx])
                
                # Get class name
                if idx < len(self.class_names):
                    class_name = self.class_names[idx]
                else:
                    class_name = f"Class_{idx}"
                
                prediction = {
                    'class_name': class_name,
                    'class_index': int(idx),
                    'confidence': confidence,
                    'confidence_percentage': round(confidence * 100, 2)
                }
                
                top_predictions.append(prediction)
            
            return top_predictions
            
        except Exception as e:
            logger.error(f"Error getting top predictions: {e}")
            return []
    
    def _extract_image_features(self, image_path: str) -> Dict[str, Any]:
        """
        Extract comprehensive features from image
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary of extracted features
        """
        try:
            # Load image for feature extraction
            img_array = self.image_loader.load_image(image_path, as_array=True)
            if img_array is None:
                return {'error': 'Failed to load image for feature extraction'}
            
            # Extract comprehensive features
            features = self.feature_extractor.extract_comprehensive_features(
                img_array,
                segment_leaf=True,
                segmentation_method='adaptive'
            )
            
            # Categorize features
            categorized_features = {
                'color_features': {},
                'shape_features': {},
                'texture_features': {},
                'edge_features': {},
                'metadata': {}
            }
            
            for key, value in features.items():
                if any(color_term in key.lower() for color_term in ['red', 'green', 'blue', 'hsv', 'lab']):
                    categorized_features['color_features'][key] = value
                elif any(shape_term in key.lower() for shape_term in ['area', 'perimeter', 'aspect', 'circularity', 'hu_moment']):
                    categorized_features['shape_features'][key] = value
                elif any(texture_term in key.lower() for texture_term in ['lbp', 'glcm', 'gabor', 'wavelet']):
                    categorized_features['texture_features'][key] = value
                elif any(edge_term in key.lower() for edge_term in ['edge', 'canny', 'sobel', 'laplacian']):
                    categorized_features['edge_features'][key] = value
                else:
                    categorized_features['metadata'][key] = value
            
            # Add feature summary
            categorized_features['summary'] = {
                'total_features': len(features),
                'color_features_count': len(categorized_features['color_features']),
                'shape_features_count': len(categorized_features['shape_features']),
                'texture_features_count': len(categorized_features['texture_features']),
                'edge_features_count': len(categorized_features['edge_features']),
                'feature_extraction_successful': True
            }
            
            return categorized_features
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return {'error': str(e), 'feature_extraction_successful': False}
    
    def predict_with_explanation(self, image_path: str) -> Dict[str, Any]:
        """
        Predict with detailed explanation and analysis
        
        Args:
            image_path: Path to image file
            
        Returns:
            Prediction with detailed explanation
        """
        try:
            # Get basic prediction
            result = self.predict_single_image(
                image_path, 
                include_features=True, 
                include_preprocessing_info=True
            )
            
            if not result.get('success', False):
                return result
            
            # Add explanation
            explanation = self._generate_prediction_explanation(result)
            result['explanation'] = explanation
            
            # Add confidence analysis
            confidence_analysis = self._analyze_confidence(result)
            result['confidence_analysis'] = confidence_analysis
            
            # Add recommendations
            recommendations = self._generate_recommendations(result)
            result['recommendations'] = recommendations
            
            return result
            
        except Exception as e:
            logger.error(f"Error generating prediction with explanation: {e}")
            return {'error': str(e), 'success': False}
    
    def _generate_prediction_explanation(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate explanation for the prediction"""
        try:
            primary_pred = result.get('primary_prediction', {})
            features = result.get('extracted_features', {})
            
            explanation = {
                'prediction_summary': f"Detected {primary_pred.get('class_name', 'Unknown')} with {primary_pred.get('confidence_percentage', 0):.1f}% confidence",
                'confidence_level': self._categorize_confidence(primary_pred.get('confidence', 0)),
                'key_indicators': [],
                'feature_analysis': {}
            }
            
            # Analyze key features
            if 'color_features' in features:
                color_analysis = self._analyze_color_features(features['color_features'])
                explanation['feature_analysis']['color'] = color_analysis
                if color_analysis.get('dominant_color'):
                    explanation['key_indicators'].append(f"Dominant color: {color_analysis['dominant_color']}")
            
            if 'shape_features' in features:
                shape_analysis = self._analyze_shape_features(features['shape_features'])
                explanation['feature_analysis']['shape'] = shape_analysis
                if shape_analysis.get('leaf_condition'):
                    explanation['key_indicators'].append(f"Leaf condition: {shape_analysis['leaf_condition']}")
            
            if 'texture_features' in features:
                texture_analysis = self._analyze_texture_features(features['texture_features'])
                explanation['feature_analysis']['texture'] = texture_analysis
                if texture_analysis.get('texture_complexity'):
                    explanation['key_indicators'].append(f"Texture complexity: {texture_analysis['texture_complexity']}")
            
            return explanation
            
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            return {'error': str(e)}
    
    def _categorize_confidence(self, confidence: float) -> str:
        """Categorize confidence level"""
        if confidence >= 0.9:
            return "Very High"
        elif confidence >= 0.8:
            return "High"
        elif confidence >= 0.7:
            return "Moderate"
        elif confidence >= 0.6:
            return "Low"
        else:
            return "Very Low"
    
    def _analyze_color_features(self, color_features: Dict[str, float]) -> Dict[str, Any]:
        """Analyze color features"""
        try:
            analysis = {}
            
            # Determine dominant color
            green_ratio = color_features.get('green_ratio', 0)
            red_ratio = color_features.get('red_ratio', 0)
            
            if green_ratio > 0.4:
                analysis['dominant_color'] = 'Healthy Green'
            elif red_ratio > 0.35:
                analysis['dominant_color'] = 'Diseased Brown/Red'
            else:
                analysis['dominant_color'] = 'Mixed Colors'
            
            # Green dominance indicator
            green_dominance = color_features.get('green_dominance', 0)
            if green_dominance > 20:
                analysis['health_indicator'] = 'Likely Healthy'
            elif green_dominance < -10:
                analysis['health_indicator'] = 'Possible Disease'
            else:
                analysis['health_indicator'] = 'Uncertain'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing color features: {e}")
            return {}
    
    def _analyze_shape_features(self, shape_features: Dict[str, float]) -> Dict[str, Any]:
        """Analyze shape features"""
        try:
            analysis = {}
            
            # Analyze leaf condition based on shape
            circularity = shape_features.get('circularity', 0)
            solidity = shape_features.get('solidity', 0)
            
            if circularity > 0.7 and solidity > 0.8:
                analysis['leaf_condition'] = 'Well-formed'
            elif circularity < 0.5 or solidity < 0.6:
                analysis['leaf_condition'] = 'Irregular/Damaged'
            else:
                analysis['leaf_condition'] = 'Moderate'
            
            # Aspect ratio analysis
            aspect_ratio = shape_features.get('aspect_ratio', 1)
            if aspect_ratio > 2:
                analysis['shape_type'] = 'Elongated'
            elif aspect_ratio < 0.5:
                analysis['shape_type'] = 'Wide'
            else:
                analysis['shape_type'] = 'Balanced'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing shape features: {e}")
            return {}
    
    def _analyze_texture_features(self, texture_features: Dict[str, float]) -> Dict[str, Any]:
        """Analyze texture features"""
        try:
            analysis = {}
            
            # Texture complexity
            lbp_entropy = texture_features.get('lbp_entropy', 0)
            if lbp_entropy > 3.5:
                analysis['texture_complexity'] = 'High (Possible Disease)'
            elif lbp_entropy > 2.5:
                analysis['texture_complexity'] = 'Moderate'
            else:
                analysis['texture_complexity'] = 'Low (Smooth Surface)'
            
            # Surface uniformity
            lbp_uniformity = texture_features.get('lbp_uniformity', 0)
            if lbp_uniformity > 0.8:
                analysis['surface_uniformity'] = 'Uniform'
            else:
                analysis['surface_uniformity'] = 'Non-uniform'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing texture features: {e}")
            return {}
    
    def _analyze_confidence(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze prediction confidence"""
        try:
            primary_pred = result.get('primary_prediction', {})
            top_preds = result.get('top_predictions', [])
            
            confidence = primary_pred.get('confidence', 0)
            
            analysis = {
                'confidence_score': confidence,
                'confidence_category': self._categorize_confidence(confidence),
                'reliability': 'High' if confidence >= self.confidence_threshold else 'Low',
                'recommendation': ''
            }
            
            # Confidence gap analysis
            if len(top_preds) >= 2:
                confidence_gap = top_preds[0]['confidence'] - top_preds[1]['confidence']
                analysis['confidence_gap'] = confidence_gap
                
                if confidence_gap > 0.3:
                    analysis['prediction_certainty'] = 'High'
                    analysis['recommendation'] = 'Prediction is reliable'
                elif confidence_gap > 0.1:
                    analysis['prediction_certainty'] = 'Moderate'
                    analysis['recommendation'] = 'Consider additional analysis'
                else:
                    analysis['prediction_certainty'] = 'Low'
                    analysis['recommendation'] = 'Multiple possibilities, manual verification recommended'
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing confidence: {e}")
            return {}
    
    def _generate_recommendations(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations based on prediction"""
        try:
            primary_pred = result.get('primary_prediction', {})
            confidence_analysis = result.get('confidence_analysis', {})
            
            recommendations = {
                'immediate_actions': [],
                'monitoring_advice': [],
                'treatment_suggestions': [],
                'prevention_tips': []
            }
            
            class_name = primary_pred.get('class_name', '').lower()
            confidence = primary_pred.get('confidence', 0)
            
            # General recommendations based on confidence
            if confidence >= 0.8:
                recommendations['immediate_actions'].append('High confidence detection - proceed with recommended treatment')
            elif confidence >= 0.6:
                recommendations['immediate_actions'].append('Moderate confidence - consider additional expert consultation')
            else:
                recommendations['immediate_actions'].append('Low confidence - manual inspection recommended')
            
            # Disease-specific recommendations
            if 'blight' in class_name:
                recommendations['treatment_suggestions'].extend([
                    'Apply copper-based fungicide',
                    'Improve air circulation around plants',
                    'Avoid overhead watering'
                ])
                recommendations['prevention_tips'].extend([
                    'Maintain proper plant spacing',
                    'Remove infected plant debris',
                    'Monitor humidity levels'
                ])
            elif 'rust' in class_name:
                recommendations['treatment_suggestions'].extend([
                    'Apply appropriate fungicide treatment',
                    'Remove affected leaves immediately'
                ])
            elif 'healthy' in class_name:
                recommendations['monitoring_advice'].extend([
                    'Continue regular monitoring',
                    'Maintain current care practices'
                ])
            
            # General monitoring advice
            recommendations['monitoring_advice'].extend([
                'Check plants weekly for new symptoms',
                'Monitor weather conditions',
                'Document any changes in plant health'
            ])
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return {}
    
    def save_prediction_results(self, results: Union[Dict, List[Dict]], 
                              output_path: str) -> bool:
        """
        Save prediction results to file
        
        Args:
            results: Prediction results (single dict or list of dicts)
            output_path: Path to save results
            
        Returns:
            Success status
        """
        try:
            # Ensure results is serializable
            if isinstance(results, dict):
                serializable_results = self._make_serializable(results)
            else:
                serializable_results = [self._make_serializable(result) for result in results]
            
            with open(output_path, 'w') as f:
                json.dump(serializable_results, f, indent=2)
            
            logger.info(f"Prediction results saved to: {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving prediction results: {e}")
            return False
    
    def _make_serializable(self, obj: Any) -> Any:
        """Make object JSON serializable"""
        if isinstance(obj, dict):
            return {key: self._make_serializable(value) for key, value in obj.items()}
        elif isinstance(obj, list):
            return [self._make_serializable(item) for item in obj]
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        else:
            return obj
    
    def clear_cache(self):
        """Clear prediction cache"""
        self.prediction_cache.clear()
        logger.info("Prediction cache cleared")
    
    def set_cache_enabled(self, enabled: bool):
        """Enable or disable prediction caching"""
        self.cache_enabled = enabled
        logger.info(f"Prediction caching {'enabled' if enabled else 'disabled'}")

# Example usage and prediction script
if __name__ == "__main__":
    print("🔮 Starting Crop Disease Detection Model Prediction")
    
    # Initialize predictor
    predictor = ModelPredictor(
        confidence_threshold=0.7
    )
    
    # Example model and image paths (replace with actual paths)
    model_path = '../trained_models/best_resnet50.h5'
    test_image = '../data/test_image.jpg'
    
    if os.path.exists(model_path):
        print("📁 Loading model...")
        
        if predictor.load_model(model_path):
            print("🎯 Model loaded successfully!")
            
            if os.path.exists(test_image):
                print("🖼️ Making prediction...")
                
                # Single image prediction with explanation
                result = predictor.predict_with_explanation(test_image)
                
                if result.get('success', False):
                    print("📊 Prediction Results:")
                    primary = result['primary_prediction']
                    print(f"   Disease: {primary['class_name']}")
                    print(f"   Confidence: {primary['confidence_percentage']:.2f}%")
                    print(f"   Confidence Level: {result['confidence_analysis']['confidence_category']}")
                    
                    print("\n💡 Key Indicators:")
                    for indicator in result['explanation']['key_indicators']:
                        print(f"   • {indicator}")
                    
                    print("\n📋 Recommendations:")
                    for action in result['recommendations']['immediate_actions']:
                        print(f"   • {action}")
                    
                    # Save results
                    predictor.save_prediction_results(result, '../prediction_results.json')
                    print("💾 Results saved to '../prediction_results.json'")
                    
                    print("✅ Prediction completed successfully!")
                else:
                    print(f"❌ Prediction failed: {result.get('error', 'Unknown error')}")
            else:
                print(f"❌ Test image not found: {test_image}")
                print("📝 Please provide a valid image path for testing")
        else:
            print("❌ Failed to load model")
    else:
        print(f"❌ Model not found: {model_path}")
        print("📝 Please ensure model is trained and available")
    
    print("\n🔮 Model prediction script completed!")