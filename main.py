from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import AgentReq, HealthRes, SuggestRes, TodoRes, WeekPlanRes
from service import get_suggest_res, get_todo_res, get_week_plan_res


app = FastAPI(title="Sloth AI Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthRes)
def get_health() -> HealthRes:
    return HealthRes(status="ok")


@app.post("/suggest", response_model=SuggestRes)
def get_suggest(req: AgentReq) -> SuggestRes:
    return get_suggest_res(req.contents)


@app.post("/write", response_model=WeekPlanRes)
def get_write(req: AgentReq) -> WeekPlanRes:
    return get_week_plan_res(req.contents)


@app.post("/todo", response_model=TodoRes)
def get_todo(req: AgentReq) -> TodoRes:
    return get_todo_res(req.contents)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
