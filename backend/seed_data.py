"""
Seed script to populate database with sample disease information
Run this script to add initial disease data to the database
"""

from database.connection import db_manager
from database.models import DiseaseInfo
from database.queries import db_queries

# Sample disease data
DISEASE_DATA = [
    {
        'name': 'Tomato_Early_Blight',
        'description': 'Early blight is a common tomato disease caused by the fungus Alternaria solani. It affects leaves, stems, and fruits.',
        'symptoms': [
            'Dark brown spots with concentric rings on older leaves',
            'Yellowing of leaves around spots',
            'Leaf drop starting from bottom of plant',
            'Stem lesions and fruit spots'
        ],
        'treatment': 'Remove infected leaves, apply fungicides containing chlorothalonil or copper-based products. Improve air circulation.',
        'prevention': 'Use disease-resistant varieties, practice crop rotation, avoid overhead watering, mulch around plants, and maintain proper spacing.'
    },
    {
        'name': 'Tomato_Late_Blight',
        'description': 'Late blight is a devastating disease caused by Phytophthora infestans. It can destroy entire crops quickly.',
        'symptoms': [
            'Water-soaked spots on leaves',
            'White fuzzy growth on leaf undersides',
            'Brown lesions on stems',
            'Firm brown spots on fruits'
        ],
        'treatment': 'Remove and destroy infected plants immediately. Apply fungicides with mancozeb or chlorothalonil preventively.',
        'prevention': 'Plant resistant varieties, ensure good drainage, avoid overhead irrigation, and monitor weather conditions.'
    },
    {
        'name': 'Tomato_Healthy',
        'description': 'Healthy tomato plant with no visible disease symptoms.',
        'symptoms': [
            'Green, vibrant leaves',
            'Strong stem growth',
            'No spots or discoloration',
            'Normal fruit development'
        ],
        'treatment': 'No treatment needed. Continue regular care and monitoring.',
        'prevention': 'Maintain good cultural practices, proper watering, fertilization, and pest management.'
    },
    {
        'name': 'Potato_Early_Blight',
        'description': 'Early blight in potatoes is caused by Alternaria solani, affecting foliage and tubers.',
        'symptoms': [
            'Brown spots with target-like rings on leaves',
            'Yellowing and wilting of lower leaves',
            'Reduced tuber size',
            'Dark lesions on tubers'
        ],
        'treatment': 'Apply fungicides, remove infected foliage, and ensure proper plant nutrition.',
        'prevention': 'Use certified disease-free seed potatoes, practice crop rotation, and maintain adequate soil fertility.'
    },
    {
        'name': 'Potato_Late_Blight',
        'description': 'Late blight in potatoes is caused by Phytophthora infestans, the same pathogen that caused the Irish potato famine.',
        'symptoms': [
            'Water-soaked lesions on leaves',
            'White mold on leaf undersides',
            'Blackened stems',
            'Brown rot in tubers'
        ],
        'treatment': 'Destroy infected plants, apply protective fungicides, and harvest tubers carefully.',
        'prevention': 'Plant resistant varieties, avoid overhead irrigation, and monitor weather for favorable disease conditions.'
    },
    {
        'name': 'Potato_Healthy',
        'description': 'Healthy potato plant showing normal growth and development.',
        'symptoms': [
            'Lush green foliage',
            'Strong plant structure',
            'No disease symptoms',
            'Good tuber formation'
        ],
        'treatment': 'No treatment required. Continue regular maintenance.',
        'prevention': 'Follow good agricultural practices and regular monitoring.'
    },
    {
        'name': 'Corn_Common_Rust',
        'description': 'Common rust is a fungal disease caused by Puccinia sorghi, affecting corn leaves.',
        'symptoms': [
            'Small, circular to elongate brown pustules on leaves',
            'Pustules on both leaf surfaces',
            'Yellowing of leaves',
            'Reduced photosynthesis'
        ],
        'treatment': 'Apply fungicides if disease is severe. Usually not economically damaging.',
        'prevention': 'Plant resistant hybrids, ensure proper plant spacing, and practice crop rotation.'
    },
    {
        'name': 'Corn_Gray_Leaf_Spot',
        'description': 'Gray leaf spot is caused by Cercospora zeae-maydis, a serious corn disease.',
        'symptoms': [
            'Rectangular gray to tan lesions on leaves',
            'Lesions parallel to leaf veins',
            'Severe leaf blight',
            'Premature plant death'
        ],
        'treatment': 'Apply fungicides at early disease stages. Remove crop residue after harvest.',
        'prevention': 'Use resistant hybrids, practice crop rotation, and manage crop residue.'
    },
    {
        'name': 'Corn_Healthy',
        'description': 'Healthy corn plant with no disease symptoms.',
        'symptoms': [
            'Dark green leaves',
            'Strong stalk',
            'Normal ear development',
            'No lesions or spots'
        ],
        'treatment': 'No treatment needed. Maintain regular care.',
        'prevention': 'Continue good management practices and regular scouting.'
    }
]

def seed_database():
    """Seed database with disease information"""
    print("🌱 Starting database seeding...")
    
    try:
        # Get database connection
        db = db_manager.get_connection()
        
        if db is None:
            print("❌ Failed to connect to database")
            return
        
        # Clear existing disease data (optional)
        if db_manager.db_type == 'mongodb':
            db.diseases.delete_many({})
            print("🗑️ Cleared existing disease data")
        
        # Insert disease data
        count = 0
        for disease_data in DISEASE_DATA:
            disease = DiseaseInfo(**disease_data)
            result = db_queries.save_disease_info(disease)
            if result:
                count += 1
                print(f"✅ Added: {disease_data['name']}")
        
        print(f"\n🎉 Successfully seeded {count} diseases!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")

if __name__ == '__main__':
    seed_database()
