from fastapi import FastAPI, APIRouter, UploadFile, File
from backend.parser import extract_resume_text
from backend.role_prediction import predict_role
from backend.activity import extract_skills, analyze_role_match
from backend.improve_text import improve_resume
from backend.export import create_report
from backend.score import calculate_score
from pydantic import BaseModel
from backend.chat import ChatRequest, generate_response
router = APIRouter()

app = FastAPI()
app.include_router(router)

@router.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    # Extract Resume Text
    resume_text = extract_resume_text(file)

    # Predict Role
    predicted_role = predict_role(resume_text)

    # Extract Skills
    skills = extract_skills(resume_text)

    # Resume Suggestions
    suggestions = improve_resume(resume_text)

    # Calculate ATS Score
    score, breakdown = calculate_score(resume_text)

    # Create PDF Report
    create_report(
        "resume_report.pdf",
        score,
        predicted_role,
        skills,
        suggestions
    )

    # Return Response
    return {
        "message": "Resume uploaded successfully.",
        "resume_text": resume_text,
        "predicted_role": predicted_role,
        "skills": skills,
        "suggestions": suggestions,
        "score": score,
        "breakdown": breakdown
    }
    
class RoleSelection(BaseModel):
    resume_id: str
selected_role: str


selected_roles = {}


@router.post("/select-role")
async def select_role(data: RoleSelection):

    selected_roles[data.resume_id] = data.selected_role

    return {
        "message": "Role selected successfully.",
        "resume_id": data.resume_id,
        "selected_role": data.selected_role
    }
    
class RoleAnalysisRequest(BaseModel):
    resume_text: str
    target_role: str


@router.post("/analyze-role")
async def analyze_role(request: RoleAnalysisRequest):

    result = analyze_role_match(
        request.resume_text,
        request.target_role
    )

    return result 

@router.post("/chat")
async def chat(request: ChatRequest):

    answer = generate_response(
        request.resume_text,
        request.question
    )

    return {
        "answer": answer
    }   