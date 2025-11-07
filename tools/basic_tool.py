from langchain.tools import tool

@tool
def echo_tool(query: str) -> str:
    """**반드시 호출**\n입력한 문장을 그대로 돌려주는 테스트용 툴"""
    print("hello, echo_tool!")
    return f"Echo: {query}"