from sqlalchemy import create_engine, func
from sqlalchemy import ForeignKey, Table, Column, Integer, String, DateTime, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.associationproxy import association_proxy

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine = create_engine('sqlite:///lib/gradebook.db')
Session = sessionmaker(bind=engine)
session = Session()

class Student(Base):
    __tablename__ = 'students'
    
    # Columns
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationships
    grades = relationship('Grade', back_populates='student')

    def __repr__(self):
        return f'<#Student(id={self.id} name={self.name})>'


class Course(Base):
    __tablename__ = 'courses'
    
    # Columns
    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationships
    grades = relationship('Grade', back_populates='course')

    def __repr__(self):
        return f'<#Course(id={self.id} name={self.name})>'


class Grade(Base):
    __tablename__ = 'grades'
    
    # Columns
    id = Column(Integer(), primary_key=True)
    score = Column(Integer())

    # Foreign Keys
    student_id = Column(Integer(), ForeignKey('students.id'))
    course_id = Column(Integer(), ForeignKey('courses.id'))

    # Relationships
    student = relationship('Student', back_populates='grades')
    course = relationship('Course', back_populates='grades')
    student_name = association_proxy('student', 'name')
    course_name = association_proxy('course', 'name')

    def __repr__(self):
        return f"""<#Grade(
        id={self.id} 
        score={self.score},
        student={self.student}, 
        course={self.course})>
        """
