from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from llm_provider import get_active_llm
from tools.file_ops import read_file, write_file, list_workspace, patch_file
from core.skill_manager import SkillManager
from tools.system_ops import execute_shell
from tools.web_ops import web_fetch


# 1. 定义状态 (如果未来状态变复杂，可以单独抽离到 state.py)
class State(TypedDict):
    messages: Annotated[list, add_messages]

class ClawClawAgent:
    def __init__(self):
        self.llm = get_active_llm()
        self.tools = self._gather_tools()

        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self.app = self._build_graph()


    def _gather_tools(self, execute_python=None):
        """组合内置工具和动态加载的技能"""

        base_tools = [
            list_workspace, 
            read_file,
            write_file,
            patch_file,
            execute_shell,
            web_fetch,
        ]
        dynamic_tools = SkillManager.load_dynamic_skills()
        return base_tools + dynamic_tools

    def _build_graph(self):
        """构建图网络"""
        def chatbot_node(state: State):
            response = self.llm_with_tools.invoke(state["messages"])
            return {"messages": [response]}

        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", chatbot_node)
        graph_builder.add_node("tools", ToolNode(tools=self.tools))

        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_conditional_edges("chatbot", tools_condition)
        graph_builder.add_edge("tools", "chatbot")

        return graph_builder.compile()

    def chat(self, user_input: str, config=None):
        """与 Agent 交互的生成器接口"""
        events = self.app.stream(
            {"messages": [("user", user_input)]},
            stream_mode="values",
            config=config
        )
        for event in events:
            latest_msg = event["messages"][-1]
            if latest_msg.type == "ai" and latest_msg.content:
                yield latest_msg.content