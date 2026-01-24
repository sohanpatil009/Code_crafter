from datetime import datetime
from typing import List, Dict, Optional
from database.connection import db_manager
from database.models import PredictionRecord, DiseaseInfo, UserPreference

class DatabaseQueries:
    """Database query operations"""
    
    def __init__(self):
        self.db = db_manager.get_connection()
    
    # Prediction Records
    def save_prediction(self, prediction: PredictionRecord) -> str:
        """Save prediction record to database"""
        try:
            if db_manager.db_type == 'mongodb':
                result = self.db.predictions.insert_one(prediction.to_dict())
                return str(result.inserted_id)
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error saving prediction: {e}")
            return None
    
    def get_prediction_history(self, user_id: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Get prediction history"""
        try:
            if db_manager.db_type == 'mongodb':
                query = {'user_id': user_id} if user_id else {}
                results = self.db.predictions.find(query).sort('timestamp', -1).limit(limit)
                return list(results)
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error fetching history: {e}")
            return []
    
    def get_prediction_by_id(self, prediction_id: str) -> Optional[Dict]:
        """Get specific prediction by ID"""
        try:
            if db_manager.db_type == 'mongodb':
                from bson.objectid import ObjectId
                return self.db.predictions.find_one({'_id': ObjectId(prediction_id)})
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error fetching prediction: {e}")
            return None
    
    # Disease Information
    def get_disease_info(self, disease_name: str) -> Optional[Dict]:
        """Get disease information by name"""
        try:
            if db_manager.db_type == 'mongodb':
                return self.db.diseases.find_one({'name': disease_name})
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error fetching disease info: {e}")
            return None
    
    def get_all_diseases(self) -> List[Dict]:
        """Get all diseases"""
        try:
            if db_manager.db_type == 'mongodb':
                return list(self.db.diseases.find())
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error fetching diseases: {e}")
            return []
    
    def save_disease_info(self, disease: DiseaseInfo) -> str:
        """Save disease information"""
        try:
            if db_manager.db_type == 'mongodb':
                result = self.db.diseases.insert_one(disease.to_dict())
                return str(result.inserted_id)
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error saving disease info: {e}")
            return None
    
    # User Preferences
    def save_user_preference(self, preference: UserPreference) -> bool:
        """Save or update user language preference"""
        try:
            if db_manager.db_type == 'mongodb':
                self.db.preferences.update_one(
                    {'user_id': preference.user_id},
                    {'$set': preference.to_dict()},
                    upsert=True
                )
                return True
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error saving preference: {e}")
            return False
    
    def get_user_preference(self, user_id: str) -> Optional[Dict]:
        """Get user language preference"""
        try:
            if db_manager.db_type == 'mongodb':
                return self.db.preferences.find_one({'user_id': user_id})
            else:
                # PostgreSQL implementation
                pass
        except Exception as e:
            print(f"Error fetching preference: {e}")
            return None

# Global query instance
db_queries = DatabaseQueries()
