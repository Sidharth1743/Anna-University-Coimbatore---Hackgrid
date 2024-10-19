## College Name - Team Name
Anna university Regional Campus Coimbatore - Hackgrid

## Problem Statement
As global investors increasingly prioritize sustainability and responsible investing, access to
reliable, real-time data has become crucial in making informed financial decisions. With the
growing importance of environmental, social, and governance (ESG) factors, alongside the
rapid changes in market sentiment driven by social media and news platforms, there is a need
for an innovative tool that consolidates these insights into a single, easy-to-use platform. The
key requirements are:
• A user-friendly application that delivers real-time sustainability and market sentiment
data from credible sources, helping investors stay informed about the equities they
follow.
• Enhanced decision-making capabilities for investors, made possible by an interactive
dashboard that integrates diverse data analytics, giving them a holistic view of stock
performance.
• Scalability for future enhancements, ensuring that the application can easily integrate
additional data sources, features, or asset classes as investment needs evolve.


# Equity Analysis Web Application

### Overview

The Equity Analysis Application aims to provide investors with a comprehensive tool for real-time equity analysis, focusing on critical financial and sustainability metrics. This application will serve as a vital resource for investors seeking actionable insights to enhance their decision-making processes regarding specific equities.
### Key Features
## 1. Sustainability Scores:
The application will integrate Environmental, Social, and Governance (ESG) scores, which are essential for evaluating a company's sustainability practices. These scores will be sourced from reputable platforms like LSEG and MSCI, which provide transparent assessments based on various ESG criteria such as emissions, human rights, and corporate governance practices135.
## 2. Market Sentiment Indicators:
Users will have access to market sentiment indicators like Beta (a measure of volatility relative to the market) and Relative Strength Index (RSI), which helps in identifying overbought or oversold conditions in the stock market. These indicators will assist investors in gauging market trends and making informed trading decisions.
## 3. Financial Metrics:
The application will also aggregate key financial indicators such as:
Price-to-Earnings (P/E) Ratio: A valuation ratio calculated by dividing the current share price by its earnings per share.
Price-to-Book (P/B) Ratio: This ratio compares a company's market value to its book value, providing insights into valuation relative to its assets.


## Features

- **Company ESG Score**: Retrieves ESG scores from WikiRate.
- **Stock Data**: Fetches real-time stock data from Yahoo Finance.
- **Sentiment Analysis**: Analyzes sentiment from news articles and Reddit posts related to companies.
- **Visualization**: Displays company stock performance trends through interactive charts.
- **User Authentication**: Allows users to register and log in to track companies.

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript, Chart.js,React.js
- **APIs**: WikiRate API, News API, Reddit API (via PRAW), Yahoo Finance API (via `yfinance`), VADER Sentiment Analysis

### Instructions on running your project
## Installation

## Prerequisites

- Python 3.8+
- MongoDB
- pip (Python package manager)

### Clone the Repository
git clone https://github.com/your-repo/esg-stock-scoring.git
cd esg-stock-scoring

## Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate

## Install Dependencies
pip install -r requirements.txt
Flask==2.0.2
Flask-PyMongo==2.3.0
Flask-Cors==3.0.10
requests==2.26.0
yfinance==0.1.67
praw==7.4.0
vaderSentiment==3.3.2
python-dotenv==0.19.2

### API Usage
The application integrates with several APIs to gather the necessary data. Below is a list of the APIs and how they are used:

## 1. WikiRate API
Purpose: Fetch ESG data for companies.
Endpoint: https://wikirate.org/{company_name}+Answer.json
Authentication: API key .

## 2. Reddit API (PRAW)
Purpose: Fetch Reddit posts for sentiment analysis.
Endpoint: Reddit's search within 'investing' subreddit.
Authentication: OAuth credentials (client ID, client secret, and user agent).

## 3. News API
Purpose: Retrieve news articles related to ESG and perform sentiment analysis on the headlines.
Endpoint: https://newsapi.org/v2/everything
Authentication: API key 

## 4.YFinance API Usage
The project makes use of the yfinance API to fetch stock data for analysis. yfinance is a Python library that wraps the Yahoo Finance API, allowing easy access to historical market data, stock prices, and financial indicators.

Features of yfinance Used in the Project:
Stock Price Retrieval: Fetch the latest and historical stock price data, including opening, closing, high, and low prices.
Stock Information: Retrieve key financial metrics such as the beta, price-to-earnings (P/E) ratio, and price-to-book (P/B) ratio.
Relative Strength Index (RSI) Calculation: The project calculates the RSI based on the fetched historical data.

## 5. VADER Sentiment Analysis (via vaderSentiment library)
Purpose: Analyze sentiment from text data.
Library: vaderSentiment (no external API requests).

### Running the Application
Steps to Create a React Application
# 1. Install Create React App
Create React App is a command-line tool that sets up a new React project with a sensible default configuration. You can install it globally by running the following command:

npm install -g create-react-app

# 2. Create a New React Application
Once you have create-react-app installed, you can create a new React application. Open your terminal and run:

npx create-react-app my-app

Replace my-app with the desired name for your application. This command will create a new folder named my-app and set up a new React project inside it.

# 3. Navigate to Your Application Directory
After creating your app, navigate into your project directory:

cd my-app

# 4. Start the Development Server
To run your application and see it in action, use the following command:

npm start

This command starts the development server and opens your new React app in your default web browser, usually at http://localhost:3000.


Register/Login: Users can create an account or log in to access company tracking.
Company Lookup: Search for companies by name to retrieve ESG scores, stock data, and sentiment analysis.
Stock Visualization: View historical stock prices for the selected company.
Sentiment Analysis: Get sentiment analysis for news articles and Reddit posts related to the company.


## Architecture:

equity-analysis-app/
├── backend/
│   ├── app.py                       # Main Flask application
│   ├── models.py                    # Database models (User, StockData)
│   ├── requirements.txt              # Python dependencies
│   ├── templates/                    # (Optional) HTML templates if needed
│   └── static/                       # (Optional) Static files (CSS, JS) if needed
├── frontend/
│   ├── public/
│   │   ├── index.html                # Main HTML file
│   │   └── favicon.ico               # App favicon
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard.js           # Dashboard component
│   │   │   ├── Login.js               # Login component
│   │   │   ├── Register.js            # Registration component
│   │   ├── App.js                     # Main App component
│   │   ├── App.css                   # CSS styles for the React app
│   │   ├── Dashboard.css             # CSS styles for the Dashboard component
│   │   ├── index.js                   # Entry point for React
│   │   └── api.js                    # API service functions for Axios
│   ├── package.json                   # React app dependencies and scripts
│   └── .env                          # Environment variables (for React app)
└── README.md                        # Project documentation





## References
https://www.reddit.com/dev/api/

https://newsapi.org/docs

https://wikirate.org/use_the_API

https://pypi.org/project/yfinance/

