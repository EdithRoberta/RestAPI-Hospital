from typing import List, Optional
from pydantic import BaseModel

class DoctorRequest(BaseModel):
    name: str
    specialization: str
    
    class Config:
        orm_mode = True


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: Optional[str]
    
    class Config:
        orm_mode = True


class PatientRequest(BaseModel):
    name: str
    phone_number: str
    
    class Config:
        orm_mode = True


class PatientResponse(BaseModel):
    id: int
    name: str
    phone_number: Optional[str]
    
    class Config:
        orm_mode = True


class AssistantRequest(BaseModel):
    name: str
    
    class Config:
        orm_mode = True
        

class AssistantResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        orm_mode = True


class TreatmentRequest(BaseModel):
    name: str
    description: str
    
    class Config:
        orm_mode = True
        

class TreatmentResponse(BaseModel):
    id: int
    name: str
    description: str
    
    class Config:
        orm_mode = True


class DoctorPatientRequest(BaseModel):
    patient_id: int
    doctor_id: int
    
    class Config:
        orm_mode = True
        

class DoctorPatientResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    
    class Config:
        orm_mode = True


class PatientTreatmentRequest(BaseModel):
    treatment_id: int
    assistant_id: int
    
    class Config:
        orm_mode = True
        

class PatientTreatmentResponse(BaseModel):
    id: int
    doctors_patients_id: int
    treatment_id: int
    assistant_id: int
    
    class Config:
        orm_mode = True


class TreatmentsList(BaseModel):
    treatment_id: int
    
    class Config:
        orm_mode = True


class UpdatePatientTreatment(BaseModel):
    treatment_id: Optional[int]
    
    class Config:
        orm_mode = True
