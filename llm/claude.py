from langchain_anthropic import ChatAnthropic

#
#  Return Claude Model with Provided Conditions
#
def get_claude_llm(model_name : str = "claude-haiku-4-5", temperature : float = 0.7, streaming : bool = True, timeout : int = 60):
    """
    Return a Claude Model with provided conditions.

    Args:
        model_name: The name of the Claude model to use. Defaults to "claude-haiku-4-5".
        temperature: The temperature setting for the model. Must be between 0 and 1. Defaults to 0.7.
        streaming: Whether to enable streaming responses. Defaults to True.
        timeout: The timeout in seconds for API requests. Defaults to 60.

    Returns:
        ChatAnthropic: An instance of the Anthropic Claude chat model.

    Raises:
        ValueError: If temperature is not between 0 and 1.
    """

    if temperature < 0 or temperature > 1:
        raise ValueError("Temperature must be between 0 and 1")

    return ChatAnthropic(
        model_name = model_name,
        temperature = temperature, 
        stop = None, 
        streaming = streaming,
        timeout = timeout
    )