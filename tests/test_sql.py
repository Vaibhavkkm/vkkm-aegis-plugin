import os
import sys
import logging
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text

# Ensure we can import the mcp_server module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mcp_server import app

client = TestClient(app)

def setup_db():
    db_url = "sqlite:///test_portfolio.db"
    engine = create_engine(db_url)
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS portfolio"))
        conn.execute(text("""
            CREATE TABLE portfolio (
                id INTEGER PRIMARY KEY,
                name TEXT,
                weight REAL,
                mu REAL,
                sigma REAL
            )
        """))
        conn.execute(text("""
            INSERT INTO portfolio (name, weight, mu, sigma) VALUES
            ('AAPL', 0.4, 0.08, 0.15),
            ('MSFT', 0.4, 0.06, 0.12),
            ('GOOGL', 0.2, 0.07, 0.18)
        """))
    return db_url

def teardown_db():
    if os.path.exists("test_portfolio.db"):
        os.remove("test_portfolio.db")

def test_fetch_portfolio():
    db_url = setup_db()
    
    try:
        response = client.post(
            "/portfolio/sql",
            json={
                "db_url": db_url,
                "query": "SELECT name, weight, mu, sigma FROM portfolio"
            }
        )
        print("Status code:", response.status_code)
        print("Response JSON:", response.json())
        
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["name"] == "AAPL"
        assert data[0]["weight"] == 0.4
        
        print("✅ tests passed.")
    finally:
        teardown_db()

if __name__ == "__main__":
    test_fetch_portfolio()
