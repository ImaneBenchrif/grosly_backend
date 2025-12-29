from fastapi import FastAPI
from urls import router as grosly_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
#uvicorn main:grosly_app --host localhost --port 8000 --reload
grosly_app = FastAPI(title="Grosly API Office")
templates = Jinja2Templates(directory="templates")


grosly_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #mon domaine
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


grosly_app.include_router(grosly_router)

@grosly_app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )