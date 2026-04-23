from core.agent import ClawClawAgent
from Callback.token_counter import TokenCountCallback


def main():
    print("🤖 ClawClaw 核心已初始化 。输入 'quit' 退出。")

    agent = ClawClawAgent()
    token_counter = TokenCountCallback()

    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "q"]:
                print("再见！")
                break

            token_counter.reset()
            response = None

            # 流式输出
            for res in agent.chat(user_input, config={"callbacks": [token_counter]}):
                response = res

            # 打印结果 + Token
            print(f"Agent: {response}")
            usage = token_counter.get_usage()
            print(f"📊 Token | 输入:{usage['prompt']} | 输出:{usage['completion']} | 总计:{usage['total']}")

        except KeyboardInterrupt:
            print("\n再见！")
            break
        except Exception as e:
            print(f"\n❌ 系统异常: {e}")


if __name__ == "__main__":
    main()