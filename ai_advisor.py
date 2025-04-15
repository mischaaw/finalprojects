import openai
import os

# Set your OpenAI API key here or via environment variable
openai.api_key = os.getenv("AIzaSyAlTFdSSiqr0TOoNLLDmRcKbJV1xZ4TCQU")

def analyze_strategy(results):
    prompt = f"""
    You are an investing advisor. Given the following portfolio:
    - Ticker: {results['ticker']}
    - Strategy: {results['strategy']}
    - Total Invested: ${results['total_invested']}
    - Final Value: ${results['portfolio_value']}
    - Total Gain: ${results['gain']}

    Provide a brief natural language analysis and suggest one way to improve the strategy.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"AI analysis unavailable: {str(e)}"
