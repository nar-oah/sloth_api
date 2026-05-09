from typing import TypeVar

from google import genai
from pydantic import BaseModel

from models import SuggestRes, TodoRes, WeekPlanRes


FAST_MODEL = "gemini-2.5-flash-lite"
THINK_MODEL = "gemini-2.5-flash-preview-05-20"

SUGGEST_TASK = "基于用户提供的本月目标与前几周目标，为我推荐本周的3-5个具体、可衡量、可实现、相关的目标。"

WEEK_PLAN_TASK = """
请根据用户提供的目标，为我创建一份从周一到周日的详细周度任务计划。请遵循以下要求：
目标对齐：确保从周一到周日的每日任务都紧密围绕「本周核心目标」展开，并服务于「本月目标」。
具体可执行：为每一天仅分配一个明确、可操作的核心任务内容。
""".strip()

TODO_TASK = """
你的任务是：
1. 分析与整合：仔细分析我提供的任务内容和目标。
2. 分解任务：将任务内容分解为数个逻辑连贯的主要阶段，并为每个阶段起一个清晰的标题。
3. 预估时间：预估并记录每个阶段需要几个小时完成。
4. 生成待办清单：在每个阶段下，生成一份详细的待办事项。
待办清单需要高度可操作，每个事项都应是一个具体的行动，并且任务分配不要偏离目标。
""".strip()

ResultT = TypeVar("ResultT", bound=BaseModel)
client = genai.Client()


def get_contents(task: str, contents: str) -> str:
    return f"{task}\n\n用户提供内容：\n{contents}"


def get_gen_res(model: str, contents: str, res_type: type[ResultT]) -> ResultT:
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config={
            "response_mime_type": "application/json",
            "response_json_schema": res_type.model_json_schema(),
        },
    )
    text = response.text if isinstance(response.text, str) else ""
    return res_type.model_validate_json(text)


def get_suggest_res(contents: str) -> SuggestRes:
    return get_gen_res(
        FAST_MODEL,
        get_contents(SUGGEST_TASK, contents),
        SuggestRes,
    )


def get_week_plan_res(contents: str) -> WeekPlanRes:
    return get_gen_res(
        THINK_MODEL,
        get_contents(WEEK_PLAN_TASK, contents),
        WeekPlanRes,
    )


def get_todo_res(contents: str) -> TodoRes:
    return get_gen_res(
        THINK_MODEL,
        get_contents(TODO_TASK, contents),
        TodoRes,
    )
