"""
Seed script to populate database with complete disease information for all 38 classes
Run this script to add disease data from New Plant Diseases Dataset
"""

from database.connection import db_manager
from database.models import DiseaseInfo
from database.queries import db_queries
from complete_disease_data import COMPLETE_DISEASE_INFO

def seed_database():
    """Seed database with all 38 disease classes"""
    print("🌱 Starting database seeding with complete disease data...")
    print(f"📊 Total classes to seed: {len(COMPLETE_DISEASE_INFO)}")
    
    try:
        # Get database connection
        db = db_manager.get_connection()
        
        if db is None:
            print("❌ Failed to connect to database")
            return
        
        # Clear existing disease data (optional)
        if db_manager.db_type == 'mongodb':
            result = db.diseases.delete_many({})
            print(f"🗑️  Cleared {result.deleted_count} existing disease records")
        
        # Insert disease data
        count = 0
        for disease_key, disease_data in COMPLETE_DISEASE_INFO.items():
            disease = DiseaseInfo(
                name=disease_key,  # Use the class name as identifier
                description=disease_data['description'],
                symptoms=disease_data['symptoms'],
                treatment=disease_data['treatment'],
                prevention=disease_data['prevention']
            )
            
            # Add additional fields
            disease_dict = disease.to_dict()
            disease_dict['display_name'] = disease_data['name']
            disease_dict['crop'] = disease_data['crop']
            
            if db_manager.db_type == 'mongodb':
                db.diseases.insert_one(disease_dict)
                count += 1
                print(f"✅ Added: {disease_data['crop']} - {disease_data['name']}")
        
        print(f"\n🎉 Successfully seeded {count} disease classes!")
        print("\n📋 Summary by Crop:")
        
        # Print summary
        crops = {}
        for disease_data in COMPLETE_DISEASE_INFO.values():
            crop = disease_data['crop']
            crops[crop] = crops.get(crop, 0) + 1
        
        for crop, count in sorted(crops.items()):
            print(f"   {crop}: {count} classes")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    seed_database()
