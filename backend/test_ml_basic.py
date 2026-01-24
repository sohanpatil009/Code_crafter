"""
Basic ML Pipeline Test (Without TensorFlow)
Tests preprocessing, feature extraction, and segmentation
"""

import os
import sys
import numpy as np
import cv2
from PIL import Image

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import modules that don't require TensorFlow
from preprocessing.image_loader import ImageLoader
from preprocessing.augmentation import ImageAugmentation
from preprocessing.normalization import ImageNormalizer
from features.segmentation import LeafSegmentation
from features.texture_analysis import TextureAnalyzer

def create_test_leaf_image(size=(224, 224)):
    """Create a test leaf image"""
    img = np.zeros((*size, 3), dtype=np.uint8)
    
    # Create leaf shape using ellipse
    center = (size[1]//2, size[0]//2)
    axes = (size[1]//3, size[0]//2)
    
    # Draw leaf shape
    cv2.ellipse(img, center, axes, 0, 0, 360, (34, 139, 34), -1)  # Forest green
    
    # Add some texture
    noise = np.random.randint(-20, 20, size=img.shape, dtype=np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    
    # Add some brown spots (disease simulation)
    for _ in range(3):
        x = np.random.randint(size[1]//4, 3*size[1]//4)
        y = np.random.randint(size[0]//4, 3*size[0]//4)
        radius = np.random.randint(5, 15)
        cv2.circle(img, (x, y), radius, (139, 69, 19), -1)  # Brown spots
    
    return img

def test_image_preprocessing():
    """Test image preprocessing pipeline"""
    print("\n🔄 Testing Image Preprocessing Pipeline")
    print("=" * 50)
    
    try:
        # Create test image
        test_image = create_test_leaf_image()
        print(f"✅ Created test image: {test_image.shape}")
        
        # Save test image
        test_image_path = 'test_leaf.jpg'
        Image.fromarray(test_image).save(test_image_path)
        
        # Initialize modules
        loader = ImageLoader(target_size=(224, 224))
        augmenter = ImageAugmentation(seed=42)
        normalizer = ImageNormalizer()
        
        # Test image loading
        print("📁 Testing image loading...")
        loaded_image = loader.load_image(test_image_path, as_array=True)
        if loaded_image is not None:
            print(f"   ✅ Image loaded: {loaded_image.shape}")
        else:
            print("   ❌ Failed to load image")
            return False
        
        # Test image validation
        print("🔍 Testing image validation...")
        is_valid = loader.validate_image(test_image_path)
        print(f"   ✅ Image validation: {is_valid}")
        
        # Test augmentation
        print("🎨 Testing image augmentation...")
        augmented = augmenter.random_augmentation(loaded_image, num_augmentations=3)
        print(f"   ✅ Augmented image: {augmented.shape}")
        
        # Test normalization
        print("⚖️ Testing image normalization...")
        normalized = normalizer.preprocess_for_model(loaded_image, enhance=True)
        print(f"   ✅ Normalized image: {normalized.shape}")
        print(f"   📊 Value range: [{np.min(normalized):.3f}, {np.max(normalized):.3f}]")
        
        # Clean up
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in preprocessing test: {e}")
        return False

def test_leaf_segmentation():
    """Test leaf segmentation"""
    print("\n🍃 Testing Leaf Segmentation")
    print("=" * 50)
    
    try:
        # Create test image
        test_image = create_test_leaf_image()
        
        # Initialize segmentation
        segmenter = LeafSegmentation()
        
        # Test different segmentation methods
        methods = ['hsv', 'kmeans', 'adaptive']
        
        for method in methods:
            print(f"🔍 Testing {method} segmentation...")
            segmented, mask = segmenter.segment_and_extract(test_image, method=method)
            
            leaf_pixels = np.sum(mask > 0)
            total_pixels = mask.size
            leaf_ratio = leaf_pixels / total_pixels
            
            print(f"   ✅ {method}: Leaf area ratio = {leaf_ratio:.3f}")
            print(f"   📊 Leaf pixels: {leaf_pixels}/{total_pixels}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in segmentation test: {e}")
        return False

def test_texture_analysis():
    """Test texture analysis"""
    print("\n🔬 Testing Texture Analysis")
    print("=" * 50)
    
    try:
        # Create test image
        test_image = create_test_leaf_image()
        
        # Initialize texture analyzer
        analyzer = TextureAnalyzer()
        
        # Test LBP features
        print("📊 Testing LBP features...")
        lbp_features = analyzer.extract_lbp_features(test_image)
        print(f"   ✅ LBP features extracted: {len(lbp_features)}")
        
        # Test GLCM features
        print("📊 Testing GLCM features...")
        glcm_features = analyzer.extract_glcm_features(test_image)
        print(f"   ✅ GLCM features extracted: {len(glcm_features)}")
        
        # Test Gabor features
        print("📊 Testing Gabor features...")
        gabor_features = analyzer.extract_gabor_features(test_image)
        print(f"   ✅ Gabor features extracted: {len(gabor_features)}")
        
        # Test all texture features
        print("📊 Testing comprehensive texture analysis...")
        all_features = analyzer.extract_all_texture_features(test_image)
        print(f"   ✅ Total texture features: {len(all_features)}")
        
        # Show sample features
        print("\n📋 Sample texture features:")
        for i, (key, value) in enumerate(list(all_features.items())[:10]):
            print(f"   {key}: {value:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in texture analysis test: {e}")
        return False

def test_ml_service_basic():
    """Test ML service without model"""
    print("\n🔗 Testing ML Service (Mock Mode)")
    print("=" * 50)
    
    try:
        # Import ML service
        from services.ml_service import ml_service
        
        # Create test image
        test_image = create_test_leaf_image()
        test_image_path = 'test_ml_image.jpg'
        Image.fromarray(test_image).save(test_image_path)
        
        print("🔮 Testing ML service prediction (mock mode)...")
        result = ml_service.predict(test_image_path)
        
        if result:
            print("✅ ML Service prediction successful!")
            print(f"   🦠 Predicted disease: {result['disease_name']}")
            print(f"   📊 Confidence: {result['confidence']:.2f}%")
            print(f"   🔍 Features extracted: {result['processing_info']['features_extracted']}")
            print(f"   🍃 Leaf segmented: {result['image_analysis']['leaf_segmented']}")
            print(f"   🎨 Dominant color: {result['image_analysis']['dominant_color']}")
        else:
            print("❌ ML Service prediction failed")
            return False
        
        # Clean up
        if os.path.exists(test_image_path):
            os.remove(test_image_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error in ML service test: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🌱 CROP DISEASE DETECTION - BASIC ML PIPELINE TEST")
    print("=" * 60)
    print("Testing without TensorFlow (Model-independent components)")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Run tests
    if test_image_preprocessing():
        tests_passed += 1
    
    if test_leaf_segmentation():
        tests_passed += 1
    
    if test_texture_analysis():
        tests_passed += 1
    
    if test_ml_service_basic():
        tests_passed += 1
    
    # Summary
    print(f"\n🎉 TEST RESULTS SUMMARY")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}/{total_tests}")
    print(f"Success Rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n✅ ALL TESTS PASSED!")
        print("🚀 Basic ML pipeline is working correctly!")
        print("\n📋 What's Working:")
        print("   ✅ Image preprocessing pipeline")
        print("   ✅ Leaf segmentation algorithms")
        print("   ✅ Texture analysis features")
        print("   ✅ ML service integration (mock mode)")
        
        print("\n📝 Next Steps:")
        print("   1. Install TensorFlow: pip install tensorflow")
        print("   2. Train a model or get pre-trained model")
        print("   3. Run complete_ml_demo.py for full testing")
        print("   4. Test with real crop disease images")
    else:
        print(f"\n⚠️ {total_tests - tests_passed} tests failed")
        print("Please check the error messages above")
    
    print("\n🔬 Basic ML pipeline test completed!")

if __name__ == "__main__":
    main()