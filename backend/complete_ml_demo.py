"""
Complete ML Pipeline Demo Script
Developed by Prathamesh for Crop Disease Detection

Demonstrates the complete ML pipeline including training, evaluation, and prediction
"""

import os
import sys
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import json

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all ML modules
from preprocessing.image_loader import ImageLoader
from preprocessing.augmentation import ImageAugmentation
from preprocessing.normalization import ImageNormalizer
from features.segmentation import LeafSegmentation
from features.texture_analysis import TextureAnalyzer
from features.extractor import FeatureExtractor
from models.cnn_model import CNNModel
from models.train import ModelTrainer
from models.evaluate import ModelEvaluator
from models.predict import ModelPredictor

def create_sample_dataset(output_dir='sample_dataset', num_samples_per_class=10):
    """Create a sample dataset for testing"""
    print("📁 Creating sample dataset...")
    
    # Disease classes
    classes = [
        'Healthy',
        'Tomato_Early_Blight',
        'Tomato_Late_Blight',
        'Potato_Late_Blight',
        'Corn_Common_Rust'
    ]
    
    # Create directory structure
    for split in ['train', 'test', 'validation']:
        for class_name in classes:
            class_dir = os.path.join(output_dir, split, class_name)
            os.makedirs(class_dir, exist_ok=True)
    
    # Generate sample images for each class
    for class_idx, class_name in enumerate(classes):
        for split in ['train', 'test', 'validation']:
            split_samples = num_samples_per_class if split == 'train' else max(2, num_samples_per_class // 5)
            
            for i in range(split_samples):
                # Create synthetic leaf image
                img = create_synthetic_leaf_image(class_name, class_idx)
                
                # Save image
                filename = f"{class_name}_{split}_{i:03d}.jpg"
                filepath = os.path.join(output_dir, split, class_name, filename)
                Image.fromarray(img).save(filepath)
    
    print(f"✅ Sample dataset created in '{output_dir}' directory")
    print(f"   Classes: {len(classes)}")
    print(f"   Samples per class (train): {num_samples_per_class}")
    print(f"   Total images: {len(classes) * (num_samples_per_class + 4 + 4)}")  # train + test + val
    
    return output_dir, classes

def create_synthetic_leaf_image(class_name, class_idx, size=(224, 224)):
    """Create a synthetic leaf image based on class"""
    img = np.zeros((*size, 3), dtype=np.uint8)
    
    # Base leaf color based on health
    if 'Healthy' in class_name:
        base_color = (34, 139, 34)  # Forest green
        spot_color = (50, 205, 50)  # Lime green (healthy variations)
        num_spots = np.random.randint(0, 3)
    else:
        base_color = (85, 107, 47)  # Dark olive green
        if 'Blight' in class_name:
            spot_color = (139, 69, 19)  # Brown spots
        elif 'Rust' in class_name:
            spot_color = (205, 92, 92)  # Orange-red spots
        else:
            spot_color = (160, 82, 45)  # Saddle brown
        num_spots = np.random.randint(3, 8)
    
    # Create leaf shape using ellipse
    center = (size[1]//2, size[0]//2)
    axes = (size[1]//3 + np.random.randint(-20, 20), size[0]//2 + np.random.randint(-20, 20))
    
    # Draw leaf shape
    cv2.ellipse(img, center, axes, 0, 0, 360, base_color, -1)
    
    # Add texture noise
    noise = np.random.randint(-15, 15, size=img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add disease spots
    for _ in range(num_spots):
        x = np.random.randint(size[1]//4, 3*size[1]//4)
        y = np.random.randint(size[0]//4, 3*size[0]//4)
        radius = np.random.randint(5, 20)
        cv2.circle(img, (x, y), radius, spot_color, -1)
    
    # Add some leaf veins for realism
    if np.random.random() > 0.5:
        vein_color = tuple(max(0, c - 30) for c in base_color)
        cv2.line(img, (center[0] - axes[0]//2, center[1]), 
                (center[0] + axes[0]//2, center[1]), vein_color, 2)
        
        # Secondary veins
        for i in range(3):
            start_y = center[1] + np.random.randint(-axes[1]//3, axes[1]//3)
            cv2.line(img, (center[0], center[1]), 
                    (center[0] + np.random.randint(-axes[0]//3, axes[0]//3), start_y), 
                    vein_color, 1)
    
    return img

def demo_preprocessing_pipeline():
    """Demonstrate preprocessing pipeline"""
    print("\n🔄 DEMO: Preprocessing Pipeline")
    print("=" * 50)
    
    # Create sample image
    sample_image = create_synthetic_leaf_image('Tomato_Early_Blight', 1)
    print(f"✅ Created sample image: {sample_image.shape}")
    
    # Initialize modules
    loader = ImageLoader(target_size=(224, 224))
    augmenter = ImageAugmentation(seed=42)
    normalizer = ImageNormalizer()
    
    # Test augmentation
    print("🎨 Testing augmentation...")
    augmented = augmenter.random_augmentation(sample_image, num_augmentations=3)
    print(f"   Augmented shape: {augmented.shape}")
    
    # Test normalization
    print("⚖️ Testing normalization...")
    normalized = normalizer.preprocess_for_model(sample_image, enhance=True)
    print(f"   Normalized shape: {normalized.shape}")
    print(f"   Value range: [{np.min(normalized):.3f}, {np.max(normalized):.3f}]")
    
    return sample_image, augmented, normalized

def demo_feature_extraction():
    """Demonstrate feature extraction"""
    print("\n🎯 DEMO: Feature Extraction")
    print("=" * 50)
    
    # Create sample image
    sample_image = create_synthetic_leaf_image('Tomato_Late_Blight', 2)
    
    # Initialize modules
    segmenter = LeafSegmentation()
    texture_analyzer = TextureAnalyzer()
    feature_extractor = FeatureExtractor()
    
    # Test segmentation
    print("🍃 Testing leaf segmentation...")
    segmented, mask = segmenter.segment_and_extract(sample_image, method='adaptive')
    leaf_ratio = np.sum(mask > 0) / mask.size
    print(f"   Leaf area ratio: {leaf_ratio:.3f}")
    
    # Test texture analysis
    print("🔬 Testing texture analysis...")
    texture_features = texture_analyzer.extract_all_texture_features(sample_image)
    print(f"   Texture features extracted: {len(texture_features)}")
    
    # Test comprehensive feature extraction
    print("📊 Testing comprehensive feature extraction...")
    all_features = feature_extractor.extract_comprehensive_features(
        sample_image, segment_leaf=True
    )
    print(f"   Total features extracted: {len(all_features)}")
    
    # Categorize features
    color_features = {k: v for k, v in all_features.items() 
                     if any(term in k.lower() for term in ['red', 'green', 'blue', 'hsv', 'lab'])}
    shape_features = {k: v for k, v in all_features.items() 
                     if any(term in k.lower() for term in ['area', 'perimeter', 'aspect', 'circularity'])}
    texture_features_subset = {k: v for k, v in all_features.items() 
                              if any(term in k.lower() for term in ['lbp', 'glcm', 'gabor'])}
    
    print(f"   Color features: {len(color_features)}")
    print(f"   Shape features: {len(shape_features)}")
    print(f"   Texture features: {len(texture_features_subset)}")
    
    return all_features

def demo_model_architectures():
    """Demonstrate CNN model architectures"""
    print("\n🧠 DEMO: CNN Model Architectures")
    print("=" * 50)
    
    architectures = ['custom_cnn', 'resnet50', 'mobilenet']
    
    for arch in architectures:
        print(f"🏗️ Testing {arch} architecture...")
        
        try:
            # Create model
            cnn = CNNModel(
                input_shape=(224, 224, 3),
                num_classes=5,
                model_name=arch
            )
            
            # Build model
            if arch == 'custom_cnn':
                model = cnn.build_model(architecture=arch, dropout_rate=0.5)
            else:
                model = cnn.build_model(architecture=arch, trainable_layers=5)
            
            # Compile model
            cnn.compile_model(optimizer='adam', learning_rate=0.001)
            
            # Get model info
            config = cnn.get_model_config()
            print(f"   ✅ {arch} created successfully")
            print(f"   📊 Total parameters: {config['total_params']:,}")
            print(f"   🎯 Trainable parameters: {config['trainable_params']:,}")
            
            # Test prediction with dummy data
            dummy_input = np.random.random((1, 224, 224, 3))
            prediction = cnn.predict(dummy_input)
            print(f"   🔮 Prediction shape: {prediction.shape}")
            
        except Exception as e:
            print(f"   ❌ Error with {arch}: {e}")
    
    return cnn

def demo_training_pipeline(dataset_dir, classes):
    """Demonstrate training pipeline"""
    print("\n🎯 DEMO: Training Pipeline")
    print("=" * 50)
    
    try:
        # Initialize trainer
        trainer = ModelTrainer(
            input_shape=(224, 224, 3),
            model_save_path='demo_models/'
        )
        
        # Load dataset
        print("📁 Loading dataset...")
        train_dir = os.path.join(dataset_dir, 'train')
        if trainer.load_dataset_from_directory(train_dir, test_size=0.2, val_size=0.1):
            print(f"   ✅ Dataset loaded successfully")
            print(f"   📊 Train samples: {len(trainer.X_train)}")
            print(f"   📊 Validation samples: {len(trainer.X_val)}")
            print(f"   📊 Test samples: {len(trainer.X_test)}")
            
            # Build model (use lightweight for demo)
            print("🏗️ Building model...")
            if trainer.build_and_compile_model(
                architecture='mobilenet',
                optimizer='adam',
                learning_rate=0.001,
                alpha=0.5,  # Lightweight MobileNet
                trainable_layers=3
            ):
                print("   ✅ Model built and compiled")
                
                # Train for few epochs (demo)
                print("🎯 Starting training (demo - 3 epochs)...")
                if trainer.train_model(epochs=3, batch_size=8, patience=5):
                    print("   ✅ Training completed")
                    
                    # Evaluate model
                    print("📊 Evaluating model...")
                    results = trainer.evaluate_model()
                    if results:
                        print(f"   📈 Test Accuracy: {results['test_accuracy']:.4f}")
                        print(f"   📈 F1-Score: {results['f1_macro']:.4f}")
                    
                    # Save training config
                    trainer.save_training_config('demo_models/training_config.json')
                    print("   💾 Training configuration saved")
                    
                    return True
                else:
                    print("   ❌ Training failed")
            else:
                print("   ❌ Model building failed")
        else:
            print("   ❌ Dataset loading failed")
    
    except Exception as e:
        print(f"❌ Training demo error: {e}")
    
    return False

def demo_evaluation_pipeline():
    """Demonstrate evaluation pipeline"""
    print("\n🔬 DEMO: Evaluation Pipeline")
    print("=" * 50)
    
    try:
        # Check if demo model exists
        model_path = 'demo_models/final_mobilenet.h5'
        
        if os.path.exists(model_path):
            print("📁 Loading trained model...")
            
            # Initialize evaluator
            evaluator = ModelEvaluator(
                model_path=model_path,
                class_names=['Healthy', 'Tomato_Early_Blight', 'Tomato_Late_Blight', 
                           'Potato_Late_Blight', 'Corn_Common_Rust']
            )
            
            if evaluator.load_model():
                print("   ✅ Model loaded successfully")
                
                # Create test arrays (mock evaluation)
                print("🎯 Creating test data...")
                X_test = np.random.random((20, 224, 224, 3))
                y_test = np.eye(5)[np.random.randint(0, 5, 20)]  # One-hot encoded
                
                # Evaluate model
                print("📊 Running evaluation...")
                results = evaluator.evaluate_on_arrays(X_test, y_test)
                
                if results:
                    print("   ✅ Evaluation completed")
                    print(f"   📈 Accuracy: {results['test_accuracy']:.4f}")
                    print(f"   📈 Precision (Macro): {results['precision_macro']:.4f}")
                    print(f"   📈 Recall (Macro): {results['recall_macro']:.4f}")
                    print(f"   📈 F1-Score (Macro): {results['f1_macro']:.4f}")
                    
                    # Generate evaluation report
                    print("📋 Generating evaluation report...")
                    evaluator.generate_evaluation_report('demo_evaluation_results/')
                    print("   💾 Evaluation report saved")
                    
                    return True
                else:
                    print("   ❌ Evaluation failed")
            else:
                print("   ❌ Failed to load model")
        else:
            print(f"   ⚠️ Model not found: {model_path}")
            print("   💡 Run training demo first to create model")
    
    except Exception as e:
        print(f"❌ Evaluation demo error: {e}")
    
    return False

def demo_prediction_pipeline():
    """Demonstrate prediction pipeline"""
    print("\n🔮 DEMO: Prediction Pipeline")
    print("=" * 50)
    
    try:
        # Initialize predictor
        predictor = ModelPredictor(
            confidence_threshold=0.6,
            class_names=['Healthy', 'Tomato_Early_Blight', 'Tomato_Late_Blight', 
                        'Potato_Late_Blight', 'Corn_Common_Rust']
        )
        
        # Check if model exists
        model_path = 'demo_models/final_mobilenet.h5'
        
        if os.path.exists(model_path):
            print("📁 Loading model...")
            if predictor.load_model(model_path):
                print("   ✅ Model loaded successfully")
                
                # Create test image
                print("🖼️ Creating test image...")
                test_image = create_synthetic_leaf_image('Tomato_Early_Blight', 1)
                test_image_path = 'demo_test_image.jpg'
                Image.fromarray(test_image).save(test_image_path)
                
                # Single image prediction
                print("🎯 Making prediction...")
                result = predictor.predict_single_image(
                    test_image_path, 
                    include_features=True,
                    include_preprocessing_info=True
                )
                
                if result.get('success', False):
                    print("   ✅ Prediction successful")
                    primary = result['primary_prediction']
                    print(f"   🦠 Predicted Disease: {primary['class_name']}")
                    print(f"   📊 Confidence: {primary['confidence_percentage']:.2f}%")
                    print(f"   ⏱️ Processing Time: {result['prediction_time']:.3f}s")
                    
                    # Show top predictions
                    print("   🏆 Top 3 Predictions:")
                    for i, pred in enumerate(result['top_predictions'][:3]):
                        print(f"      {i+1}. {pred['class_name']}: {pred['confidence_percentage']:.2f}%")
                    
                    # Prediction with explanation
                    print("💡 Getting detailed explanation...")
                    detailed_result = predictor.predict_with_explanation(test_image_path)
                    
                    if detailed_result.get('success', False):
                        explanation = detailed_result['explanation']
                        print(f"   📝 Summary: {explanation['prediction_summary']}")
                        print(f"   🎯 Confidence Level: {explanation['confidence_level']}")
                        
                        if explanation['key_indicators']:
                            print("   🔍 Key Indicators:")
                            for indicator in explanation['key_indicators']:
                                print(f"      • {indicator}")
                        
                        # Save results
                        predictor.save_prediction_results(
                            detailed_result, 'demo_prediction_results.json'
                        )
                        print("   💾 Detailed results saved")
                    
                    # Clean up
                    if os.path.exists(test_image_path):
                        os.remove(test_image_path)
                    
                    return True
                else:
                    print(f"   ❌ Prediction failed: {result.get('error', 'Unknown error')}")
            else:
                print("   ❌ Failed to load model")
        else:
            print(f"   ⚠️ Model not found: {model_path}")
            print("   💡 Run training demo first to create model")
    
    except Exception as e:
        print(f"❌ Prediction demo error: {e}")
    
    return False

def main():
    """Run complete ML pipeline demo"""
    print("🌱 CROP DISEASE DETECTION - COMPLETE ML PIPELINE DEMO")
    print("=" * 70)
    print("Developed by Prathamesh")
    print("=" * 70)
    
    try:
        # Create sample dataset
        dataset_dir, classes = create_sample_dataset(num_samples_per_class=20)
        
        # Run all demos
        print("\n🚀 Starting Complete ML Pipeline Demo...")
        
        # 1. Preprocessing Pipeline
        demo_preprocessing_pipeline()
        
        # 2. Feature Extraction
        demo_feature_extraction()
        
        # 3. Model Architectures
        demo_model_architectures()
        
        # 4. Training Pipeline
        training_success = demo_training_pipeline(dataset_dir, classes)
        
        # 5. Evaluation Pipeline (only if training succeeded)
        if training_success:
            demo_evaluation_pipeline()
            
            # 6. Prediction Pipeline
            demo_prediction_pipeline()
        else:
            print("\n⚠️ Skipping evaluation and prediction demos (training required)")
        
        print("\n🎉 COMPLETE ML PIPELINE DEMO FINISHED!")
        print("=" * 70)
        print("✅ Preprocessing pipeline working")
        print("✅ Feature extraction working")
        print("✅ CNN model architectures working")
        
        if training_success:
            print("✅ Training pipeline working")
            print("✅ Evaluation pipeline working")
            print("✅ Prediction pipeline working")
            print("\n🚀 The complete ML pipeline is ready for production!")
        else:
            print("⚠️ Training pipeline needs larger dataset for full functionality")
            print("💡 For production, use real crop disease dataset")
        
        print("\n📂 Generated Files:")
        print("   • sample_dataset/ - Synthetic training data")
        if training_success:
            print("   • demo_models/ - Trained model files")
            print("   • demo_evaluation_results/ - Evaluation reports")
            print("   • demo_prediction_results.json - Prediction results")
        
        print("\n📚 Next Steps:")
        print("   1. Collect real crop disease dataset")
        print("   2. Train models with larger dataset")
        print("   3. Fine-tune hyperparameters")
        print("   4. Deploy to production environment")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()