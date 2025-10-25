import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import '../CSS/Register.css';

const Register = () => {
  const [username, setUsername] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [preferredStock, setPreferredStock] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const stocks = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL', 'META'];

  const handleRegisterSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    if (newPassword !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (newPassword.length < 6) {
      setError('Password must be at least 6 characters long');
      return;
    }

    if (!preferredStock) {
      setError('Please select a preferred stock');
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password: newPassword, preferredStock }),
      });

      setLoading(false);

      if (response.ok) {
        alert('Registration successful');
        navigate('/login');
      } else {
        const data = await response.json();
        setError(data.error || 'Registration failed');
      }
    } catch (error) {
      setLoading(false);
      console.error('Error during registration:', error);
      setError('An error occurred during registration. Please try again later.');
    }
  };

  return (
    <div className="register-container">
      <div className="register-form">
        <h2>Register</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleRegisterSubmit}>
          <div className="form-group">
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              placeholder=" "
            />
            <label htmlFor="username">Username</label>
          </div>

          <div className="form-group">
            <input
              type="password"
              id="newPassword"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
              placeholder=" "
            />
            <label htmlFor="newPassword">New Password</label>
          </div>

          <div className="form-group">
            <input
              type="password"
              id="confirmPassword"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              placeholder=" "
            />
            <label htmlFor="confirmPassword">Confirm Password</label>
          </div>

          <div className="form-group">
            <select
              id="preferredStock"
              value={preferredStock}
              onChange={(e) => setPreferredStock(e.target.value)}
              required
            >
              <option value="" disabled>Select a stock</option>
              {stocks.map((stock, index) => (
                <option key={index} value={stock}>
                  {stock}
                </option>
              ))}
            </select>
            <label htmlFor="preferredStock">Select Preferred Stock</label>
          </div>

          <button type="submit" disabled={loading}>
            {loading ? 'Registering...' : 'Register'}
          </button>
        </form>
        <p>
          Already have an account? <Link to="/login">Login Here</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;