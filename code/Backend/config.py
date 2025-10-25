# backend/config.py

import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/equity")  # Change to your MongoDB URI
