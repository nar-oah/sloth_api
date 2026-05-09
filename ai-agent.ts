import { GoogleGenAI, Type } from "@google/genai";
export interface TodoRes {
  name: string;
  value: number;
  todos: string[];
}

const API_KEY = "AIzaSyC8GJGVaGemFuiIpTMNq1cmdI2-zW7nhXA";
const ai = new GoogleGenAI({ apiKey: API_KEY });
const thinkModel = "gemini-2.5-flash-preview-05-20";
const fastModel = "gemini-2.5-flash-lite";

async function callGemini(
  model: string,
  contents: string,
  prompt: string,
  schema: object,
): Promise<string> {
  const response = await ai.models.generateContent({
    model: model,
    contents: contents,
    config: {
      systemInstruction: prompt,
      responseMimeType: "application/json",
      responseSchema: schema,
    },
  });
  return response.text as string;
}
export async function suggestAgent(contents: string): Promise<string[]> {
  const prompt = `基于用户提供的本月目标与前几周目标，为我推荐本周的3-5个具体、可衡量、可实现、相关的目标。`;
  const schema = {
    type: Type.ARRAY,
    description: "按优先级排列目标",
    items: {
      type: Type.STRING,
    },
  };
  const res: string = await callGemini(fastModel, contents, prompt, schema);
  return JSON.parse(res);
}
export async function writAgent(contents: string): Promise<string[]> {
  const prompt = `请根据用户提供的目标，为我创建一份从周一到周日的详细周度任务计划。请遵循以下要求：
  **目标对齐：** 确保从周一到周日的每日任务都紧密围绕「本周核心目标」展开，并服务于「本月目标」。
  **具体可执行：** 为每一天仅分配一个明确、可操作的核心任务内容。`;
  const schema = {
    type: Type.ARRAY,
    maxItems: "7",
    description:
      "从周一到周日排列任务内容，仅保留具体任务内容不保留星期等时间信息",
    items: {
      type: Type.STRING,
    },
  };
  const res = await callGemini(thinkModel, contents, prompt, schema);
  return JSON.parse(res);
}
export async function todoAgent(contents: string): Promise<TodoRes[]> {
  const prompt = `
你的任务是：
1.  **分析与整合**: 仔细分析我提供的任务内容和目标。
2.  **分解任务**: 将任务内容分解为数个逻辑连贯的主要阶段，并为每个阶段起一个清晰的标题。
3.  **预估时间**: 预估并记录每个阶段需要几个小时完成。
4.  **生成待办清单**: 在每个阶段下，生成一份详细的待办事项（To-do list）。这份清单需要：
    *   **高度可操作**: 每个事项都应是一个具体的行动，而不是一个模糊的目标。
    *   **目标匹配**: 任务的分配不要偏离目标。`;
  const schema = {
    type: Type.ARRAY,
    items: {
      type: Type.OBJECT,
      properties: {
        name: {
          type: Type.STRING,
          description: "阶段名称",
        },
        value: {
          type: Type.NUMBER,
          description: "预计完成小时数（允许小数）",
        },
        todos: {
          type: Type.ARRAY,
          description: "待办事项内容",
          items: {
            type: Type.STRING,
          },
        },
      },
    },
  };
  const res = await callGemini(thinkModel, contents, prompt, schema);
  return JSON.parse(res);
}
