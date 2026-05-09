from pydantic import AliasChoices, BaseModel, Field, RootModel


class HealthRes(BaseModel):
    status: str = Field(description="服务健康检查状态。")


class AgentReq(BaseModel):
    contents: str = Field(
        validation_alias=AliasChoices("contents", "req"),
        description="用户提供的目标或任务内容。",
    )


class SuggestRes(RootModel[list[str]]):
    root: list[str] = Field(
        min_length=3,
        max_length=5,
        description="按优先级排列的本周目标，来自用户提供的本月目标与前几周目标。",
    )


class WeekPlanRes(RootModel[list[str]]):
    root: list[str] = Field(
        min_length=7,
        max_length=7,
        description="从周一到周日排列的每日核心任务，仅包含具体任务内容。",
    )


class TodoStage(BaseModel):
    name: str = Field(description="任务阶段名称。")
    value: float = Field(description="预计完成小时数，允许小数。")
    todos: list[str] = Field(description="该阶段下高度可执行的待办事项内容。")


class TodoRes(RootModel[list[TodoStage]]):
    root: list[TodoStage] = Field(
        description="按执行顺序排列的任务阶段及其待办事项。",
    )
