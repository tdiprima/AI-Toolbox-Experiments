import pandas as pd
import matplotlib.pyplot as plt
from pandasai import Agent
from pandasai.llm.openai import OpenAI
import os

# 1. Load CSV with pandas
df = pd.read_csv('sales_data.csv')

# 2. Set up OpenAI LLM for PandasAI
llm = OpenAI(api_token=os.getenv("OPENAI_API_KEY"))

# 3. Create PandasAI agent instance
agent = Agent(df, config={"llm": llm})

# 4. Use natural language query to find product with highest seasonal variance
query = "Which product has the highest seasonal variance in sales? Show the sales trend for that product."
response = agent.chat(query)

# 5. Optionally, print the result
print(response)

# 6. Visualize: Let's plot the sales trend for the product with highest seasonal variance

# First, let's find the product with the highest sales variance by month
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month

# Calculate variance per product
variance = df.groupby('product').apply(lambda x: x.groupby('month')['sales'].sum().var())
top_product = variance.idxmax()
print(f"Product with highest seasonal variance: {top_product}")

# Plot sales trend for that product
product_data = df[df['product'] == top_product].groupby('month')['sales'].sum()
plt.figure(figsize=(8,5))
plt.plot(product_data.index, product_data.values, marker='o')
plt.title(f'Sales Trend for {top_product}')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.xticks(product_data.index)
plt.grid(True)
plt.show()
