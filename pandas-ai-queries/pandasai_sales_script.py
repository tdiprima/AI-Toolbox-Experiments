#!/usr/bin/env python3
"""
PandasAI Sales Data Analysis Script
Loads CSV sales data and uses natural language to find products with highest seasonal variance
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandasai import Agent
from pandasai.llm import OpenAI
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configuration
OPENAI_API_KEY = "your-openai-api-key-here"  # Replace with your actual API key
CSV_FILE_PATH = "sales_data.csv"  # Replace with your CSV file path

def create_sample_data():
    """Create sample sales data if CSV doesn't exist"""
    np.random.seed(42)
    
    # Generate date range
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2024, 12, 31)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    products = ['Laptop', 'Phone', 'Tablet', 'Headphones', 'Watch', 'Camera']
    
    data = []
    for date in date_range:
        for product in products:
            # Add seasonal patterns
            month = date.month
            seasonal_factor = 1.0
            
            if product in ['Laptop', 'Tablet']:  # Back-to-school/holiday boost
                seasonal_factor = 1.5 if month in [8, 9, 11, 12] else 0.8
            elif product == 'Phone':  # Spring/fall releases
                seasonal_factor = 1.3 if month in [3, 4, 9, 10] else 0.9
            elif product == 'Watch':  # Holiday/fitness season
                seasonal_factor = 1.4 if month in [1, 11, 12] else 0.7
            elif product == 'Camera':  # Summer/holiday travel
                seasonal_factor = 1.6 if month in [6, 7, 8, 12] else 0.6
            
            base_sales = np.random.normal(100, 20)
            sales = max(0, base_sales * seasonal_factor + np.random.normal(0, 10))
            
            data.append({
                'date': date,
                'product': product,
                'sales': round(sales, 2),
                'month': month,
                'quarter': f"Q{(month-1)//3 + 1}",
                'season': 'Spring' if month in [3,4,5] else 
                         'Summer' if month in [6,7,8] else 
                         'Fall' if month in [9,10,11] else 'Winter'
            })
    
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE_PATH, index=False)
    print(f"Sample data created and saved to {CSV_FILE_PATH}")
    return df

