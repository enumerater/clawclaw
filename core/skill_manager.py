import os
import importlib.util
import inspect
from langchain_core.tools import BaseTool

SKILLS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../skills"))
os.makedirs(SKILLS_DIR, exist_ok=True)


class SkillManager:
    @staticmethod
    def load_dynamic_skills() -> list[BaseTool]:
        """动态扫描 skills 目录下的所有 python 文件，提取 Tool"""
        dynamic_tools = []
        for filename in os.listdir(SKILLS_DIR):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(SKILLS_DIR, filename)

                try:
                    # 动态加载模块
                    spec = importlib.util.spec_from_file_location(module_name, file_path)
                    module = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(module)

                    # 遍历模块内的所有成员，寻找 LangChain 的工具对象
                    for name, obj in inspect.getmembers(module):
                        if isinstance(obj, BaseTool):
                            dynamic_tools.append(obj)
                            print(f"[Skill Manager] 成功加载技能: {name} (来自 {filename})")
                except Exception as e:
                    print(f"[Skill Manager] 加载技能 {filename} 失败: {e}")

        return dynamic_tools