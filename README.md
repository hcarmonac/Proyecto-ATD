# 📈 StockPulse: Integrated Market Analytics

**A High-Performance Client-Server Stock Analysis Tool** *Developed for the Adquisición y Transmisión de Datos (ATD) Course, 2025-2026.*

---

## 🚀 Project Overview

**StockPulse** is a financial intelligence tool designed to bridge the gap between raw market data and actionable insights. By integrating multiple data acquisition techniques —including **REST APIs** and **Dynamic Web Scraping**— the system provides a 360-degree view of any stock ticker.

The project follows a **Client-Server architecture** implemented via **TCP Sockets**, ensuring a separation of concerns where the server handles heavy data lifting and the client focuses on interactive visualization.

### 🎯 Objectives

* **Multi-Source Integration:** Correlate technical price history with fundamental ratios and real-world news.

* **Advanced Data Acquisition:** Utilize `Selenium`, `Requests`, and `RESTful APIs`.

* **Efficient Transmission:** Implement a robust `Socket` communication protocol to transfer complex JSON payloads.

* **Data Refinement:** Apply filtering and mapping logic to transform raw data into human-readable economic interpretations.

---

## 🛠 Tech Stack

| Category | Tools |
| :--- | :--- |
| **Language** | Python 3.11+ |
| **Data Acquisition** | Selenium, BeautifulSoup (Testing), Requests |
| **APIs** | TwelveData, Financial Modeling Prep (FMP) |
| **Networking** | Sockets (TCP/IP), JSON serialization |
| **Visualization** | Plotly, Tabulate, Webbrowser |

---

## 🏗 System Architecture
The system is divided into three main components:

### 1. The Server (`server.py`)

The engine of the project. It listens for incoming connections and orchestrates data retrieval from **four distinct sources**:

* **TwelveData API:** Retrieves historical closing prices from the last 365 days.

* **FMP API:** Fetches analyst consensus, price targets, and future growth estimates.

* **Finviz (Selenium):** Scrapes the "Snapshot" table for real-time fundamental ratios like P/E, ROE, and Debt/Eq.

* **El Mundo (Selenium):** Performs an advanced search for the latest economic news in Spanish related to the company.

### 2. The Client (`client.py`)

A user-friendly interface that:

1. Connects to the server via IP and Port.

2. Validates tickers using the `yfinance` library.

3. Receives and unpacks JSON data.

4. Generates an interactive **Plotly** graph and renders a formatted financial report in the terminal.

### 3. Testing Environment (`testing_notebook.ipynb`)

A modular playground used during development to isolate functions and debug scraping selectors before integration.

---

## 💎 Features (Grading Criteria)

### 📊 Multi-Web Data Correlation

We exceed the requirement of *members + 1* sources by integrating **4 high-value sources**, relating technical trends with market sentiment and public news.

### 🔍 Data Filtering (Bonus)
Raw data is processed via `generate_financial_summary`. This function maps obscure API keys to readable names and adds an **"Economic Interpretation"** column to help users understand metrics like RSI or Debt/Equity.

### 🌐 Socket Communication (Bonus)
Implemented a full **TCP Socket** lifecycle:
* **Server-side:** Concurrent-ready binding on port 10000 and listening for requests.
* **Client-side:** Structured request-response pattern using encoded JSON strings.

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/stockpulse-atd.git](https://github.com/your-username/stockpulse-atd.git)
   cd stockpulse-atd

2. **Install dependencies**: The system relies on libraries such as `socket`, `selenium` or `requests` for data acquisition, transmission and display.
   ```bash
   pip install -r requirements.txt

3. **Run the server**: Execute `server.py` script to start the backend. The server will bind to the local IP and listen for TCP connections on port 10000.
   ```bash
   python .\server.py

4. **Run the client**: In a separate terminal, launch the `client.py` script. The application will prompt you for the server's IP address and port to establish the socket connection.
   ```bash
   python .\client.py

---

## 👥 The Team

- Hugo Carmona Casas

- Lluc Climent Navarro ([LinkedIn](https://www.linkedin.com/in/lluc-climent-85116538a/))

- Juan López Blasco ([LinkedIn](https://www.linkedin.com/in/juanlopez1590/))