def load_data():
    """Load sales data from CSV"""
    try:
        df = pd.read_csv(CSV_FILE_PATH)
        print(f"Loaded data from {CSV_FILE_PATH}")
        print(f"Data shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        return df
    except FileNotFoundError:
        print(f"CSV file {CSV_FILE_PATH} not found. Creating sample data...")
        return create_sample_data()

def setup_pandasai(df):
    """Initialize PandasAI with OpenAI integration"""
    # Set up OpenAI API key
    os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
    
    # Initialize the LLM
    llm = OpenAI(api_token=OPENAI_API_KEY)
    
    # Create PandasAI agent
    agent = Agent(df, config={"llm": llm, "verbose": True})
    
    return agent

def calculate_seasonal_variance_manually(df):
    """Calculate seasonal variance manually as backup/verification"""
    # Ensure date column is datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.month
    
    # Group by product and season/month to calculate variance
    seasonal_stats = df.groupby(['product', 'season'])['sales'].agg(['mean', 'std']).reset_index()
    
    # Calculate coefficient of variation (std/mean) for each product across seasons
    product_variance = []
    for product in df['product'].unique():
        product_data = seasonal_stats[seasonal_stats['product'] == product]
        seasonal_means = product_data['mean'].values
        
        # Calculate variance across seasonal means
        variance = np.var(seasonal_means)
        cv = np.std(seasonal_means) / np.mean(seasonal_means) if np.mean(seasonal_means) > 0 else 0
        
        product_variance.append({
            'product': product,
            'seasonal_variance': variance,
            'coefficient_of_variation': cv,
            'seasonal_means': seasonal_means
        })
    
    # Sort by coefficient of variation (relative variance)
    product_variance.sort(key=lambda x: x['coefficient_of_variation'], reverse=True)
    
    return product_variance

def visualize_results(df, variance_results):
    """Create visualizations for seasonal variance analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    fig.suptitle('Sales Data Seasonal Variance Analysis', fontsize=16, fontweight='bold')
    
    # 1. Seasonal sales by product (box plot)
    ax1 = axes[0, 0]
    sns.boxplot(data=df, x='season', y='sales', hue='product', ax=ax1)
    ax1.set_title('Sales Distribution by Season and Product')
    ax1.tick_params(axis='x', rotation=45)
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # 2. Variance ranking
    ax2 = axes[0, 1]
    products = [item['product'] for item in variance_results]
    cv_values = [item['coefficient_of_variation'] for item in variance_results]
    
    bars = ax2.bar(products, cv_values, color='skyblue', edgecolor='navy', alpha=0.7)
    ax2.set_title('Seasonal Variance by Product\n(Coefficient of Variation)')
    ax2.set_ylabel('Coefficient of Variation')
    ax2.tick_params(axis='x', rotation=45)
    
    # Highlight the highest variance product
    bars[0].set_color('orange')
    bars[0].set_edgecolor('red')
    
    # 3. Time series for top variance product
    ax3 = axes[1, 0]
    top_product = variance_results[0]['product']
    product_data = df[df['product'] == top_product].copy()
    product_data['date'] = pd.to_datetime(product_data['date'])
    product_data = product_data.sort_values('date')
    
    ax3.plot(product_data['date'], product_data['sales'], alpha=0.7, linewidth=1)
    ax3.set_title(f'Sales Over Time: {top_product}\n(Highest Seasonal Variance)')
    ax3.set_ylabel('Sales')
    ax3.tick_params(axis='x', rotation=45)
    
    # 4. Seasonal means comparison
    ax4 = axes[1, 1]
    seasonal_means = df.groupby(['product', 'season'])['sales'].mean().unstack()
    seasonal_means.plot(kind='bar', ax=ax4, width=0.8)
    ax4.set_title('Average Sales by Season and Product')
    ax4.set_ylabel('Average Sales')
    ax4.tick_params(axis='x', rotation=45)
    ax4.legend(title='Season', bbox_to_anchor=(1.05, 1), loc='upper left')
    
    plt.tight_layout()
    plt.show()
    
    return fig

def main():
    """Main execution function"""
    print("=== PandasAI Sales Data Analysis ===\n")
    
    # Load data
    df = load_data()
    print(f"\nFirst few rows of data:")
    print(df.head())
    
    # Calculate variance manually (as backup)
    print("\n=== Manual Seasonal Variance Calculation ===")
    variance_results = calculate_seasonal_variance_manually(df)
    
    print("\nProducts ranked by seasonal variance (Coefficient of Variation):")
    for i, result in enumerate(variance_results, 1):
        print(f"{i}. {result['product']}: CV = {result['coefficient_of_variation']:.3f}")
    
    highest_variance_product = variance_results[0]['product']
    print(f"\n🏆 Product with highest seasonal variance: {highest_variance_product}")
    
    # Set up PandasAI
    print("\n=== Setting up PandasAI ===")
    try:
        agent = setup_pandasai(df)
        
        # Natural language queries
        queries = [
            "Which product has the highest seasonal variance?",
            "Show me the seasonal sales patterns for each product",
            "What is the coefficient of variation for sales across seasons by product?",
            "Which product shows the most inconsistent sales across different seasons?"
        ]
        
        print("\n=== PandasAI Natural Language Queries ===")
        for i, query in enumerate(queries, 1):
            print(f"\n--- Query {i}: {query} ---")
            try:
                response = agent.chat(query)
                print(f"Response: {response}")
            except Exception as e:
                print(f"Error with query: {e}")
                print("Falling back to manual calculation...")
                
    except Exception as e:
        print(f"PandasAI setup failed: {e}")
        print("Make sure you have set your OpenAI API key correctly.")
        print("Proceeding with manual analysis only...")
    
    # Create visualizations
    print("\n=== Creating Visualizations ===")
    fig = visualize_results(df, variance_results)
    
    # Summary
    print("\n=== Summary ===")
    print(f"Analysis complete! The product with the highest seasonal variance is: {highest_variance_product}")
    print(f"Coefficient of Variation: {variance_results[0]['coefficient_of_variation']:.3f}")
    print("\nThis indicates that this product's sales fluctuate the most between seasons,")
    print("making it important for inventory planning and seasonal marketing strategies.")

if __name__ == "__main__":
    # Required packages check
    required_packages = ['pandas', 'numpy', 'matplotlib', 'seaborn', 'pandasai']
    
    print("Checking required packages...")
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        print("Install them with: pip install " + " ".join(missing_packages))
    else:
        main()
