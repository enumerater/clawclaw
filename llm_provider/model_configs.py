import os
import sys
import yaml
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    provider: str
    model_name: str
    api_key: str
    base_url: Optional[str] = None
    temperature: float = 0.0

class ConfigManager:
    """模型配置管理器 """

    def __init__(self, config_path: str = "models.yaml"):
        # 检查配置文件是否存在
        if not os.path.exists(config_path):
            print(f"\n❌ 错误：未找到模型配置文件 {config_path}")
            print("请创建该文件并配置模型信息后重试。\n")
            sys.exit(1)

        # 加载 YAML
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._raw_configs = yaml.safe_load(f) or {}
        except Exception as e:
            print(f"\n❌ 错误：配置文件解析失败：{str(e)}")
            print("请检查 YAML 格式是否正确。\n")
            sys.exit(1)

    def get_active_model_id(self) -> str:
        """
        从 yaml 中读取【当前激活的模型】ID
        示例：app_settings.active_model
        """
        app_settings = self._raw_configs.get("app_settings", {})
        return app_settings.get("active_model", "dashscope")

    def get_config(self, config_id: str) -> LLMConfig:
        """
        根据模型 ID 获取完整配置
        缺失任何必要项 → 友好提示并退出
        """
        # 模型不存在
        if config_id not in self._raw_configs:
            print(f"\n❌ 错误：未找到模型配置「{config_id}」")
            print("请检查 models.yaml 中的配置名称。\n")
            sys.exit(1)

        cfg_dict = self._raw_configs[config_id]
        env_key_name = cfg_dict.get("api_key_env")

        # 未配置环境变量名
        if not env_key_name:
            print(f"\n❌ 错误：模型「{config_id}」未配置 api_key_env")
            print("请在 YAML 中添加：api_key_env: 你的环境变量名\n")
            sys.exit(1)

        # 未获取到 API Key
        actual_api_key = os.getenv(env_key_name)
        if not actual_api_key:
            print(f"\n❌ 错误：模型「{config_id}」缺少 API Key")
            print(f"请配置环境变量：{env_key_name}")
            print("可在 .env 文件或系统环境变量中配置。\n")
            sys.exit(1)

        # 一切正常，返回配置
        return LLMConfig(
            provider=cfg_dict.get("provider", "unknown"),
            model_name=cfg_dict.get("model_name", ""),
            api_key=actual_api_key,
            base_url=cfg_dict.get("base_url"),
            temperature=cfg_dict.get("temperature", 0.0),
        )


# 全局单例
config_manager = ConfigManager()