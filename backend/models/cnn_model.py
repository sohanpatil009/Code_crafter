"""
CNN Model Architecture Module
Developed by Prathamesh for Crop Disease Detection

Provides various CNN architectures including custom models and transfer learning
"""

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers, models, applications
from tensorflow.keras.optimizers import Adam, SGD, RMSprop
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
import numpy as np
from typing import Tuple, List, Optional, Dict, Any
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CNNModel:
    """
    CNN Model class with various architectures for crop disease detection
    """
    
    def __init__(self, input_shape: Tuple[int, int, int] = (224, 224, 3),
                 num_classes: int = 10, model_name: str = 'custom_cnn'):
        """
        Initialize CNN Model
        
        Args:
            input_shape: Input image shape (height, width, channels)
            num_classes: Number of disease classes
            model_name: Name of the model architecture
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model_name = model_name
        self.model = None
        self.history = None
        
        logger.info(f"CNNModel initialized: {model_name}, input_shape: {input_shape}, classes: {num_classes}")
    
    def create_custom_cnn(self, dropout_rate: float = 0.5) -> keras.Model:
        """
        Create custom CNN architecture
        
        Args:
            dropout_rate: Dropout rate for regularization
            
        Returns:
            Compiled Keras model
        """
        try:
            model = models.Sequential([
                # First Convolutional Block
                layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
                layers.BatchNormalization(),
                layers.Conv2D(32, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(dropout_rate * 0.5),
                
                # Second Convolutional Block
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.Conv2D(64, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(dropout_rate * 0.5),
                
                # Third Convolutional Block
                layers.Conv2D(128, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.Conv2D(128, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(dropout_rate * 0.7),
                
                # Fourth Convolutional Block
                layers.Conv2D(256, (3, 3), activation='relu'),
                layers.BatchNormalization(),
                layers.Conv2D(256, (3, 3), activation='relu'),
                layers.MaxPooling2D((2, 2)),
                layers.Dropout(dropout_rate * 0.7),
                
                # Global Average Pooling
                layers.GlobalAveragePooling2D(),
                
                # Dense Layers
                layers.Dense(512, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(dropout_rate),
                
                layers.Dense(256, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(dropout_rate),
                
                # Output Layer
                layers.Dense(self.num_classes, activation='softmax')
            ])
            
            logger.info("Created custom CNN architecture")
            return model
            
        except Exception as e:
            logger.error(f"Error creating custom CNN: {e}")
            raise
    
    def create_resnet_transfer(self, trainable_layers: int = 0) -> keras.Model:
        """
        Create ResNet50 with transfer learning
        
        Args:
            trainable_layers: Number of top layers to make trainable (0 = freeze all)
            
        Returns:
            Compiled Keras model
        """
        try:
            # Load pre-trained ResNet50
            base_model = applications.ResNet50(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Make top layers trainable if specified
            if trainable_layers > 0:
                for layer in base_model.layers[-trainable_layers:]:
                    layer.trainable = True
            
            # Add custom classification head
            model = models.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(512, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(256, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(self.num_classes, activation='softmax')
            ])
            
            logger.info(f"Created ResNet50 transfer learning model with {trainable_layers} trainable layers")
            return model
            
        except Exception as e:
            logger.error(f"Error creating ResNet transfer model: {e}")
            raise
    
    def create_mobilenet_transfer(self, alpha: float = 1.0, trainable_layers: int = 0) -> keras.Model:
        """
        Create MobileNetV2 with transfer learning (lightweight for mobile)
        
        Args:
            alpha: Width multiplier for MobileNet
            trainable_layers: Number of top layers to make trainable
            
        Returns:
            Compiled Keras model
        """
        try:
            # Load pre-trained MobileNetV2
            base_model = applications.MobileNetV2(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape,
                alpha=alpha
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Make top layers trainable if specified
            if trainable_layers > 0:
                for layer in base_model.layers[-trainable_layers:]:
                    layer.trainable = True
            
            # Add custom classification head
            model = models.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.BatchNormalization(),
                layers.Dropout(0.4),
                layers.Dense(256, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(128, activation='relu'),
                layers.Dropout(0.2),
                layers.Dense(self.num_classes, activation='softmax')
            ])
            
            logger.info(f"Created MobileNetV2 transfer learning model with alpha={alpha}")
            return model
            
        except Exception as e:
            logger.error(f"Error creating MobileNet transfer model: {e}")
            raise
    
    def create_efficientnet_transfer(self, model_size: str = 'B0', trainable_layers: int = 0) -> keras.Model:
        """
        Create EfficientNet with transfer learning
        
        Args:
            model_size: EfficientNet size ('B0', 'B1', 'B2', etc.)
            trainable_layers: Number of top layers to make trainable
            
        Returns:
            Compiled Keras model
        """
        try:
            # Map model size to EfficientNet variant
            efficientnet_models = {
                'B0': applications.EfficientNetB0,
                'B1': applications.EfficientNetB1,
                'B2': applications.EfficientNetB2,
                'B3': applications.EfficientNetB3
            }
            
            if model_size not in efficientnet_models:
                logger.warning(f"Unknown EfficientNet size: {model_size}, using B0")
                model_size = 'B0'
            
            # Load pre-trained EfficientNet
            base_model = efficientnet_models[model_size](
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Make top layers trainable if specified
            if trainable_layers > 0:
                for layer in base_model.layers[-trainable_layers:]:
                    layer.trainable = True
            
            # Add custom classification head
            model = models.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(512, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(256, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.3),
                layers.Dense(self.num_classes, activation='softmax')
            ])
            
            logger.info(f"Created EfficientNet{model_size} transfer learning model")
            return model
            
        except Exception as e:
            logger.error(f"Error creating EfficientNet transfer model: {e}")
            raise
    
    def create_vgg_transfer(self, trainable_layers: int = 0) -> keras.Model:
        """
        Create VGG16 with transfer learning
        
        Args:
            trainable_layers: Number of top layers to make trainable
            
        Returns:
            Compiled Keras model
        """
        try:
            # Load pre-trained VGG16
            base_model = applications.VGG16(
                weights='imagenet',
                include_top=False,
                input_shape=self.input_shape
            )
            
            # Freeze base model layers
            base_model.trainable = False
            
            # Make top layers trainable if specified
            if trainable_layers > 0:
                for layer in base_model.layers[-trainable_layers:]:
                    layer.trainable = True
            
            # Add custom classification head
            model = models.Sequential([
                base_model,
                layers.GlobalAveragePooling2D(),
                layers.BatchNormalization(),
                layers.Dropout(0.5),
                layers.Dense(512, activation='relu'),
                layers.BatchNormalization(),
                layers.Dropout(0.4),
                layers.Dense(256, activation='relu'),
                layers.Dropout(0.3),
                layers.Dense(self.num_classes, activation='softmax')
            ])
            
            logger.info("Created VGG16 transfer learning model")
            return model
            
        except Exception as e:
            logger.error(f"Error creating VGG transfer model: {e}")
            raise
    
    def build_model(self, architecture: str = 'custom_cnn', **kwargs) -> keras.Model:
        """
        Build model based on specified architecture
        
        Args:
            architecture: Model architecture name
            **kwargs: Additional arguments for model creation
            
        Returns:
            Compiled Keras model
        """
        try:
            if architecture == 'custom_cnn':
                self.model = self.create_custom_cnn(**kwargs)
            elif architecture == 'resnet50':
                self.model = self.create_resnet_transfer(**kwargs)
            elif architecture == 'mobilenet':
                self.model = self.create_mobilenet_transfer(**kwargs)
            elif architecture == 'efficientnet':
                self.model = self.create_efficientnet_transfer(**kwargs)
            elif architecture == 'vgg16':
                self.model = self.create_vgg_transfer(**kwargs)
            else:
                logger.warning(f"Unknown architecture: {architecture}, using custom_cnn")
                self.model = self.create_custom_cnn(**kwargs)
            
            self.model_name = architecture
            logger.info(f"Built model with architecture: {architecture}")
            return self.model
            
        except Exception as e:
            logger.error(f"Error building model: {e}")
            raise
    
    def compile_model(self, optimizer: str = 'adam', learning_rate: float = 0.001,
                     loss: str = 'categorical_crossentropy', metrics: List[str] = None) -> None:
        """
        Compile the model with specified parameters
        
        Args:
            optimizer: Optimizer name
            learning_rate: Learning rate
            loss: Loss function
            metrics: List of metrics to track
        """
        try:
            if self.model is None:
                raise ValueError("Model not built yet. Call build_model() first.")
            
            if metrics is None:
                metrics = ['accuracy', 'top_3_accuracy']
            
            # Create optimizer
            if optimizer.lower() == 'adam':
                opt = Adam(learning_rate=learning_rate)
            elif optimizer.lower() == 'sgd':
                opt = SGD(learning_rate=learning_rate, momentum=0.9)
            elif optimizer.lower() == 'rmsprop':
                opt = RMSprop(learning_rate=learning_rate)
            else:
                logger.warning(f"Unknown optimizer: {optimizer}, using Adam")
                opt = Adam(learning_rate=learning_rate)
            
            # Compile model
            self.model.compile(
                optimizer=opt,
                loss=loss,
                metrics=metrics
            )
            
            logger.info(f"Model compiled with {optimizer} optimizer, lr={learning_rate}")
            
        except Exception as e:
            logger.error(f"Error compiling model: {e}")
            raise
    
    def get_model_summary(self) -> str:
        """
        Get model summary as string
        
        Returns:
            Model summary string
        """
        if self.model is None:
            return "Model not built yet."
        
        import io
        import sys
        
        # Capture model summary
        old_stdout = sys.stdout
        sys.stdout = buffer = io.StringIO()
        
        self.model.summary()
        
        sys.stdout = old_stdout
        summary = buffer.getvalue()
        
        return summary
    
    def get_callbacks(self, monitor: str = 'val_loss', patience: int = 10,
                     save_path: str = 'best_model.h5') -> List[keras.callbacks.Callback]:
        """
        Get training callbacks
        
        Args:
            monitor: Metric to monitor
            patience: Patience for early stopping
            save_path: Path to save best model
            
        Returns:
            List of callbacks
        """
        callbacks = [
            EarlyStopping(
                monitor=monitor,
                patience=patience,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor=monitor,
                factor=0.5,
                patience=patience//2,
                min_lr=1e-7,
                verbose=1
            ),
            ModelCheckpoint(
                filepath=save_path,
                monitor=monitor,
                save_best_only=True,
                save_weights_only=False,
                verbose=1
            )
        ]
        
        return callbacks
    
    def save_model(self, filepath: str) -> bool:
        """
        Save the trained model
        
        Args:
            filepath: Path to save the model
            
        Returns:
            Success status
        """
        try:
            if self.model is None:
                logger.error("No model to save")
                return False
            
            self.model.save(filepath)
            logger.info(f"Model saved to {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving model: {e}")
            return False
    
    def load_model(self, filepath: str) -> bool:
        """
        Load a trained model
        
        Args:
            filepath: Path to the model file
            
        Returns:
            Success status
        """
        try:
            self.model = keras.models.load_model(filepath)
            logger.info(f"Model loaded from {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def predict(self, images: np.ndarray) -> np.ndarray:
        """
        Make predictions on images
        
        Args:
            images: Input images array
            
        Returns:
            Prediction probabilities
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded. Load or build a model first.")
            
            predictions = self.model.predict(images)
            return predictions
            
        except Exception as e:
            logger.error(f"Error making predictions: {e}")
            return np.array([])
    
    def get_model_config(self) -> Dict[str, Any]:
        """
        Get model configuration
        
        Returns:
            Dictionary with model configuration
        """
        config = {
            'model_name': self.model_name,
            'input_shape': self.input_shape,
            'num_classes': self.num_classes,
            'total_params': self.model.count_params() if self.model else 0,
            'trainable_params': sum([tf.keras.backend.count_params(w) for w in self.model.trainable_weights]) if self.model else 0
        }
        
        return config

# Example usage
if __name__ == "__main__":
    # Test the CNNModel
    print("Testing CNNModel...")
    
    # Create model instance
    cnn = CNNModel(input_shape=(224, 224, 3), num_classes=10, model_name='test_model')
    
    # Build custom CNN
    model = cnn.build_model(architecture='custom_cnn', dropout_rate=0.5)
    
    # Compile model
    cnn.compile_model(optimizer='adam', learning_rate=0.001)
    
    # Get model summary
    print("Model Summary:")
    print(cnn.get_model_summary())
    
    # Get model config
    config = cnn.get_model_config()
    print(f"Model Config: {config}")
    
    # Test prediction with dummy data
    dummy_images = np.random.random((1, 224, 224, 3))
    predictions = cnn.predict(dummy_images)
    print(f"Prediction shape: {predictions.shape}")
    
    print("CNNModel tests completed successfully!")