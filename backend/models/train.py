"""
Model Training Module
Developed by Prathamesh for Crop Disease Detection

Provides comprehensive training pipeline for CNN models
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import json
from typing import Tuple, Dict, List, Optional
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cnn_model import CNNModel
from preprocessing.image_loader import ImageLoader
from preprocessing.augmentation import ImageAugmentation
from preprocessing.normalization import ImageNormalizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelTrainer:
    """
    Comprehensive model training class for crop disease detection
    """
    
    def __init__(self, input_shape: Tuple[int, int, int] = (224, 224, 3),
                 model_save_path: str = '../trained_models/'):
        """
        Initialize ModelTrainer
        
        Args:
            input_shape: Input image shape
            model_save_path: Path to save trained models
        """
        self.input_shape = input_shape
        self.model_save_path = model_save_path
        
        # Initialize preprocessing modules
        self.image_loader = ImageLoader(target_size=input_shape[:2])
        self.augmenter = ImageAugmentation(seed=42)
        self.normalizer = ImageNormalizer()
        
        # Training data
        self.X_train = None
        self.X_val = None
        self.X_test = None
        self.y_train = None
        self.y_val = None
        self.y_test = None
        self.class_names = []
        self.label_encoder = LabelEncoder()
        
        # Model
        self.cnn_model = None
        self.training_history = None
        
        # Create save directory
        os.makedirs(model_save_path, exist_ok=True)
        
        logger.info(f"ModelTrainer initialized with input shape: {input_shape}")
    
    def load_dataset_from_directory(self, data_dir: str, 
                                  test_size: float = 0.2, 
                                  val_size: float = 0.1) -> bool:
        """
        Load dataset from directory structure
        
        Args:
            data_dir: Path to dataset directory
            test_size: Fraction of data for testing
            val_size: Fraction of data for validation
            
        Returns:
            Success status
        """
        try:
            if not os.path.exists(data_dir):
                logger.error(f"Dataset directory not found: {data_dir}")
                return False
            
            images = []
            labels = []
            
            # Get class names from subdirectories
            self.class_names = [d for d in os.listdir(data_dir) 
                              if os.path.isdir(os.path.join(data_dir, d))]
            self.class_names.sort()
            
            logger.info(f"Found {len(self.class_names)} classes: {self.class_names}")
            
            # Load images from each class directory
            for class_name in self.class_names:
                class_dir = os.path.join(data_dir, class_name)
                image_files = [f for f in os.listdir(class_dir) 
                             if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]
                
                logger.info(f"Loading {len(image_files)} images from {class_name}")
                
                for image_file in image_files:
                    image_path = os.path.join(class_dir, image_file)
                    
                    # Load and preprocess image
                    img_array = self.image_loader.load_image(image_path, as_array=True)
                    if img_array is not None:
                        images.append(img_array)
                        labels.append(class_name)
            
            if len(images) == 0:
                logger.error("No images loaded from dataset")
                return False
            
            # Convert to numpy arrays
            X = np.array(images)
            y = np.array(labels)
            
            # Encode labels
            y_encoded = self.label_encoder.fit_transform(y)
            y_categorical = to_categorical(y_encoded, num_classes=len(self.class_names))
            
            # Split dataset
            X_temp, self.X_test, y_temp, self.y_test = train_test_split(
                X, y_categorical, test_size=test_size, random_state=42, stratify=y_encoded
            )
            
            self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
                X_temp, y_temp, test_size=val_size/(1-test_size), random_state=42
            )
            
            logger.info(f"Dataset split - Train: {len(self.X_train)}, Val: {len(self.X_val)}, Test: {len(self.X_test)}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def create_data_generators(self, batch_size: int = 32, 
                             augment_training: bool = True) -> Tuple[tf.keras.utils.Sequence, tf.keras.utils.Sequence]:
        """
        Create data generators for training and validation
        
        Args:
            batch_size: Batch size for training
            augment_training: Whether to apply augmentation to training data
            
        Returns:
            Tuple of (train_generator, val_generator)
        """
        try:
            if augment_training:
                # Training data generator with augmentation
                train_datagen = ImageDataGenerator(
                    rescale=1./255,
                    rotation_range=20,
                    width_shift_range=0.2,
                    height_shift_range=0.2,
                    shear_range=0.2,
                    zoom_range=0.2,
                    horizontal_flip=True,
                    brightness_range=[0.8, 1.2],
                    fill_mode='nearest'
                )
            else:
                # Simple rescaling for training
                train_datagen = ImageDataGenerator(rescale=1./255)
            
            # Validation data generator (no augmentation)
            val_datagen = ImageDataGenerator(rescale=1./255)
            
            # Create generators
            train_generator = train_datagen.flow(
                self.X_train, self.y_train,
                batch_size=batch_size,
                shuffle=True
            )
            
            val_generator = val_datagen.flow(
                self.X_val, self.y_val,
                batch_size=batch_size,
                shuffle=False
            )
            
            logger.info(f"Created data generators with batch size: {batch_size}")
            return train_generator, val_generator
            
        except Exception as e:
            logger.error(f"Error creating data generators: {e}")
            return None, None
    
    def build_and_compile_model(self, architecture: str = 'custom_cnn',
                              optimizer: str = 'adam', 
                              learning_rate: float = 0.001,
                              **model_kwargs) -> bool:
        """
        Build and compile CNN model
        
        Args:
            architecture: Model architecture name
            optimizer: Optimizer name
            learning_rate: Learning rate
            **model_kwargs: Additional model arguments
            
        Returns:
            Success status
        """
        try:
            # Create CNN model
            self.cnn_model = CNNModel(
                input_shape=self.input_shape,
                num_classes=len(self.class_names),
                model_name=architecture
            )
            
            # Build model
            model = self.cnn_model.build_model(architecture=architecture, **model_kwargs)
            
            # Compile model
            self.cnn_model.compile_model(
                optimizer=optimizer,
                learning_rate=learning_rate,
                loss='categorical_crossentropy',
                metrics=['accuracy', 'top_3_accuracy']
            )
            
            logger.info(f"Model built and compiled: {architecture}")
            logger.info(f"Model summary:\n{self.cnn_model.get_model_summary()}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error building model: {e}")
            return False
    
    def train_model(self, epochs: int = 50, batch_size: int = 32,
                   patience: int = 10, save_best: bool = True) -> bool:
        """
        Train the CNN model
        
        Args:
            epochs: Number of training epochs
            batch_size: Batch size
            patience: Early stopping patience
            save_best: Whether to save best model
            
        Returns:
            Success status
        """
        try:
            if self.cnn_model is None:
                logger.error("Model not built. Call build_and_compile_model() first.")
                return False
            
            if self.X_train is None:
                logger.error("Training data not loaded. Call load_dataset_from_directory() first.")
                return False
            
            # Create data generators
            train_gen, val_gen = self.create_data_generators(batch_size=batch_size)
            if train_gen is None:
                return False
            
            # Get callbacks
            model_save_path = os.path.join(self.model_save_path, f'best_{self.cnn_model.model_name}.h5')
            callbacks = self.cnn_model.get_callbacks(
                monitor='val_loss',
                patience=patience,
                save_path=model_save_path if save_best else None
            )
            
            # Train model
            logger.info(f"Starting training for {epochs} epochs...")
            
            self.training_history = self.cnn_model.model.fit(
                train_gen,
                epochs=epochs,
                validation_data=val_gen,
                callbacks=callbacks,
                verbose=1
            )
            
            # Save final model
            final_model_path = os.path.join(self.model_save_path, f'final_{self.cnn_model.model_name}.h5')
            self.cnn_model.save_model(final_model_path)
            
            logger.info("Training completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False
    
    def evaluate_model(self) -> Dict[str, float]:
        """
        Evaluate model on test set
        
        Returns:
            Dictionary of evaluation metrics
        """
        try:
            if self.cnn_model is None or self.X_test is None:
                logger.error("Model or test data not available")
                return {}
            
            # Normalize test data
            X_test_normalized = self.X_test / 255.0
            
            # Evaluate model
            test_loss, test_accuracy, test_top3_accuracy = self.cnn_model.model.evaluate(
                X_test_normalized, self.y_test, verbose=0
            )
            
            # Get predictions for additional metrics
            predictions = self.cnn_model.model.predict(X_test_normalized)
            predicted_classes = np.argmax(predictions, axis=1)
            true_classes = np.argmax(self.y_test, axis=1)
            
            # Calculate additional metrics
            from sklearn.metrics import classification_report, confusion_matrix
            
            report = classification_report(
                true_classes, predicted_classes,
                target_names=self.class_names,
                output_dict=True
            )
            
            evaluation_results = {
                'test_loss': float(test_loss),
                'test_accuracy': float(test_accuracy),
                'test_top3_accuracy': float(test_top3_accuracy),
                'precision_macro': float(report['macro avg']['precision']),
                'recall_macro': float(report['macro avg']['recall']),
                'f1_macro': float(report['macro avg']['f1-score'])
            }
            
            logger.info(f"Model evaluation results: {evaluation_results}")
            return evaluation_results
            
        except Exception as e:
            logger.error(f"Error evaluating model: {e}")
            return {}
    
    def plot_training_history(self, save_path: Optional[str] = None) -> bool:
        """
        Plot training history
        
        Args:
            save_path: Path to save plot
            
        Returns:
            Success status
        """
        try:
            if self.training_history is None:
                logger.error("No training history available")
                return False
            
            # Create subplots
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
            
            # Plot accuracy
            ax1.plot(self.training_history.history['accuracy'], label='Training Accuracy')
            ax1.plot(self.training_history.history['val_accuracy'], label='Validation Accuracy')
            ax1.set_title('Model Accuracy')
            ax1.set_xlabel('Epoch')
            ax1.set_ylabel('Accuracy')
            ax1.legend()
            ax1.grid(True)
            
            # Plot loss
            ax2.plot(self.training_history.history['loss'], label='Training Loss')
            ax2.plot(self.training_history.history['val_loss'], label='Validation Loss')
            ax2.set_title('Model Loss')
            ax2.set_xlabel('Epoch')
            ax2.set_ylabel('Loss')
            ax2.legend()
            ax2.grid(True)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Training history plot saved to: {save_path}")
            else:
                plt.show()
            
            return True
            
        except Exception as e:
            logger.error(f"Error plotting training history: {e}")
            return False
    
    def save_training_config(self, config_path: str) -> bool:
        """
        Save training configuration and results
        
        Args:
            config_path: Path to save configuration
            
        Returns:
            Success status
        """
        try:
            config = {
                'model_config': self.cnn_model.get_model_config() if self.cnn_model else {},
                'dataset_info': {
                    'num_classes': len(self.class_names),
                    'class_names': self.class_names,
                    'train_samples': len(self.X_train) if self.X_train is not None else 0,
                    'val_samples': len(self.X_val) if self.X_val is not None else 0,
                    'test_samples': len(self.X_test) if self.X_test is not None else 0
                },
                'training_params': {
                    'input_shape': self.input_shape,
                    'model_save_path': self.model_save_path
                }
            }
            
            # Add evaluation results if available
            evaluation_results = self.evaluate_model()
            if evaluation_results:
                config['evaluation_results'] = evaluation_results
            
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            logger.info(f"Training configuration saved to: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving training config: {e}")
            return False

# Example usage and training script
if __name__ == "__main__":
    print("🚀 Starting Crop Disease Detection Model Training")
    
    # Initialize trainer
    trainer = ModelTrainer(
        input_shape=(224, 224, 3),
        model_save_path='../trained_models/'
    )
    
    # Example dataset path (replace with actual path)
    dataset_path = '../data/train'
    
    if os.path.exists(dataset_path):
        print("📁 Loading dataset...")
        if trainer.load_dataset_from_directory(dataset_path):
            
            print("🏗️ Building model...")
            if trainer.build_and_compile_model(
                architecture='resnet50',  # or 'custom_cnn', 'mobilenet', etc.
                optimizer='adam',
                learning_rate=0.001,
                trainable_layers=10  # for transfer learning
            ):
                
                print("🎯 Starting training...")
                if trainer.train_model(
                    epochs=50,
                    batch_size=32,
                    patience=10
                ):
                    
                    print("📊 Evaluating model...")
                    results = trainer.evaluate_model()
                    print(f"Evaluation Results: {results}")
                    
                    print("📈 Plotting training history...")
                    trainer.plot_training_history(
                        save_path='../trained_models/training_history.png'
                    )
                    
                    print("💾 Saving configuration...")
                    trainer.save_training_config(
                        '../trained_models/training_config.json'
                    )
                    
                    print("✅ Training completed successfully!")
                else:
                    print("❌ Training failed")
            else:
                print("❌ Model building failed")
        else:
            print("❌ Dataset loading failed")
    else:
        print(f"❌ Dataset path not found: {dataset_path}")
        print("📝 Please create dataset directory with class subdirectories")
        print("   Example structure:")
        print("   data/train/")
        print("   ├── healthy/")
        print("   ├── disease1/")
        print("   ├── disease2/")
        print("   └── ...")