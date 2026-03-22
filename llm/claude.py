from langchain_anthropic import ChatAnthropic

#
#  Return Claude Model with Provided Conditions
#
def get_claude_llm(model_name = "claude-haiku-4-5", temperature = 0.7, streaming = True, timeout = 60):
    return ChatAnthropic(
    model_name = model_name,
    temperature = temperature, 
    stop = None, 
    streaming = streaming,
    timeout = timeout
    )