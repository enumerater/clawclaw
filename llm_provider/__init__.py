# clawclaw/llm_provider/__init__.py
from .model_configs import config_manager
from .openai_compat import OpenAICompatProvider


def get_active_llm():
    """
    模型工厂：
    """

    active_model_id = config_manager.get_active_model_id()

    config = config_manager.get_config(active_model_id)

    print(f"[LLM Factory] 成功加载模型: {config.model_name} (ID: {active_model_id})")

    provider = OpenAICompatProvider(config)
    return provider.get_llm()