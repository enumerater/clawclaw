from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.tracers.schemas import Run


class TokenCountCallback(BaseCallbackHandler):
    """独立的 Token 统计回调"""

    def __init__(self):
        super().__init__()
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

    def on_llm_end(self, response: Run, **kwargs):
        """LLM 结束后统计真实 Token"""
        try:
            usage = response.llm_output.get("token_usage", {})
            self.prompt_tokens = usage.get("prompt_tokens", 0)
            self.completion_tokens = usage.get("completion_tokens", 0)
            self.total_tokens = usage.get("total_tokens", 0)
        except Exception:
            pass

    def reset(self):
        """重置本轮统计"""
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

    def get_usage(self) -> dict:
        return {
            "prompt": self.prompt_tokens,
            "completion": self.completion_tokens,
            "total": self.total_tokens
        }