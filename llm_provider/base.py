# clawclaw/llm_provider/base.py
from abc import ABC, abstractmethod
from langchain_core.language_models.chat_models import BaseChatModel

class BaseLLMProvider(ABC):

    @abstractmethod
    def get_llm(self) -> BaseChatModel:
        pass