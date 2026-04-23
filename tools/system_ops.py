import subprocess
from langchain_core.tools import tool
from tools.file_ops import WORKSPACE_DIR


@tool
def execute_shell(command: str) -> str:
    """
    当需要执行系统命令（如 pip install, git clone, npm run dev 等）时使用此工具。
    命令将默认在沙盒工作区(workspace)目录中执行。
    """
    # 🌟 核心：引入 Human-in-the-loop 安全确认循环
    print(f"\n" + "=" * 40)
    print(f"🚨 [安全拦截] Agent 请求执行命令:")
    print(f"💻 {command}")
    print("=" * 40)

    user_auth = input("👉 是否允许执行？(y/n): ").strip().lower()

    if user_auth not in ['y', 'yes']:
        print("[🚫 执行已取消]\n")
        # 将拒绝信息返回给大模型，模型会据此调整后续策略
        return "执行失败：人类用户拒绝了该命令的执行权限。请尝试其他方案或询问用户。"

    print("[✅ 授权成功，正在执行...]\n")

    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=WORKSPACE_DIR,
            capture_output=True,
            text=True,
            timeout=120
        )

        output = f"Exit Code: {result.returncode}\n"
        if result.stdout:
            stdout_text = result.stdout[:8000] + "\n...[截断]" if len(result.stdout) > 8000 else result.stdout
            output += f"STDOUT:\n{stdout_text}\n"
        if result.stderr:
            output += f"STDERR:\n{result.stderr}\n"

        return output

    except subprocess.TimeoutExpired:
        return f"执行命令 '{command}' 超时。"
    except Exception as e:
        return f"执行命令出错: {str(e)}"