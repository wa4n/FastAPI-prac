from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from App import Models
from App.database import engine
from App.Routers import posts, users, Auth, Votes


# Models.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(Auth.router)
app.include_router(Votes.router)
@app.get("/")
def root():
    return {'message': 'HELLO NERMIE!'}





