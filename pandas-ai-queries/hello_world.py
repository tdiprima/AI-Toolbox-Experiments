# PandasAI agent example with sample DataFrame queries
import pandas as pd
from pandasai import Agent


def main():
    print("Hello World - PandasAI Example")

    sample_data = {
        "name": ["Alice", "Bob", "Charlie", "Diana"],
        "age": [25, 30, 35, 28],
        "city": ["New York", "London", "Tokyo", "Paris"],
        "greeting": ["Hello!", "Hi there!", "Konnichiwa!", "Bonjour!"],
    }

    df = pd.DataFrame(sample_data)
    print("\nSample DataFrame:")
    print(df)

    try:
        agent = Agent(df)

        response = agent.chat("Show me the greetings from the data")
        print(f"\nPandasAI Response: {response}")

        response2 = agent.chat("What is the average age?")
        print(f"Average age query: {response2}")

    except Exception as e:
        print(f"\nNote: PandasAI requires API configuration: {e}")
        print("Manual analysis:")
        print(f"Greetings: {df['greeting'].tolist()}")
        print(f"Average age: {df['age'].mean()}")


if __name__ == "__main__":
    main()
