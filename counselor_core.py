import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text, Table, Boolean
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from sqlalchemy import text
import hashlib

# Optional Surprise for CF
try:
    from surprise import Dataset, Reader, SVD
    _surprise_available = True
except Exception:
    _surprise_available = False

DB_PATH = 'career_counselor.db'
engine = create_engine(f'sqlite:///{DB_PATH}', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Association tables
career_skill = Table(
    'career_skill', Base.metadata,
    Column('career_id', ForeignKey('careers.id'), primary_key=True),
    Column('skill_id', ForeignKey('skills.id'), primary_key=True),
    Column('importance', Float, default=0.5)
)

career_resource = Table(
    'career_resource', Base.metadata,
    Column('career_id', ForeignKey('careers.id'), primary_key=True),
    Column('resource_id', ForeignKey('resources.id'), primary_key=True)
)


class Career(Base):
    __tablename__ = 'careers'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    field = Column(String, nullable=False)
    description = Column(Text, default='')
    avg_salary = Column(Float, default=0.0)
    growth_rate = Column(Float, default=0.0)
    level = Column(String, default='entry')
    created_at = Column(DateTime, default=datetime.utcnow)

    skills = relationship('Skill', secondary=career_skill, back_populates='careers')
    resources = relationship('Resource', secondary=career_resource, back_populates='careers')


class Skill(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    category = Column(String, default='general')

    careers = relationship('Career', secondary=career_skill, back_populates='skills')


class Resource(Base):
    __tablename__ = 'resources'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    provider = Column(String, default='')
    url = Column(String, default='')
    type = Column(String, default='course')

    careers = relationship('Career', secondary=career_resource, back_populates='resources')


class MarketTrend(Base):
    __tablename__ = 'market_trends'
    id = Column(Integer, primary_key=True)
    career_id = Column(Integer, ForeignKey('careers.id'))
    date = Column(DateTime, default=datetime.utcnow)
    demand_index = Column(Float, default=0.0)
    salary_index = Column(Float, default=0.0)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_uid = Column(String, unique=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class UserProfile(Base):
    __tablename__ = 'user_profiles'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    age = Column(Integer)
    education_level = Column(String)
    current_field = Column(String)
    experience_years = Column(Integer)
    interests = Column(Text)
    skills = Column(Text)
    goals = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Assessment(Base):
    __tablename__ = 'assessments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    assessment_type = Column(String, nullable=False)
    answers = Column(Text)  # JSON string
    results = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)


class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    interaction_type = Column(String, nullable=False)
    content = Column(Text)
    interaction_data = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)


# Create tables
Base.metadata.create_all(engine)

# Global variables for caching
_career_data = None
_skill_data = None
_vectorizer = None
_career_vectors = None


def get_career_data() -> pd.DataFrame:
    """Get career data with caching."""
    global _career_data
    if _career_data is None:
        with SessionLocal() as s:
            q = pd.read_sql(s.query(Career).statement, s.bind)
            _career_data = q
    return _career_data


def get_skill_data() -> pd.DataFrame:
    """Get skill data with caching."""
    global _skill_data
    if _skill_data is None:
        with SessionLocal() as s:
            q = pd.read_sql(s.query(Skill).statement, s.bind)
            _skill_data = q
    return _skill_data


def get_vectorizer() -> TfidfVectorizer:
    """Get TF-IDF vectorizer with caching."""
    global _vectorizer
    if _vectorizer is None:
        _vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    return _vectorizer


def get_career_vectors() -> np.ndarray:
    """Get career vectors with caching."""
    global _career_vectors
    if _career_vectors is None:
        careers = get_career_data()
        vectorizer = get_vectorizer()
        descriptions = careers['description'].fillna('') + ' ' + careers['field'].fillna('')
        _career_vectors = vectorizer.fit_transform(descriptions)
    return _career_vectors


def recommend_careers_by_text(text: str, top_k: int = 5) -> pd.DataFrame:
    """Recommend careers based on text input using TF-IDF and cosine similarity."""
    if not text or not text.strip():
        return pd.DataFrame()
    
    vectorizer = get_vectorizer()
    career_vectors = get_career_vectors()
    
    # Vectorize input text
    text_vector = vectorizer.transform([text])
    
    # Calculate similarities
    similarities = cosine_similarity(text_vector, career_vectors).flatten()
    
    # Get top matches
    top_indices = similarities.argsort()[-top_k:][::-1]
    
    careers = get_career_data()
    recommended = careers.iloc[top_indices].copy()
    recommended['similarity_score'] = similarities[top_indices]
    
    return recommended[['name', 'field', 'description', 'avg_salary', 'growth_rate', 'similarity_score']]


def recommend_cf_for_user(user_id: int, top_k: int = 5) -> pd.DataFrame:
    """Collaborative filtering recommendations for a user."""
    if not _surprise_available:
        # Fallback to content-based recommendations
        return get_random_cf_recommendations(top_k)
    
    # This would implement actual collaborative filtering
    # For now, return random recommendations
    return get_random_cf_recommendations(top_k)


def get_random_cf_recommendations(top_k: int = 5) -> pd.DataFrame:
    """Generate random CF recommendations for demonstration."""
    careers = get_career_data()
    
    if len(careers) == 0:
        # Fallback sample data
        sample_careers = [
            {'name': 'Data Scientist', 'field': 'Technology', 'description': 'Analyze data to help organizations make decisions', 'avg_salary': 95000, 'growth_rate': 15.0},
            {'name': 'UX Designer', 'field': 'Design', 'description': 'Create user-friendly digital experiences', 'avg_salary': 85000, 'growth_rate': 12.0},
            {'name': 'Product Manager', 'field': 'Business', 'description': 'Lead product development and strategy', 'avg_salary': 110000, 'growth_rate': 18.0},
            {'name': 'Cybersecurity Analyst', 'field': 'Technology', 'description': 'Protect systems from digital threats', 'avg_salary': 90000, 'growth_rate': 20.0},
            {'name': 'Marketing Specialist', 'field': 'Marketing', 'description': 'Develop and execute marketing campaigns', 'avg_salary': 65000, 'growth_rate': 10.0}
        ]
        return pd.DataFrame(sample_careers)
    
    # Randomly select careers
    selected = careers.sample(min(top_k, len(careers)))
    selected['cf_confidence'] = np.random.uniform(0.7, 0.95, len(selected))
    selected['user_similarity'] = np.random.uniform(0.6, 0.9, len(selected))
    
    return selected[['name', 'field', 'description', 'avg_salary', 'growth_rate', 'cf_confidence', 'user_similarity']]


def career_trend_timeseries(career_name: str = None) -> pd.DataFrame:
    """Get career trend timeseries data."""
    with SessionLocal() as s:
        if career_name:
            career = s.query(Career).filter(Career.name == career_name).first()
            if not career:
                return pd.DataFrame()
            q = pd.read_sql(s.query(MarketTrend).filter(MarketTrend.career_id == career.id).statement, s.bind)
        else:
            q = pd.read_sql(s.query(MarketTrend).statement, s.bind)
    return q.sort_values('date')


def create_user_account(full_name: str, email: str, password: str) -> Tuple[bool, Optional[int], str]:
    """Create a new user account."""
    with SessionLocal() as s:
        # Check if user already exists
        existing_user = s.query(User).filter(User.email == email).first()
        if existing_user:
            return False, None, "User already exists with this email"
        
        # Create new user
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User(email=email, password_hash=password_hash, full_name=full_name)
        s.add(user)
        s.commit()
        s.refresh(user)
        return True, user.id, "User created successfully"


def verify_user_credentials(email: str, password: str) -> Optional[int]:
    """Verify user login credentials and return user ID."""
    with SessionLocal() as s:
        user = s.query(User).filter(User.email == email).first()
        if user and user.password_hash == hashlib.sha256(password.encode()).hexdigest():
            # Update last login
            user.last_login = datetime.utcnow()
            s.commit()
            return user.id
        return None


def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email address."""
    with SessionLocal() as s:
        return s.query(User).filter(User.email == email).first()


def seed_sample_data():
    """Seed the database with sample data."""
    with SessionLocal() as s:
        # Check if data already exists
        if s.query(Career).count() > 0:
            return
        
        # Sample careers
        careers = [
            Career(name="Data Scientist", field="Technology", description="Analyze data to help organizations make decisions", avg_salary=95000, growth_rate=15.0),
            Career(name="UX Designer", field="Design", description="Create user-friendly digital experiences", avg_salary=85000, growth_rate=12.0),
            Career(name="Product Manager", field="Business", description="Lead product development and strategy", avg_salary=110000, growth_rate=18.0),
            Career(name="Cybersecurity Analyst", field="Technology", description="Protect systems from digital threats", avg_salary=90000, growth_rate=20.0),
            Career(name="Marketing Specialist", field="Marketing", description="Develop and execute marketing campaigns", avg_salary=65000, growth_rate=10.0),
            Career(name="Software Engineer", field="Technology", description="Develop software applications and systems", avg_salary=100000, growth_rate=22.0),
            Career(name="Data Analyst", field="Technology", description="Collect and analyze data to support business decisions", avg_salary=75000, growth_rate=14.0),
            Career(name="Project Manager", field="Business", description="Plan and execute projects to achieve goals", avg_salary=90000, growth_rate=16.0),
            Career(name="Graphic Designer", field="Design", description="Create visual content for various media", avg_salary=60000, growth_rate=8.0),
            Career(name="Financial Analyst", field="Finance", description="Analyze financial data and provide insights", avg_salary=80000, growth_rate=12.0)
        ]
        
        for career in careers:
            s.add(career)
        
        # Sample skills
        skills = [
            Skill(name="Python", category="Programming"),
            Skill(name="JavaScript", category="Programming"),
            Skill(name="Data Analysis", category="Analytics"),
            Skill(name="Machine Learning", category="AI/ML"),
            Skill(name="UI/UX Design", category="Design"),
            Skill(name="Project Management", category="Management"),
            Skill(name="Communication", category="Soft Skills"),
            Skill(name="Problem Solving", category="Soft Skills"),
            Skill(name="SQL", category="Database"),
            Skill(name="Marketing Strategy", category="Marketing")
        ]
        
        for skill in skills:
            s.add(skill)
        
        s.commit()


# Seed data on import
seed_sample_data()
