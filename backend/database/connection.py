from pymongo import MongoClient
import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class DatabaseConnection:
    """Database connection manager"""
    
    def __init__(self):
        self.db_type = Config.DATABASE_TYPE
        self.connection = None
        
    def connect_mongodb(self):
        """Connect to MongoDB"""
        try:
            client = MongoClient(Config.MONGODB_URI)
            db = client[Config.MONGODB_DB]
            print(f"✅ Connected to MongoDB: {Config.MONGODB_DB}")
            return db
        except Exception as e:
            print(f"❌ MongoDB connection error: {e}")
            return None
    
    def connect_postgresql(self):
        """Connect to PostgreSQL"""
        try:
            conn = psycopg2.connect(
                Config.POSTGRES_URI,
                cursor_factory=RealDictCursor
            )
            print("✅ Connected to PostgreSQL")
            return conn
        except Exception as e:
            print(f"❌ PostgreSQL connection error: {e}")
            return None
    
    def get_connection(self):
        """Get database connection based on config"""
        if self.db_type == 'mongodb':
            return self.connect_mongodb()
        elif self.db_type == 'postgresql':
            return self.connect_postgresql()
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

# Global database instance
db_manager = DatabaseConnection()
