"""
SQLAlchemy Database Module for Algorithm Analysis Results
Stores and manages algorithm complexity analysis data
"""

from sqlalchemy import create_engine, text, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# MySQL connection parameters
DB_USER = 'root'
DB_PASSWORD = ''  # Default XAMPP password is empty
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'alchemy'

# Create MySQL connection string
database_path = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_engine(database_path, echo=False)

# Create base class for declarative models
Base = declarative_base()

# Create session factory
Session = sessionmaker(bind=engine)


# ==================== TABLE MODEL ====================

class AlgorithmAnalysis(Base):
    """
    Table to store algorithm analysis results
    """
    __tablename__ = 'algorithm_analysis'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    algo = Column(String(100), nullable=False)
    items = Column(Integer, nullable=False)
    steps = Column(Integer, nullable=False)
    start_time = Column(BigInteger, nullable=False)
    end_time = Column(BigInteger, nullable=False)
    total_time_ms = Column(Integer, nullable=False)
    time_complexity = Column(String(50), nullable=False)
    path_to_graph = Column(String(500), nullable=True)
    created_at = Column(String(50), default=lambda: datetime.now().isoformat())
    
    def to_dict(self):
        """Convert model instance to dictionary"""
        return {
            'id': self.id,
            'algo': self.algo,
            'items': self.items,
            'steps': self.steps,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'total_time_ms': self.total_time_ms,
            'time_complexity': self.time_complexity,
            'path_to_graph': self.path_to_graph,
            'created_at': self.created_at
        }


# ==================== DATABASE FUNCTIONS ====================

def init_database():
    """
    Initialize database - create all tables if they don't exist
    """
    try:
        Base.metadata.create_all(engine)
        print("✓ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False


def save_analysis_result(data):
    """
    Save algorithm analysis result to database
    
    Args:
        data (dict): Dictionary containing analysis data with keys:
                    - algo, items, steps, start_time, end_time, 
                      total_time_ms, time_complexity, path_to_graph
    
    Returns:
        dict: Response with status code and saved instance ID
              Format: {'status': 'success', 'id': <id>, 'message': '...'}
              Or: {'status': 'error', 'message': '...'}
    """
    session = Session()
    try:
        # Create new analysis record
        analysis = AlgorithmAnalysis(
            algo=data.get('algo'),
            items=int(data.get('items', 0)),
            steps=int(data.get('steps', 0)),
            start_time=int(data.get('start_time', 0)),
            end_time=int(data.get('end_time', 0)),
            total_time_ms=int(data.get('total_time_ms', 0)),
            time_complexity=data.get('time_complexity', ''),
            path_to_graph=data.get('path_to_graph', '')
        )
        
        # Add and commit to database
        session.add(analysis)
        session.commit()
        
        # Get the ID of the saved instance
        saved_id = analysis.id
        
        # Return success response
        return {
            'status': 'success',
            'status_code': 201,
            'id': saved_id,
            'message': f'Algorithm analysis saved successfully with ID: {saved_id}',
            'data': analysis.to_dict()
        }
        
    except Exception as e:
        session.rollback()
        return {
            'status': 'error',
            'status_code': 500,
            'message': f'Failed to save analysis: {str(e)}'
        }
    finally:
        session.close()


def get_analysis_by_id(analysis_id):
    """
    Retrieve an analysis record by ID
    
    Args:
        analysis_id (int): ID of the analysis record
    
    Returns:
        dict: Analysis data or error message
    """
    session = Session()
    try:
        analysis = session.query(AlgorithmAnalysis).filter_by(id=analysis_id).first()
        if analysis:
            return {
                'status': 'success',
                'status_code': 200,
                'data': analysis.to_dict()
            }
        else:
            return {
                'status': 'error',
                'status_code': 404,
                'message': f'Analysis with ID {analysis_id} not found'
            }
    except Exception as e:
        return {
            'status': 'error',
            'status_code': 500,
            'message': f'Error retrieving analysis: {str(e)}'
        }
    finally:
        session.close()


def get_all_analyses():
    """
    Retrieve all analysis records
    
    Returns:
        dict: List of all analyses or error message
    """
    session = Session()
    try:
        analyses = session.query(AlgorithmAnalysis).all()
        return {
            'status': 'success',
            'status_code': 200,
            'count': len(analyses),
            'data': [analysis.to_dict() for analysis in analyses]
        }
    except Exception as e:
        return {
            'status': 'error',
            'status_code': 500,
            'message': f'Error retrieving analyses: {str(e)}'
        }
    finally:
        session.close()


# ==================== TEST CONNECTION ====================

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("\n✓ Connection successful to database!\n")
            return True
    except Exception as e:
        print(f"\n✗ Connection failed: {e}\n")
        return False


# ==================== MAIN EXECUTION ====================

if __name__ == '__main__':
    print("=" * 60)
    print("Algorithm Analysis Database Setup")
    print("=" * 60)
    
    # Test connection
    if test_connection():
        # Initialize database (create tables)
        init_database()
        
        # Example: Save sample data
        print("\n--- Testing Save Functionality ---")
        sample_data = {
            "algo": "Bubble Sort",
            "items": 1000,
            "steps": 10,
            "start_time": 36458241,
            "end_time": 239759234,
            "total_time_ms": 3,
            "time_complexity": "O(n²)",
            "path_to_graph": "/graphs/bubble_sort_20240204_123456_abc123.png"
        }
        
        result = save_analysis_result(sample_data)
        print(f"Save Result: {result}")
        
        # Retrieve all analyses
        if result['status'] == 'success':
            print("\n--- Testing Retrieve Functionality ---")
            saved_id = result['id']
            retrieve_result = get_analysis_by_id(saved_id)
            print(f"Retrieved Analysis: {retrieve_result}")
    
    print("\n" + "=" * 60)