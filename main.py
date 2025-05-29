from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from database import Student, init_db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ses_client import send_email

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

DATABASE_URL = "sqlite:///./emails.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

init_db()


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": "",
        "selected_department": "",
        "typed_message": ""
    })


@app.post("/send")
async def send_email_form(
    request: Request,
    message: str = Form(...),
    department: str = Form(...)
):
    db = SessionLocal()

    if department == "ALL":
        students = db.query(Student).all()
    else:
        students = db.query(Student).filter_by(department=department).all()

    db.close()

    failed_any = False

    for student in students:
        if not send_email(
            to_email=student.email,
            subject="Notification from College",
            body=message
        ):
            failed_any = True
            break  # stop early if any mail fails

    result_message = "Mail sent" if not failed_any else "Failed to send"

    return templates.TemplateResponse("index.html", {
        "request": request,
        "message": result_message,
        "selected_department": department,
        "typed_message": message
    })
