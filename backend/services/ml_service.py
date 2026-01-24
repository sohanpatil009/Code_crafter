import os
import numpy as np
from PIL import Image
import tensorflow as tf
from config import Config

class MLService:
    """Machine Learning service for disease prediction"""
    
    def __init__(self):
        self.model_path = Config.MODEL_PATH
        self.image_size = Config.IMAGE_SIZE
        self.disease_classes = Config.DISEASE_CLASSES
        self.model = None
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
        """Preprocess image for model input"""
        try:
            # Load image
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize to model input size
            img = img.resize(self.image_size)
            
            # Convert to array and normalize
            img_array = np.array(img)
            img_array = img_array / 255.0  # Normalize to [0, 1]
            
            # Add batch dimension
            img_array = np.expand_dims(img_array, axis=0)
            
            return img_array
        except Exception as e:
            print(f"❌ Error preprocessing image: {e}")
            return None
    
    def predict(self, image_path: str) -> dict:
        """Predict disease from image"""
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return None
            
            # Make prediction
            if self.model is not None:
                predictions = self.model.predict(processed_image)
                predicted_class_idx = np.argmax(predictions[0])
                confidence = float(predictions[0][predicted_class_idx])
                disease_name = self.disease_classes[predicted_class_idx]
            else:
                # Mock prediction for testing
                import random
                disease_name = random.choice(self.disease_classes)
                confidence = random.uniform(0.75, 0.98)
            
            result = {
                'disease_name': disease_name,
                'confidence': round(confidence * 100, 2),
                'all_predictions': self._get_top_predictions(predictions[0] if self.model else None)
            }
            
            return result
        except Exception as e:
            print(f"❌ Error making prediction: {e}")
            return None
    
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
