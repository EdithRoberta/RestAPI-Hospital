from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, status
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.models import Doctor, Patient, Assistant, Treatment, DoctorPatient, PatientTreatment
from schema.schema import DoctorRequest, DoctorResponse, PatientRequest, PatientResponse, \
                          AssistantRequest, AssistantResponse, TreatmentRequest, TreatmentResponse, \
                          DoctorPatientRequest, DoctorPatientResponse, PatientTreatmentRequest, PatientTreatmentResponse, \
                          TreatmentsList, UpdatePatientTreatment
from typing import List
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordRequestForm, OAuth2PasswordBearer

app = FastAPI()

#creates the connection to PostgreSQL
DATABASE_URL = 'postgresql://postgres:pass@localhost:5432/postgres'

#creates an object using the previous URL that interacts with the database
engine = create_engine(DATABASE_URL)

#creates the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

security = HTTPBasic()


#creates a local session for database and closing it after being used
async def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


#creates general login for the user so it can manage all the methods
async def general_login(credentials: HTTPBasicCredentials = Depends(HTTPBasic())):
    username = credentials.username
    password = credentials.password
    if username != 'user' or password != 'pass':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Incorrect username or password',
                            headers={'WWW-Authenticate': 'Basic'})
    return username


#creates doctors
@app.post('/doctors/', response_model=DoctorResponse, dependencies=[Depends(general_login)])
async def create_doctor(doctor: DoctorRequest,
                        db: Session = Depends(get_db)):
    
    db_doctor = Doctor(name=doctor.name, specialization=doctor.specialization)
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor


#creates patients
@app.post('/patients/', response_model=PatientResponse, dependencies=[Depends(general_login)])
async def create_patient(patient:PatientRequest,
                         db: Session = Depends(get_db)):
    
    try:
        db_patient = Patient(name=patient.name, phone_number=patient.phone_number)
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Phone number already exists')
    
    return db_patient


#creates assistants
@app.post('/assistants/', response_model=AssistantResponse, dependencies=[Depends(general_login)])
async def create_assistant(assistant: AssistantRequest,
                           db: Session = Depends(get_db)):
    
    db_assistant = Assistant(name=assistant.name)
    db.add(db_assistant)
    db.commit()
    db.refresh(db_assistant)
    return db_assistant


#creates treatments
@app.post('/treatments/', response_model=TreatmentResponse, dependencies=[Depends(general_login)])
async def create_treatment(treatment: TreatmentRequest,
                           db: Session = Depends(get_db)):
    
    try:
        db_treatment = Treatment(name=treatment.name, description=treatment.description)
        db.add(db_treatment)
        db.commit()
        db.refresh(db_treatment)
    except IntegrityError:
        raise HTTPException(status_code=400, detail='Treatment name already exists')

    return db_treatment


#assign a patient to a doctor
@app.post('/doctor/patient', response_model=DoctorPatientResponse, dependencies=[Depends(general_login)])
async def assign_doctor_patient(doctor_patient: DoctorPatientRequest,
                                db: Session = Depends(get_db)):
    
    find_doctor = db.query(Doctor).filter(Doctor.id==doctor_patient.doctor_id).first()
    if not find_doctor:
        raise HTTPException(status_code=404, detail='Doctor not found')
    
    find_patient = db.query(Patient).filter(Patient.id==doctor_patient.patient_id).first()
    if not find_patient:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    db_doctor_patient = DoctorPatient(patient_id=doctor_patient.patient_id,
                                      doctor_id=doctor_patient.doctor_id)
    db.add(db_doctor_patient)
    try:
        db.commit()
        db.refresh(db_doctor_patient)
        return db_doctor_patient
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Pacient already assigned to this doctor')


