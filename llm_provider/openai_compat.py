from langchain_openai import ChatOpenAI
from .base import BaseLLMProvider
from .model_configs import LLMConfig

class OpenAICompatProvider(BaseLLMProvider):
    """
    OpenAI 协议兼容层
    只要传入对应的 LLMConfig，就能支持所有遵循 OpenAI 标准的模型
    """
    def __init__(self, config: LLMConfig):
        self.config = config

    def get_llm(self) -> ChatOpenAI:
        return ChatOpenAI(
            model=self.config.model_name,
            api_key=self.config.api_key,
            base_url=self.config.base_url,
            temperature=self.config.temperature,
            max_tokens=4096,
        )