from agents.agent import agent  # 이게 AgentExecutor라고 가정

if __name__ == "__main__":
    while True:
        user_input = input("질문: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # streaming
        for event in agent.stream({"input": user_input}):
            # tool 호출
            if "actions" in event:
                for action in event["actions"]:
                    print(f"[tool] {action.tool}({action.tool_input})")

            # 최종 답변
            if "outputs" in event:
                print("답변:", event["outputs"]["output"])
