from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import matplotlib.pyplot as plt
import requests
import praw
import yfinance as yf
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import io
import base64
import bcrypt
from config import Config
from models import mongo, create_user, find_user

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # This will allow cross-origin requests
mongo.init_app(app)  # Initialize MongoDB

# Initialize Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# Reddit API initialization
reddit = praw.Reddit(
    client_id='vZAg9lHB2nvxY0wR_LbIwg',
    client_secret='owDrVmQdzYYQfyP4SHTjKFtaLKMe1w',
    user_agent='myApp:v1.0 (by /u/Sidhu1748)'
)

# ESG Scorer class
class ESGScorer:
    def __init__(self):
        self.keywords = {
            'environmental': {
                'carbon emissions': 5,
                'renewable energy': 4,
                'waste management': 3,
                'climate change': 5,
                'biodiversity': 4,
                'water conservation': 3,
            },
            'social': {
                'employee satisfaction': 4,
                'workplace safety': 5,
                'human rights': 5,
                'diversity inclusion': 4,
                'community engagement': 3,
                'labor practices': 4,
            },
            'governance': {
                'board diversity': 4,
                'business ethics': 5,
                'corruption': 5,
                'transparency': 4,
                'executive compensation': 3,
                'shareholder rights': 4,
            }
        }

    @lru_cache(maxsize=100)
    def fetch_wikirate_data(self, company_name: str) -> Dict:
        """Fetch data from WikiRate API with caching"""
        headers = {'Authorization': 'sN1yYSIMfAEwQ97LQqyZ5gtt'}
        response = requests.get(f'https://wikirate.org/{company_name}+Answer.json', headers=headers)
        if response.status_code == 200:
            data = response.json()
            print(f"WikiRate data for {company_name}: {data}")
            return data
        else:
            print(f"Error fetching WikiRate data for {company_name}: {response.status_code}")
            return {}

    def fetch_reddit_sentiment(self, company_name: str) -> float:
        """Fetch Reddit posts and calculate sentiment"""
        subreddit = reddit.subreddit('investing')
        posts = subreddit.search(company_name, limit=100, time_filter='month')
        sentiment_scores = [analyzer.polarity_scores(post.title + ' ' + post.selftext)['compound'] for post in posts]
        return np.mean(sentiment_scores) if sentiment_scores else 0

    def fetch_news_sentiment(self, company_name: str) -> float:
        """Fetch news articles and calculate sentiment"""
        base_url = "https://newsapi.org/v2/everything"
        params = {
            'q': f"{company_name} AND (ESG OR sustainability OR environmental OR social OR governance)",
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': '389668f989f14dd3a72f1eae8f3a3495'
        }
        response = requests.get(base_url, params=params)
        articles = response.json().get('articles', [])
        sentiment_scores = [analyzer.polarity_scores(article.get('title', ''))['compound'] for article in articles if article.get('title')]
        return np.mean(sentiment_scores) if sentiment_scores else 0

    def calculate_keyword_score(self, text: str, category: str) -> float:
        """Calculate score based on keyword presence and importance"""
        score = 0
        for keyword, importance in self.keywords[category].items():
            if keyword in text.lower():
                score += importance
        return min(score, 100)  # Cap the score at 100

    def calculate_esg_score(self, company_name: str, ticker: str) -> Dict:
        """Calculate ESG score for a company and scale it to a 0-100 range"""
        wikirate_data = self.fetch_wikirate_data(company_name)
        reddit_sentiment = self.fetch_reddit_sentiment(company_name)
        news_sentiment = self.fetch_news_sentiment(company_name)

        def scale_sentiment(sentiment: float) -> float:
            return round((sentiment + 1) * 50)  # Converts [-1, 1] to [0, 100]

        scaled_reddit_sentiment = scale_sentiment(reddit_sentiment)
        scaled_news_sentiment = scale_sentiment(news_sentiment)

        # Calculate scores based on keywords in WikiRate data
        environmental_score = self.calculate_keyword_score(str(wikirate_data), 'environmental')
        social_score = self.calculate_keyword_score(str(wikirate_data), 'social')
        governance_score = self.calculate_keyword_score(str(wikirate_data), 'governance')

        # Incorporate sentiment scores
        environmental_score = (environmental_score + scaled_news_sentiment) / 2
        social_score = (social_score + scaled_reddit_sentiment) / 2
        governance_score = (governance_score + scaled_reddit_sentiment) / 2

        # Calculate total ESG score
        total_score = (environmental_score + social_score + governance_score) / 3

        return {
            'timestamp': datetime.now().isoformat(),
            'ticker': ticker,
            'total_score': round(total_score, 2),
            'environmental_score': round(environmental_score, 2),
            'social_score': round(social_score, 2),
            'governance_score': round(governance_score, 2),
        }

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to register a user
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        preferred_stock = data.get("preferredStock")

        # Validate request data
        if not username or not password or not preferred_stock:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the user already exists
        if find_user(username):
            return jsonify({"error": "User already exists"}), 400

        # Create the new user
        user = create_user(username, password, preferred_stock)
        return jsonify({"message": "User registered successfully", "user": user}), 201

    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route to log in a user
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # Validate request data
        if not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Find the user in the database
        user = find_user(username)

        # Check if the user exists
        if not user:
            return jsonify({"error": "No user exists with this username. Please register."}), 404

        # Check if the password matches
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Incorrect password. Please try again."}), 401

        # Successful login
        return jsonify({"message": "Login successful", "username": username}), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route to get stock data