#assign a treatment to a patient that has a doctor
@app.post('/patient/{doctor_patient_id}/treatment', response_model=PatientTreatmentResponse, dependencies=[Depends(general_login)])
async def assign_patient_treatment(patient_treatment: PatientTreatmentRequest,
                                   doctor_patient_id: int,
                                   db: Session = Depends(get_db)):
    
    find_assign_doctor_patient = db.query(DoctorPatient).filter(DoctorPatient.id==doctor_patient_id).first()
    if not find_assign_doctor_patient:
        raise HTTPException(status_code=404, detail='Couldn\'t find the id in the database')
    
    find_assistant = db.query(Assistant).filter(Assistant.id==patient_treatment.assistant_id).first()
    if not find_assistant:
        raise HTTPException(status_code=404, detail='Assistant not found')
    
    find_treatment = db.query(Treatment).filter(Treatment.id==patient_treatment.treatment_id).first()
    if not find_treatment:
        raise HTTPException(status_code=404, detail='Treatment not found')

    db_patient_treatment = PatientTreatment(doctors_patients_id=doctor_patient_id,
                                            treatment_id=patient_treatment.treatment_id,
                                            assistant_id=patient_treatment.assistant_id)
    db.add(db_patient_treatment)
    try:
        db.commit()
        db.refresh(db_patient_treatment)
        return db_patient_treatment
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail='Treatment already applied to this patient')


#list of all the doctors and the associated patients
@app.get('/doctor-patient', response_model=List[DoctorPatientResponse])
async def get_doctor_patient(db: Session = Depends(get_db),
                             current_user: str = Depends(general_login),
                             auth: HTTPBasic = Depends(security)):
    
    find_doctors_patients = db.query(DoctorPatient)
    response_list = find_doctors_patients.all()
    return response_list


#list of all treatments applied to a patient
@app.get('/doctor-patient/{doctors_patients_id}/treatments', response_model=List[TreatmentsList])
async def get_patient_treatments(doctors_patients_id: int, db: Session = Depends(get_db),
                                 current_user: str = Depends(general_login),
                                 auth: HTTPBasic = Depends(security)):
    
    find_doctor_patient = db.query(PatientTreatment).filter(PatientTreatment.doctors_patients_id==doctors_patients_id).first()
    if not find_doctor_patient:
        raise HTTPException(status_code=404, detail='Couldn\'t find the id in the database')
    
    find_treatments = db.query(PatientTreatment).filter(PatientTreatment.doctors_patients_id==doctors_patients_id).all()
    return find_treatments


#delete a treatment from a patient
@app.delete('/patient-treatment/{patient_treatment_id}')
async def delete_treatment(patient_treatment_id: int, db: Session = Depends(get_db),
                           current_user: str = Depends(general_login),
                           auth: HTTPBasic = Depends(security)):
    
    find_treatment = db.query(PatientTreatment).filter(PatientTreatment.id==patient_treatment_id).first()
    if not find_treatment:
        raise HTTPException(status_code=404, detail='Couldn\'nt find the id in the database')
    db.delete(find_treatment)
    db.commit()
    return 'The delete was successful'


#update a treatment from a patient
@app.patch('/patient-treatment/{patient_treatment_id}', response_model=PatientTreatmentResponse, dependencies=[Depends(general_login)])
async def update_treatment(new_treatment: UpdatePatientTreatment,
                           patient_treatment_id: int,
                           db: Session = Depends(get_db)):

    find_patient_treatment = db.query(PatientTreatment).filter(PatientTreatment.id==patient_treatment_id).first()
    if not find_patient_treatment:
        raise HTTPException(status_code=404, detail='Couldn\'nt find the id in the database')

    find_treatment = db.query(Treatment).filter(Treatment.id==new_treatment.treatment_id).first()
    if not find_treatment:
        raise HTTPException(status_code=404, detail='Couldn\'nt find the treatment id in the database')

    existing_treatment = db.query(PatientTreatment).filter(PatientTreatment.treatment_id==new_treatment.treatment_id,
                                                           PatientTreatment.doctors_patients_id==find_patient_treatment.doctors_patients_id).first()
    if existing_treatment:
        raise HTTPException(status_code=400, detail='Treatment already added')

    find_patient_treatment.treatment_id = find_treatment.id
    db.commit()
    return find_patient_treatment
