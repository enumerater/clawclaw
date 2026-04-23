import os
from dotenv import load_dotenv
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

import llm_provider



# 加载环境变量
load_dotenv()

# ==========================================
# 定义状态与工具
# ==========================================
class State(TypedDict):
    messages: Annotated[list, add_messages]

@tool
def execute_python(code: str) -> str:
    """
    当需要计算数学题、处理数据或验证逻辑时，使用此工具执行简单的 Python 代码。
    参数 code 必须是可执行的 Python 字符串。
    """
    print(f"\n[Tool Executing] 正在执行代码:\n{code}\n")
    try:
        local_env = {}
        exec(code, {}, local_env)
        return f"执行成功。提取的局部变量结果: {str(local_env)}"
    except Exception as e:
        return f"执行报错，请根据错误信息修复代码: {str(e)}"

tools = [execute_python]

# 初始化 LLM 并绑定工具
llm = llm_provider.get_active_llm()
llm_with_tools = llm.bind_tools(tools)

# ==========================================
# 构建图网络 (Graph)
# ==========================================
def chatbot(state: State):
    """大脑节点"""
    response = llm_with_tools.invoke(state["messages"])
    return {"messages": [response]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

app = graph_builder.compile()

# ==========================================
# 运行测试
# ==========================================
if __name__ == "__main__":
    print(f"🤖 ClawClaw已启动。输入 'quit' 退出。")
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            break

        events = app.stream(
            {"messages": [("user", user_input)]},
            stream_mode="values"
        )

        for event in events:
            latest_msg = event["messages"][-1]
            if latest_msg.type == "ai" and latest_msg.content:
                print(f"Agent: {latest_msg.content}")