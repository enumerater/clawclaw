import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def web_fetch(url: str) -> str:
    """
    当需要查阅最新文档、搜索报错信息或获取外部网页内容时，使用此工具。
    传入目标 URL，将返回提取后的纯文本网页内容。
    """
    print(f"\n[🌐 正在抓取网页]: {url}")
    try:
        # 伪装 User-Agent 防止被简单的反爬虫拦截
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # 如果返回 404 或 500 会抛出异常

        # 使用 BeautifulSoup 提取文本
        soup = BeautifulSoup(response.text, 'html.parser')

        # 移除 scripts 和 styles 标签，减少噪音
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text(separator='\n', strip=True)

        # 防止页面过大撑爆 Token
        if len(text) > 8000:
            return text[:8000] + "\n...[网页内容过长已截断，请尝试搜索更精确的页面]..."

        return text if text else "网页内容为空或无法解析纯文本。"

    except requests.exceptions.RequestException as e:
        return f"网络请求失败: {str(e)}"
    except Exception as e:
        return f"抓取网页发生未知错误: {str(e)}"