from agents.basic_agent import agent

if __name__ == "__main__":
    while True:
        user_input = input("질문: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # streaming
        for chunk in agent.stream(  
            {"messages": [{"role": "user", "content": user_input}]},
            stream_mode="values",
        ):
            latest_message = chunk["messages"][-1]
            if latest_message.content:
                print(f"Agent: {latest_message.content}")
            elif latest_message.tool_calls:
                print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")
