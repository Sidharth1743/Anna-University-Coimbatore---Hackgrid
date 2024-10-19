import React, { useEffect, useState, useCallback } from 'react';
import axios from 'axios';
import '../CSS/Dashboard.css'; // Import the CSS file

const Dashboard = () => {
  const [charts, setCharts] = useState({
    rsi_plot: '',
    beta_plot: '',
    pe_plot: '',
    pb_plot: ''
  });

  const [ticker, setTicker] = useState('AAPL'); // Default ticker is AAPL
  const [companyName, setCompanyName] = useState('AAPL'); // Set default value for dropdown
  const [esgScore, setEsgScore] = useState(null);
  const [error, setError] = useState('');

  // Using useCallback to memoize fetchStockData
  const fetchStockData = useCallback(async () => {
    try {
      const response = await axios.post('http://127.0.0.1:5000/get_stock_data', { ticker });
      setCharts(response.data);
    } catch (error) {
      console.error('Error fetching stock data:', error);
    }
  }, [ticker]); // Include ticker as a dependency

  // Fetch stock data when the component is first rendered
  useEffect(() => {
    fetchStockData();
  }, [fetchStockData]); // Safe to include fetchStockData here

  // Handle ESG score calculation
  const handleCalculateEsg = useCallback(async () => {
    setError(''); // Reset error state

    try {
      const response = await axios.post('http://127.0.0.1:5000/calculate_esg_score', {
        company_name: companyName,
        ticker,
      });
      setEsgScore(response.data); // Set the ESG score from the response
    } catch (err) {
      setError('Error fetching ESG score. Please try again.'); // Handle any errors
      console.error(err);
    }
  }, [companyName, ticker]); // Include companyName and ticker as dependencies

  // Automatically calculate ESG score when companyName changes
  useEffect(() => {
    handleCalculateEsg(); // Call ESG calculation when companyName changes
  }, [handleCalculateEsg]); // Trigger ESG calculation on handleCalculateEsg change

  // Handle form submission for fetching stock data
  const handleSubmit = (event) => {
    event.preventDefault();
    fetchStockData(); // Fetch new data based on the inputted ticker
  };

  return (
    <div className="dashboard">
      <h2>Stock Market Analysis Dashboard</h2>
      
      {/* Ticker Input Form */}
      <form onSubmit={handleSubmit} className="form">
        <label>
          Enter Ticker Symbol:
          <select
            value={ticker}
            onChange={(e) => setTicker(e.target.value)} // Update ticker state
            className="input"
          >
            {/* Dropdown with ticker options */}
            <option value="AAPL">AAPL</option>
            <option value="MSFT">MSFT</option>
            <option value="AMZN">AMZN</option>
            <option value="TSLA">TSLA</option>
            <option value="GOOGL">GOOGL</option>
            <option value="GOOG">GOOG</option>
            <option value="META">META</option>
            <option value="NVDA">NVDA</option>
            <option value="BRK-A">BRK-A</option>
            <option value="BRK-B">BRK-B</option>
            <option value="JPM">JPM</option>
            <option value="JNJ">JNJ</option>
            <option value="V">V</option>
            <option value="WMT">WMT</option>
            <option value="PG">PG</option>
            <option value="UNH">UNH</option>
            <option value="HD">HD</option>
            <option value="DIS">DIS</option>
            <option value="NFLX">NFLX</option>
            <option value="XOM">XOM</option>
          </select>
        </label>
        <button type="submit" className="button">Fetch Data</button>
      </form>

      <div className="charts-container">
        {/* RSI Chart */}
        <div className="chart-card rsi-chart">
          <div className="chart-header">
            <h3>RSI (Relative Strength Index)</h3>
          </div>
          {charts.rsi_plot ? (
            <img src={`data:image/png;base64,${charts.rsi_plot}`} alt="RSI Chart" className="chart-image" />
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>

      <div className="charts-row">
        {/* Beta Chart */}
        <div className="chart-card">
          <h3>Beta</h3>
          {charts.beta_plot ? (
            <img src={`data:image/png;base64,${charts.beta_plot}`} alt="Beta Chart" className="chart-image" />
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* P/E Ratios Chart */}
        <div className="chart-card">
          <h3>P/E Ratios</h3>
          {charts.pe_plot ? (
            <img src={`data:image/png;base64,${charts.pe_plot}`} alt="P/E Ratios Chart" className="chart-image" />
          ) : (
            <p>Loading...</p>
          )}
        </div>

        {/* Price to Book Ratio Chart */}
        <div className="chart-card">
          <h3>Price to Book Ratio</h3>
          {charts.pb_plot ? (
            <img src={`data:image/png;base64,${charts.pb_plot}`} alt="Price to Book Chart" className="chart-image" />
          ) : (
            <p>Loading...</p>
          )}
        </div>
      </div>

      {/* ESG Score Calculation Form */}
      <form className="esf-form">
        <label>
          Select Company for ESG Score:
          <select
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
            className="input"
          >
            <option value="AAPL">AAPL</option>
            <option value="MSFT">MSFT</option>
            <option value="AMZN">AMZN</option>
            <option value="TSLA">TSLA</option>
            <option value="GOOGL">GOOGL</option>
            <option value="GOOG">GOOG</option>
            <option value="META">META</option>
            <option value="NVDA">NVDA</option>
            <option value="BRK-A">BRK-A</option>
            <option value="BRK-B">BRK-B</option>
            <option value="JPM">JPM</option>
            <option value="JNJ">JNJ</option>
            <option value="V">V</option>
            <option value="WMT">WMT</option>
            <option value="PG">PG</option>
            <option value="UNH">UNH</option>
            <option value="HD">HD</option>
            <option value="DIS">DIS</option>
            <option value="NFLX">NFLX</option>
            <option value="XOM">XOM</option>
          </select>
        </label>
      </form>

      {/* Display ESG Score */}
      {esgScore && (
        <div className='esgg'>
          <h2>ESG Score for {companyName}:</h2>
          <p>Total Score: {esgScore.total_score}</p>
          <p>Environmental Score: {esgScore.environmental_score}</p>
          <p>Social Score: {esgScore.social_score}</p>
          <p>Governance Score: {esgScore.governance_score}</p>
          <p>Timestamp: {esgScore.timestamp}</p>
        </div>
      )}
      {error && <p>{error}</p>}
    </div>
  );
};

export default Dashboard;