@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        ticker = request.json['ticker']  # Get the ticker from the request JSON
        
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)

        # Fetch historical data for the last month
        hist = stock.history(period='1mo', interval='1d')

        # Calculate daily price change
        hist['PriceChange'] = hist['Close'].diff()

        # Separate gains and losses
        hist['Gain'] = hist['PriceChange'].apply(lambda x: x if x > 0 else 0)
        hist['Loss'] = hist['PriceChange'].apply(lambda x: -x if x < 0 else 0)

        # Calculate average gain and loss over the past 14 days
        hist['AvgGain'] = hist['Gain'].rolling(window=14).mean()
        hist['AvgLoss'] = hist['Loss'].rolling(window=14).mean()

        # Calculate the RS and RSI
        hist['RS'] = hist['AvgGain'] / hist['AvgLoss']
        hist['RSI'] = 100 - (100 / (1 + hist['RS']))

        # Get stock info
        info = stock.info
        beta = info.get('beta', 0)
        trailing_pe = info.get('trailingPE', 0)
        forward_pe = info.get('forwardPE', 0)
        price_to_book = info.get('priceToBook', 0)

        # Convert to float if needed
        beta = float(beta) if isinstance(beta, (int, float)) else 0
        trailing_pe = float(trailing_pe) if isinstance(trailing_pe, (int, float)) else 0
        forward_pe = float(forward_pe) if isinstance(forward_pe, (int, float)) else 0
        price_to_book = float(price_to_book) if isinstance(price_to_book, (int, float)) else 0

        # Generate plots
        rsi_plot = create_rsi_plot(hist, ticker)
        beta_plot = create_beta_plot(beta)
        pe_plot = create_pe_plot(trailing_pe, forward_pe)
        pb_plot = create_pb_plot(price_to_book)

        # Return the plots as JSON
        return jsonify({
            'rsi_plot': rsi_plot,
            'beta_plot': beta_plot,
            'pe_plot': pe_plot,
            'pb_plot': pb_plot
        })

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return jsonify({"error": str(e)}), 500

# Function to create RSI plot
def create_rsi_plot(hist, ticker):
    img_rsi = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title(f'Relative Strength Index (RSI) for {ticker}')
    plt.legend()
    plt.savefig(img_rsi, format='png')
    plt.close()
    img_rsi.seek(0)
    return base64.b64encode(img_rsi.getvalue()).decode()

# Function to create Beta plot
def create_beta_plot(beta):
    img_beta = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.bar('Beta', beta, color='blue')
    plt.title('Beta')
    plt.ylim(0, max(beta + 0.5, 2))
    plt.savefig(img_beta, format='png')
    plt.close()
    img_beta.seek(0)
    return base64.b64encode(img_beta.getvalue()).decode()

# Function to create P/E ratios plot
def create_pe_plot(trailing_pe, forward_pe):
    img_pe = io.BytesIO()
    pe_ratios = {'Trailing P/E': trailing_pe, 'Forward P/E': forward_pe}
    plt.figure(figsize=(5, 5))
    plt.bar(pe_ratios.keys(), pe_ratios.values(), color=['orange', 'cyan'])
    plt.title('P/E Ratios')
    plt.ylim(0, max(trailing_pe, forward_pe) + 10)
    plt.savefig(img_pe, format='png')
    plt.close()
    img_pe.seek(0)
    return base64.b64encode(img_pe.getvalue()).decode()

# Function to create P/B ratio plot
def create_pb_plot(price_to_book):
    img_pb = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.bar('P/B Ratio', price_to_book, color='green')
    plt.title('Price to Book (P/B) Ratio')
    plt.ylim(0, max(price_to_book + 10, 20))
    plt.savefig(img_pb, format='png')
    plt.close()
    img_pb.seek(0)
    return base64.b64encode(img_pb.getvalue()).decode()

# Function to create a user
def create_user(username, password, preferred_stock):
    try:
        # Hash the password before saving
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {"username": username, "password": hashed.decode('utf-8'), "preferred_stock": preferred_stock}
        mongo.db.users.insert_one(user)
        return {"username": username, "preferred_stock": preferred_stock}
    except Exception as e:
        print(f"Error creating user: {e}")
        raise
# Route to calculate ESG score
@app.route('/calculate_esg_score', methods=['POST'])
def calculate_esg():
    try:
        data = request.json
        company_name = data['company_name']
        ticker = data['ticker']

        esg_scorer = ESGScorer()
        esg_score = esg_scorer.calculate_esg_score(company_name, ticker)

        return jsonify(esg_score)

    except Exception as e:
        print(f"Error calculating ESG score: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == "__main__":
    app.run(debug=True)
