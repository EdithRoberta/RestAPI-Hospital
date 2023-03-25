from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Doctor(Base):
    __tablename__ = 'doctors'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String)


class Patient(Base):
    __tablename__ = 'patients'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone_number = Column(String, unique=True)


class Assistant(Base):
    __tablename__ = 'assistants'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    

class Treatment(Base):
    __tablename__ = 'treatments'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    description = Column(String)


class DoctorPatient(Base):
    __tablename__= 'doctors_patients'
    
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    
    #relationships between tables
    patient = relationship('Patient', backref=backref('doctors_patients'))
    doctor = relationship('Doctor', backref=backref('doctors_patients'))
    
    #constraint an unique pair between fiels
    __table_args__ = (UniqueConstraint('patient_id', 'doctor_id'),)
    

class PatientTreatment(Base):
    __tablename__ = 'patient_treatment'
    
    id = Column(Integer, primary_key=True)
    doctors_patients_id = Column(Integer, ForeignKey('doctors_patients.id'))
    treatment_id = Column(Integer, ForeignKey('treatments.id'))
    assistant_id = Column(Integer, ForeignKey('assistants.id'))
    
    #relationships between tables
    doctor_patient = relationship('DoctorPatient', backref=backref('patient_treatment'))
    treatment = relationship('Treatment', backref=backref('patient_treatment'))
    assistant = relationship('Assistant', backref=backref('patient_treatment'))
    
    #constraint an unique pair between fiels
    __table_args__ = (UniqueConstraint('treatment_id', 'doctors_patients_id'),)
