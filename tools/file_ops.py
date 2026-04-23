import os
from pathlib import Path  # 企业级都用 Path，比 os 更安全
from langchain_core.tools import tool

# 当前文件路径：clawclaw/tools/file_ops.py
THIS_FILE = Path(__file__).resolve()

# 项目包根目录：clawclaw/
PACKAGE_ROOT = THIS_FILE.parents[1]

# 工作区：放在 clawclaw/.workspace
WORKSPACE_DIR = PACKAGE_ROOT / ".workspace"

# 自动创建
WORKSPACE_DIR.mkdir(exist_ok=True, parents=True)


def _get_safe_path(filename: str) -> Path:
    """安全路径检查：绝对禁止越权访问"""
    file_path = (WORKSPACE_DIR / filename).resolve()

    # 严格安全校验：必须在工作区内
    if not file_path.is_relative_to(WORKSPACE_DIR):
        raise ValueError(f"安全警告：禁止访问工作区外的文件 → {filename}")

    return file_path


# ========================
# 工具函数
# ========================
@tool
def list_workspace(sub_path: str = "") -> str:
    """查看工作区文件目录"""
    try:
        target_dir = _get_safe_path(sub_path)
        files = [f.name for f in target_dir.iterdir()] if target_dir.exists() else []
        return f"目录 {sub_path} 内容：\n" + "\n".join(files) if files else "目录为空"
    except Exception as e:
        return f"列出失败：{str(e)}"


@tool
def read_file(filename: str) -> str:
    """读取文件内容"""
    try:
        filepath = _get_safe_path(filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            if len(content) > 12000:
                return content[:12000] + "\n...[内容过长已截断...]"
            return content
    except Exception as e:
        return f"读取失败：{str(e)}"


@tool
def write_file(filename: str, content: str) -> str:
    """写入文件（自动创建目录）"""
    try:
        filepath = _get_safe_path(filename)
        filepath.parent.mkdir(exist_ok=True, parents=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"✅ 写入成功：{filename}"
    except Exception as e:
        return f"❌ 写入失败：{str(e)}"


@tool
def patch_file(filename: str, old_str: str, new_str: str) -> str:
    """
    当需要修改文件中的某一段特定代码或文本时，使用此工具。
    它会在文件中查找精确的 old_str 并替换为 new_str。
    注意：old_str 必须与文件中的内容完全匹配（包括空格和换行）。
    """
    try:
        filepath = _get_safe_path(filename)

        if not os.path.exists(filepath):
            return f"错误：文件 {filename} 不存在，请先使用 write_file 创建。"

        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if old_str not in content:
            return (f"错误：未在文件中找到指定的 old_str。\n"
                    f"请确保空白字符和缩进完全一致，或者先使用 read_file 查看文件当前状态。")

        # 替换文本
        new_content = content.replace(old_str, new_str, 1)  # 默认只替换匹配到的第一处

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return f"成功修改文件: {filename}"
    except Exception as e:
        return f"修改文件失败: {str(e)}"
