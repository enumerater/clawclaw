# clawclaw
基于 LangGraph 和 LangChain 复刻一下openclaw。

# 🚀 快速开始
1. 安装依赖
``` Bash
pip install langchain-openai langgraph python-dotenv pyyaml
```
2. 配置秘钥 (.env)
在项目根目录下创建 .env 文件，并填入你的 API Key：

```
# 阿里云百炼
DASHSCOPE_API_KEY=your_sk_here
```
3. 配置模型 (models.yaml)
在项目根目录下创建 models.yaml 文件，通过修改 active_model 字段实现模型切换：

``` YAML
app_settings:
  active_model: "dashscope"
 ```
4. 运行 Demo
```Bash
python main.py
```