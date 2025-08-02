"""
Demonstrates basic AutoGen agent setup with assistant and user proxy
Just says "Hello World"; no need to run.
"""
import os
import autogen


def main():
    print("Hello World - AutoGen Example")
    
    config_list = [
        {
            "model": "gpt-3.5-turbo",
            "api_key": os.getenv("OPENAI_API_KEY")
        }
    ]
    
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={"config_list": config_list}
    )
    
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=1
    )
    
    user_proxy.initiate_chat(
        assistant,
        message="Say hello world!"
    )


if __name__ == "__main__":
    main()
