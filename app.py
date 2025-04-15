from flask import Flask, request, jsonify
import openai
import yfinance as yf
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
openai.api_key = os.getenv("AIzaSyAlTFdSSiqr0TOoNLLDmRcKbJV1xZ4TCQU")

app = Flask(__name__)

# Route to display home page
@app.route('/')
def home():
    return "Auto-Investing Strategy Backtester with AI Advisor is up and running!"

# Route to handle strategy backtest
@app.route('/backtest', methods=['POST'])
def backtest():
    # Get form data
    ticker = request.json.get('ticker')
    strategy = request.json.get('strategy')  # For simplicity, not implementing the full strategy logic
    monthly_investment = request.json.get('monthly_investment', 1000)
    start_year = request.json.get('start_year', 2015)

    # Fetch data from Yahoo Finance
    data = yf.download(ticker, start=f'{start_year}-01-01', end='2024-01-01', interval="1mo")
    
    # For now, let’s simulate simple calculations (no actual strategy logic implemented yet)
    total_invested = monthly_investment * len(data)
    portfolio_value = total_invested * 1.2  # Simulate 20% growth
    gain = portfolio_value - total_invested

    # Use OpenAI to generate an analysis
    prompt = f"Analyze this investment strategy:\nTicker: {ticker}\nTotal Invested: ${total_invested}\nPortfolio Value: ${portfolio_value}\nGain: ${gain}\n"
    
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=200
        )
        ai_analysis = response.choices[0].text.strip()
    except Exception as e:
        ai_analysis = f"Error generating analysis: {str(e)}"
    
    return jsonify({
        "total_invested": total_invested,
        "portfolio_value": portfolio_value,
        "gain": gain,
        "ai_analysis": ai_analysis
    })

if __name__ == "__main__":
    app.run(debug=True)
