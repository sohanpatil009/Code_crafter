"""
Model Evaluation Module
Developed by Prathamesh for Crop Disease Detection

Provides comprehensive model evaluation and performance analysis
"""

import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns
import json
from typing import Dict, List, Tuple, Optional, Any
import logging

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.cnn_model import CNNModel
from preprocessing.image_loader import ImageLoader
from preprocessing.normalization import ImageNormalizer

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelEvaluator:
    """
    Comprehensive model evaluation class for crop disease detection models
    """
    
    def __init__(self, model_path: str = None, class_names: List[str] = None):
        """
        Initialize ModelEvaluator
        
        Args:
            model_path: Path to trained model file
            class_names: List of class names for evaluation
        """
        self.model_path = model_path
        self.class_names = class_names or []
        self.model = None
        self.evaluation_results = {}
        
        # Initialize preprocessing modules
        self.image_loader = ImageLoader(target_size=(224, 224))
        self.normalizer = ImageNormalizer()
        
        logger.info(f"ModelEvaluator initialized with model: {model_path}")
    
    def load_model(self, model_path: str = None) -> bool:
        """
        Load trained model for evaluation
        
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
            
            logger.info(f"Model loaded successfully from: {path}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def evaluate_on_dataset(self, test_data_dir: str, 
                          batch_size: int = 32) -> Dict[str, Any]:
        """
        Evaluate model on test dataset
        
        Args:
            test_data_dir: Path to test dataset directory
            batch_size: Batch size for evaluation
            
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            if self.model is None:
                logger.error("Model not loaded. Call load_model() first.")
                return {}
            
            # Create test data generator
            test_datagen = ImageDataGenerator(rescale=1./255)
            
            test_generator = test_datagen.flow_from_directory(
                test_data_dir,
                target_size=(224, 224),
                batch_size=batch_size,
                class_mode='categorical',
                shuffle=False
            )
            
            # Update class names if not provided
            if not self.class_names:
                self.class_names = list(test_generator.class_indices.keys())
            
            logger.info(f"Evaluating on {test_generator.samples} test samples")
            logger.info(f"Classes: {self.class_names}")
            
            # Evaluate model
            test_loss, test_accuracy = self.model.evaluate(test_generator, verbose=1)
            
            # Get predictions
            predictions = self.model.predict(test_generator, verbose=1)
            predicted_classes = np.argmax(predictions, axis=1)
            true_classes = test_generator.classes
            
            # Calculate detailed metrics
            results = self._calculate_detailed_metrics(
                true_classes, predicted_classes, predictions
            )
            
            # Add basic metrics
            results.update({
                'test_loss': float(test_loss),
                'test_accuracy': float(test_accuracy),
                'num_samples': int(test_generator.samples),
                'num_classes': len(self.class_names),
                'class_names': self.class_names
            })
            
            self.evaluation_results = results
            logger.info(f"Evaluation completed. Accuracy: {test_accuracy:.4f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating on dataset: {e}")
            return {}
    
    def evaluate_on_arrays(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate model on numpy arrays
        
        Args:
            X_test: Test images array
            y_test: Test labels array (one-hot encoded)
            
        Returns:
            Dictionary with evaluation metrics
        """
        try:
            if self.model is None:
                logger.error("Model not loaded. Call load_model() first.")
                return {}
            
            logger.info(f"Evaluating on {len(X_test)} test samples")
            
            # Normalize test data
            X_test_normalized = X_test / 255.0
            
            # Evaluate model
            test_loss, test_accuracy = self.model.evaluate(
                X_test_normalized, y_test, verbose=1
            )
            
            # Get predictions
            predictions = self.model.predict(X_test_normalized, verbose=1)
            predicted_classes = np.argmax(predictions, axis=1)
            true_classes = np.argmax(y_test, axis=1)
            
            # Calculate detailed metrics
            results = self._calculate_detailed_metrics(
                true_classes, predicted_classes, predictions
            )
            
            # Add basic metrics
            results.update({
                'test_loss': float(test_loss),
                'test_accuracy': float(test_accuracy),
                'num_samples': len(X_test),
                'num_classes': len(self.class_names) if self.class_names else y_test.shape[1],
                'class_names': self.class_names
            })
            
            self.evaluation_results = results
            logger.info(f"Evaluation completed. Accuracy: {test_accuracy:.4f}")
            
            return results
            
        except Exception as e:
            logger.error(f"Error evaluating on arrays: {e}")
            return {}
    
    def _calculate_detailed_metrics(self, true_classes: np.ndarray, 
                                  predicted_classes: np.ndarray,
                                  predictions: np.ndarray) -> Dict[str, Any]:
        """
        Calculate detailed evaluation metrics
        
        Args:
            true_classes: True class labels
            predicted_classes: Predicted class labels
            predictions: Prediction probabilities
            
        Returns:
            Dictionary with detailed metrics
        """
        try:
            results = {}
            
            # Classification report
            class_report = classification_report(
                true_classes, predicted_classes,
                target_names=self.class_names,
                output_dict=True,
                zero_division=0
            )
            
            # Extract macro and weighted averages
            results['precision_macro'] = float(class_report['macro avg']['precision'])
            results['recall_macro'] = float(class_report['macro avg']['recall'])
            results['f1_macro'] = float(class_report['macro avg']['f1-score'])
            
            results['precision_weighted'] = float(class_report['weighted avg']['precision'])
            results['recall_weighted'] = float(class_report['weighted avg']['recall'])
            results['f1_weighted'] = float(class_report['weighted avg']['f1-score'])
            
            # Per-class metrics
            results['per_class_metrics'] = {}
            for i, class_name in enumerate(self.class_names):
                if class_name in class_report:
                    results['per_class_metrics'][class_name] = {
                        'precision': float(class_report[class_name]['precision']),
                        'recall': float(class_report[class_name]['recall']),
                        'f1_score': float(class_report[class_name]['f1-score']),
                        'support': int(class_report[class_name]['support'])
                    }
            
            # Confusion matrix
            cm = confusion_matrix(true_classes, predicted_classes)
            results['confusion_matrix'] = cm.tolist()
            
            # Top-k accuracy
            results['top_3_accuracy'] = float(self._calculate_top_k_accuracy(
                true_classes, predictions, k=3
            ))
            results['top_5_accuracy'] = float(self._calculate_top_k_accuracy(
                true_classes, predictions, k=5
            ))
            
            # Calculate AUC for multi-class (if applicable)
            if len(self.class_names) > 2:
                try:
                    auc_scores = self._calculate_multiclass_auc(
                        true_classes, predictions
                    )
                    results['auc_scores'] = auc_scores
                except Exception as e:
                    logger.warning(f"Could not calculate AUC scores: {e}")
            
            # Confidence statistics
            confidence_stats = self._calculate_confidence_statistics(predictions)
            results['confidence_statistics'] = confidence_stats
            
            return results
            
        except Exception as e:
            logger.error(f"Error calculating detailed metrics: {e}")
            return {}
    
    def _calculate_top_k_accuracy(self, true_classes: np.ndarray, 
                                predictions: np.ndarray, k: int = 3) -> float:
        """Calculate top-k accuracy"""
        try:
            top_k_predictions = np.argsort(predictions, axis=1)[:, -k:]
            correct = 0
            
            for i, true_class in enumerate(true_classes):
                if true_class in top_k_predictions[i]:
                    correct += 1
            
            return correct / len(true_classes)
            
        except Exception as e:
            logger.error(f"Error calculating top-{k} accuracy: {e}")
            return 0.0
    
    def _calculate_multiclass_auc(self, true_classes: np.ndarray, 
                                predictions: np.ndarray) -> Dict[str, float]:
        """Calculate AUC scores for multi-class classification"""
        try:
            n_classes = len(self.class_names)
            
            # Binarize the output
            y_true_binary = label_binarize(true_classes, classes=range(n_classes))
            
            auc_scores = {}
            
            # Calculate AUC for each class
            for i, class_name in enumerate(self.class_names):
                try:
                    fpr, tpr, _ = roc_curve(y_true_binary[:, i], predictions[:, i])
                    auc_score = auc(fpr, tpr)
                    auc_scores[class_name] = float(auc_score)
                except Exception as e:
                    logger.warning(f"Could not calculate AUC for class {class_name}: {e}")
                    auc_scores[class_name] = 0.0
            
            # Calculate macro average AUC
            auc_scores['macro_avg'] = float(np.mean(list(auc_scores.values())))
            
            return auc_scores
            
        except Exception as e:
            logger.error(f"Error calculating multiclass AUC: {e}")
            return {}
    
    def _calculate_confidence_statistics(self, predictions: np.ndarray) -> Dict[str, float]:
        """Calculate confidence statistics"""
        try:
            max_confidences = np.max(predictions, axis=1)
            
            stats = {
                'mean_confidence': float(np.mean(max_confidences)),
                'std_confidence': float(np.std(max_confidences)),
                'min_confidence': float(np.min(max_confidences)),
                'max_confidence': float(np.max(max_confidences)),
                'median_confidence': float(np.median(max_confidences)),
                'confidence_25th_percentile': float(np.percentile(max_confidences, 25)),
                'confidence_75th_percentile': float(np.percentile(max_confidences, 75))
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating confidence statistics: {e}")
            return {}
    
    def plot_confusion_matrix(self, save_path: str = None, 
                            figsize: Tuple[int, int] = (10, 8)) -> bool:
        """
        Plot confusion matrix
        
        Args:
            save_path: Path to save plot
            figsize: Figure size
            
        Returns:
            Success status
        """
        try:
            if 'confusion_matrix' not in self.evaluation_results:
                logger.error("No confusion matrix available. Run evaluation first.")
                return False
            
            cm = np.array(self.evaluation_results['confusion_matrix'])
            
            plt.figure(figsize=figsize)
            sns.heatmap(
                cm, 
                annot=True, 
                fmt='d', 
                cmap='Blues',
                xticklabels=self.class_names,
                yticklabels=self.class_names
            )
            
            plt.title('Confusion Matrix', fontsize=16, fontweight='bold')
            plt.xlabel('Predicted Label', fontsize=12)
            plt.ylabel('True Label', fontsize=12)
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Confusion matrix saved to: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            logger.error(f"Error plotting confusion matrix: {e}")
            return False
    
    def plot_class_performance(self, save_path: str = None,
                             figsize: Tuple[int, int] = (12, 8)) -> bool:
        """
        Plot per-class performance metrics
        
        Args:
            save_path: Path to save plot
            figsize: Figure size
            
        Returns:
            Success status
        """
        try:
            if 'per_class_metrics' not in self.evaluation_results:
                logger.error("No per-class metrics available. Run evaluation first.")
                return False
            
            metrics_data = self.evaluation_results['per_class_metrics']
            
            classes = list(metrics_data.keys())
            precision = [metrics_data[cls]['precision'] for cls in classes]
            recall = [metrics_data[cls]['recall'] for cls in classes]
            f1_score = [metrics_data[cls]['f1_score'] for cls in classes]
            
            x = np.arange(len(classes))
            width = 0.25
            
            fig, ax = plt.subplots(figsize=figsize)
            
            bars1 = ax.bar(x - width, precision, width, label='Precision', alpha=0.8)
            bars2 = ax.bar(x, recall, width, label='Recall', alpha=0.8)
            bars3 = ax.bar(x + width, f1_score, width, label='F1-Score', alpha=0.8)
            
            ax.set_xlabel('Classes', fontsize=12)
            ax.set_ylabel('Score', fontsize=12)
            ax.set_title('Per-Class Performance Metrics', fontsize=16, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(classes, rotation=45, ha='right')
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add value labels on bars
            def add_value_labels(bars):
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                           f'{height:.3f}', ha='center', va='bottom', fontsize=8)
            
            add_value_labels(bars1)
            add_value_labels(bars2)
            add_value_labels(bars3)
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Class performance plot saved to: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            logger.error(f"Error plotting class performance: {e}")
            return False
    
    def plot_confidence_distribution(self, save_path: str = None,
                                   figsize: Tuple[int, int] = (10, 6)) -> bool:
        """
        Plot confidence score distribution
        
        Args:
            save_path: Path to save plot
            figsize: Figure size
            
        Returns:
            Success status
        """
        try:
            if 'confidence_statistics' not in self.evaluation_results:
                logger.error("No confidence statistics available. Run evaluation first.")
                return False
            
            stats = self.evaluation_results['confidence_statistics']
            
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
            
            # Box plot
            confidence_data = [
                stats['min_confidence'],
                stats['confidence_25th_percentile'],
                stats['median_confidence'],
                stats['confidence_75th_percentile'],
                stats['max_confidence']
            ]
            
            ax1.boxplot([confidence_data], labels=['Confidence Scores'])
            ax1.set_ylabel('Confidence Score')
            ax1.set_title('Confidence Score Distribution')
            ax1.grid(True, alpha=0.3)
            
            # Statistics table
            ax2.axis('tight')
            ax2.axis('off')
            
            table_data = [
                ['Mean', f"{stats['mean_confidence']:.4f}"],
                ['Std Dev', f"{stats['std_confidence']:.4f}"],
                ['Min', f"{stats['min_confidence']:.4f}"],
                ['Max', f"{stats['max_confidence']:.4f}"],
                ['Median', f"{stats['median_confidence']:.4f}"],
                ['25th %ile', f"{stats['confidence_25th_percentile']:.4f}"],
                ['75th %ile', f"{stats['confidence_75th_percentile']:.4f}"]
            ]
            
            table = ax2.table(cellText=table_data,
                            colLabels=['Metric', 'Value'],
                            cellLoc='center',
                            loc='center')
            table.auto_set_font_size(False)
            table.set_fontsize(10)
            table.scale(1.2, 1.5)
            
            ax2.set_title('Confidence Statistics')
            
            plt.tight_layout()
            
            if save_path:
                plt.savefig(save_path, dpi=300, bbox_inches='tight')
                logger.info(f"Confidence distribution plot saved to: {save_path}")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            logger.error(f"Error plotting confidence distribution: {e}")
            return False
    
    def generate_evaluation_report(self, output_dir: str = '../evaluation_results/') -> bool:
        """
        Generate comprehensive evaluation report
        
        Args:
            output_dir: Directory to save evaluation results
            
        Returns:
            Success status
        """
        try:
            if not self.evaluation_results:
                logger.error("No evaluation results available. Run evaluation first.")
                return False
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Save evaluation results as JSON
            results_path = os.path.join(output_dir, 'evaluation_results.json')
            with open(results_path, 'w') as f:
                json.dump(self.evaluation_results, f, indent=2)
            
            # Generate plots
            cm_path = os.path.join(output_dir, 'confusion_matrix.png')
            self.plot_confusion_matrix(save_path=cm_path)
            
            perf_path = os.path.join(output_dir, 'class_performance.png')
            self.plot_class_performance(save_path=perf_path)
            
            conf_path = os.path.join(output_dir, 'confidence_distribution.png')
            self.plot_confidence_distribution(save_path=conf_path)
            
            # Generate text report
            report_path = os.path.join(output_dir, 'evaluation_report.txt')
            self._generate_text_report(report_path)
            
            logger.info(f"Evaluation report generated in: {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating evaluation report: {e}")
            return False
    
    def _generate_text_report(self, report_path: str) -> bool:
        """Generate text-based evaluation report"""
        try:
            with open(report_path, 'w') as f:
                f.write("CROP DISEASE DETECTION MODEL - EVALUATION REPORT\n")
                f.write("=" * 60 + "\n\n")
                
                # Basic metrics
                f.write("OVERALL PERFORMANCE:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Test Accuracy: {self.evaluation_results['test_accuracy']:.4f}\n")
                f.write(f"Test Loss: {self.evaluation_results['test_loss']:.4f}\n")
                f.write(f"Number of Samples: {self.evaluation_results['num_samples']}\n")
                f.write(f"Number of Classes: {self.evaluation_results['num_classes']}\n\n")
                
                # Macro averages
                f.write("MACRO AVERAGES:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Precision: {self.evaluation_results['precision_macro']:.4f}\n")
                f.write(f"Recall: {self.evaluation_results['recall_macro']:.4f}\n")
                f.write(f"F1-Score: {self.evaluation_results['f1_macro']:.4f}\n\n")
                
                # Top-k accuracy
                if 'top_3_accuracy' in self.evaluation_results:
                    f.write("TOP-K ACCURACY:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"Top-3 Accuracy: {self.evaluation_results['top_3_accuracy']:.4f}\n")
                    if 'top_5_accuracy' in self.evaluation_results:
                        f.write(f"Top-5 Accuracy: {self.evaluation_results['top_5_accuracy']:.4f}\n")
                    f.write("\n")
                
                # Per-class metrics
                if 'per_class_metrics' in self.evaluation_results:
                    f.write("PER-CLASS PERFORMANCE:\n")
                    f.write("-" * 30 + "\n")
                    f.write(f"{'Class':<20} {'Precision':<10} {'Recall':<10} {'F1-Score':<10} {'Support':<10}\n")
                    f.write("-" * 70 + "\n")
                    
                    for class_name, metrics in self.evaluation_results['per_class_metrics'].items():
                        f.write(f"{class_name:<20} {metrics['precision']:<10.4f} "
                               f"{metrics['recall']:<10.4f} {metrics['f1_score']:<10.4f} "
                               f"{metrics['support']:<10}\n")
                    f.write("\n")
                
                # Confidence statistics
                if 'confidence_statistics' in self.evaluation_results:
                    f.write("CONFIDENCE STATISTICS:\n")
                    f.write("-" * 30 + "\n")
                    stats = self.evaluation_results['confidence_statistics']
                    f.write(f"Mean Confidence: {stats['mean_confidence']:.4f}\n")
                    f.write(f"Std Deviation: {stats['std_confidence']:.4f}\n")
                    f.write(f"Min Confidence: {stats['min_confidence']:.4f}\n")
                    f.write(f"Max Confidence: {stats['max_confidence']:.4f}\n")
                    f.write(f"Median Confidence: {stats['median_confidence']:.4f}\n\n")
                
                # Model information
                f.write("MODEL INFORMATION:\n")
                f.write("-" * 30 + "\n")
                f.write(f"Model Path: {self.model_path}\n")
                f.write(f"Classes: {', '.join(self.class_names)}\n")
                
            logger.info(f"Text report saved to: {report_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating text report: {e}")
            return False
    
    def compare_models(self, model_paths: List[str], 
                      test_data_dir: str) -> Dict[str, Any]:
        """
        Compare multiple models on the same test dataset
        
        Args:
            model_paths: List of model file paths
            test_data_dir: Path to test dataset
            
        Returns:
            Comparison results
        """
        try:
            comparison_results = {}
            
            for i, model_path in enumerate(model_paths):
                logger.info(f"Evaluating model {i+1}/{len(model_paths)}: {model_path}")
                
                # Load and evaluate model
                if self.load_model(model_path):
                    results = self.evaluate_on_dataset(test_data_dir)
                    
                    model_name = os.path.basename(model_path)
                    comparison_results[model_name] = results
                else:
                    logger.warning(f"Failed to load model: {model_path}")
            
            # Generate comparison summary
            if comparison_results:
                summary = self._generate_comparison_summary(comparison_results)
                comparison_results['comparison_summary'] = summary
            
            return comparison_results
            
        except Exception as e:
            logger.error(f"Error comparing models: {e}")
            return {}
    
    def _generate_comparison_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comparison summary between models"""
        try:
            summary = {
                'best_accuracy': {'model': '', 'value': 0.0},
                'best_f1_macro': {'model': '', 'value': 0.0},
                'best_precision_macro': {'model': '', 'value': 0.0},
                'best_recall_macro': {'model': '', 'value': 0.0}
            }
            
            for model_name, model_results in results.items():
                if model_name == 'comparison_summary':
                    continue
                
                # Check accuracy
                if model_results.get('test_accuracy', 0) > summary['best_accuracy']['value']:
                    summary['best_accuracy'] = {
                        'model': model_name,
                        'value': model_results['test_accuracy']
                    }
                
                # Check F1 macro
                if model_results.get('f1_macro', 0) > summary['best_f1_macro']['value']:
                    summary['best_f1_macro'] = {
                        'model': model_name,
                        'value': model_results['f1_macro']
                    }
                
                # Check precision macro
                if model_results.get('precision_macro', 0) > summary['best_precision_macro']['value']:
                    summary['best_precision_macro'] = {
                        'model': model_name,
                        'value': model_results['precision_macro']
                    }
                
                # Check recall macro
                if model_results.get('recall_macro', 0) > summary['best_recall_macro']['value']:
                    summary['best_recall_macro'] = {
                        'model': model_name,
                        'value': model_results['recall_macro']
                    }
            
            return summary
            
        except Exception as e:
            logger.error(f"Error generating comparison summary: {e}")
            return {}

# Example usage and evaluation script
if __name__ == "__main__":
    print("🔬 Starting Crop Disease Detection Model Evaluation")
    
    # Initialize evaluator
    evaluator = ModelEvaluator()
    
    # Example model path (replace with actual path)
    model_path = '../trained_models/best_resnet50.h5'
    test_data_dir = '../data/test'
    
    if os.path.exists(model_path) and os.path.exists(test_data_dir):
        print("📁 Loading model and test data...")
        
        if evaluator.load_model(model_path):
            print("🎯 Running evaluation...")
            
            # Evaluate model
            results = evaluator.evaluate_on_dataset(test_data_dir)
            
            if results:
                print("📊 Evaluation Results:")
                print(f"   Accuracy: {results['test_accuracy']:.4f}")
                print(f"   F1-Score (Macro): {results['f1_macro']:.4f}")
                print(f"   Precision (Macro): {results['precision_macro']:.4f}")
                print(f"   Recall (Macro): {results['recall_macro']:.4f}")
                
                if 'top_3_accuracy' in results:
                    print(f"   Top-3 Accuracy: {results['top_3_accuracy']:.4f}")
                
                print("📈 Generating evaluation report...")
                evaluator.generate_evaluation_report('../evaluation_results/')
                
                print("✅ Evaluation completed successfully!")
                print("📂 Results saved in '../evaluation_results/' directory")
            else:
                print("❌ Evaluation failed")
        else:
            print("❌ Failed to load model")
    else:
        print(f"❌ Model or test data not found")
        print(f"   Model path: {model_path}")
        print(f"   Test data: {test_data_dir}")
        print("📝 Please ensure model is trained and test data is available")
    
    print("\n🔬 Model evaluation script completed!")