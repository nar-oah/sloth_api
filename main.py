from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import HealthRes, TodoStage
from service import get_suggest_res, get_todo_res, get_week_plan_res


app = FastAPI(title="Sloth AI Agent API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthRes)
def get_health() -> HealthRes:
    return HealthRes(status="ok")


@app.post("/suggest", response_model=list[str])
def get_suggest(req: str) -> list[str]:
    return get_suggest_res(req).root


@app.post("/writ", response_model=list[str])
def get_write(req: str) -> list[str]:
    return get_week_plan_res(req).root


@app.post("/todo", response_model=list[TodoStage])
def get_todo(req: str) -> list[TodoStage]:
    return get_todo_res(req).root


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
