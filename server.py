# Necessary imports
import requests
from datetime import date, timedelta, datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import yfinance as yf
from tabulate import tabulate
from socket import *
import json
import re

def get_graph_data(ticker):
    """
    
        Obtains the data of the stock price evolution for a given ticker over the last year

        Parameters:
            ticker (str): Stock ticker symbol
        
        Returns:
            A dictionary containing the data for making the plot with Plotly {dates: [], prices: []}
    
    """
    
    # Variables and API setup
    API_KEY = 'ea51535a06ab42f0824812f815f2eb08' 
    OUTPUT_SIZE = 252
    URL = 'https://api.twelvedata.com/time_series'
    START_DATE = (date.today() - timedelta(days=365)).isoformat()

    params = {
        'symbol': ticker,
        'interval': '1day',
        'outputsize': OUTPUT_SIZE,
        'start_date': START_DATE,
        'order': 'asc',
        'apikey': API_KEY
    }
    
    # Make the API request
    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        values = data['values']
        
        # Extract dates and prices
        dates, prices = [], []
        for day in values:
            # Para que la fecha tenga el mismo formato que las news y poder plotear
            date_obj = datetime.strptime(day['datetime'], '%Y-%m-%d')
            dates.append(date_obj)
            prices.append(float(day['close']))
        
        return {'ticker': ticker, 'dates': dates, 'prices': prices}

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None
    
def get_estimations(ticker):
    """
    
        Fetch financial estimations from Financial Modeling Prep API
        
        Parameters:
            ticker: str - The stock ticker symbol to search for.
        Returns:
            Dictionary with the fetched estimations (key-value pairs including metrics like price target, earnings estimates, etc.)
    
    """
    
    # Financial Modeling Prep (FMP) API key for estimations
    API_KEY = 'm6B6VyNRoaMYJOIxJPWLzD6K9oVopgoe'
    
    # Prepare the URLs
    URL_FINANCIAL_ESTIMATES = f'https://financialmodelingprep.com/stable/analyst-estimates'
    params_financial_estimates = {
        'apikey': API_KEY,
        'symbol': ticker.upper(),
        'period': 'annual'
    }
    
    URL_PRICE_TARGET_CONSENSUS = f'https://financialmodelingprep.com/stable/price-target-consensus'
    params_price_target_consensus = {
        'apikey': API_KEY,
        'symbol': ticker.upper()
    }
    
    URL_STOCK_GRADES = f'https://financialmodelingprep.com/stable/grades-consensus'
    params_stock_grades = params_price_target_consensus
    
    # Function to fetch data
    def fetch_data(url, params):
        try:
            # Make the GET request to the API endpoint
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Process the response data
            if isinstance(data, list):
                return data[0] if data else {}
            
            if isinstance(data, dict):
                return data
            
            # Handle unexpected data format
            print(f"Unexpected data format from {url}: {type(data)}")
            return {}
        
        # Handle request exceptions
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching data from {url}: {e}")
            return {}
    
    # Fetch data from the three endpoints
    financial_estimates = fetch_data(URL_FINANCIAL_ESTIMATES, params_financial_estimates)
    price_target_consensus = fetch_data(URL_PRICE_TARGET_CONSENSUS, params_price_target_consensus)
    stock_grades = fetch_data(URL_STOCK_GRADES, params_stock_grades)
    
    # Return combined data
    return {**financial_estimates, **price_target_consensus, **stock_grades}
    
def get_information(ticker):
    """
    
        Selenium Web Scraping from finviz.com
        
        Parameters:
            ticker: str - The stock ticker symbol to search for.
        Returns:
            Dictionary with the extracted information (key-value pairs including metrics like P/E ratio, market cap, etc.)
    
    """
    # Hide warnings from Selenium
    options = Options()
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    # Initialize the WebDriver and information dictionary
    driver = webdriver.Chrome(options=options)
    info = {}
    
    # Full screen the window
    driver.maximize_window()
    
    try:
        # Access the website
        driver.get("https://finviz.com/")
        
        # Handle cookie consent pop-up
        time.sleep(1)  # Wait for the pop-up to appear

        """leer_mas = driver.find_element(By.CSS_SELECTOR, ".Button__StyledButton-buoy__sc-a1qza5-0.elJono")
        if leer_mas:
            leer_mas.click()"""

        cookie_reject_button = driver.find_element(By.CLASS_NAME, "Button__StyledButton-buoy__sc-a1qza5-0")
        cookie_reject_button.click()
        
        # Locate the search input field and enter the ticker symbol. Then wait 0.5 seconds and press ENTER
        search_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.TAG_NAME, "input")))
        search_input.click()
        search_input.send_keys(ticker.upper())
        time.sleep(0.5)
        search_input.send_keys(Keys.ENTER)
        
        # Wait for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "snapshot-table2")))
        
        # Extract the required information
        table = driver.find_element(By.CLASS_NAME, "snapshot-table2")
        rows = table.find_elements(By.TAG_NAME, "tr")
        
        # Iterate through rows and extract key-value pairs
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for i in range(0, len(cells), 2):
                key = cells[i].text
                value = cells[i + 1].text
                info[key] = value
    
    # Handle exceptions
    except Exception as e:
        print(f"An error occurred: {e}")
    
    # Ensure the driver is closed properly
    finally:
        time.sleep(1)
        driver.quit()
    
    # Return the extracted information
    return info

def get_news(ticker):
    """
    
    Selenium Web Scraping from elmundo.es for news related to the company represented by the ticker symbol.
    
    Parameters:
        ticker: str - The stock ticker symbol to search for.
        
    Returns:
        List of tuples containing (date, title, link) of relevant news articles.
    
    """
    # This function cleans company names by removing initial articles and legal suffixes (like "Inc." or "S.A.") using regular expressions to extract only the commercial brand name
    def filtrar(nombre):
        #Remove 'the' if it starts in the company name
        if nombre.lower().startswith("the "):
            nombre = nombre[4:]
        
        # Specify separations with legal sufixes and other
        patron_sufijos = r',|\bInc\b|\bCorp\b|\bS\.A\b|\bCorporation\b|\bAG\b|\bN\.V\b|\bSE\b|& Co|\bPLC\b|\bLtd\b|\.com\b|\bPlatforms\b|\bGroup\b|\bMotor\b|\bHoldings\b|\bIncorporated\b|\bCompany\b'    

        #Separe the company name with the sufixes
        partes = re.split(patron_sufijos, nombre, flags=re.IGNORECASE)
        
        resultado = partes[0].strip()
        return resultado
        
    # Get company name from ticker
    try:
        empresa = yf.Ticker(ticker).info['shortName']
        empresa = filtrar(empresa)
    except:
        empresa = ticker  # If fails, use ticker as company name
    
    # Hide warnings from Selenium
    options = Options()
    options.add_argument('--log-level=3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    
    # Initialize WebDriver
    try:
        driver = webdriver.Chrome(options=options)
        driver.get('https://www.elmundo.es/')
        driver.maximize_window()
    
    except:
        print("Error initializing WebDriver or accessing elmundo.es")
    
    # Handle cookies pop-up
    try:
        cookies_button=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "ue-accept-notice-button"))
                )
        cookies_button.click()
    except:
        print("Error handling cookies pop-up")
    
    # Click search button
    try:
        search_button=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "ue-c-main-header__search-box"))
                )
        search_button.click()
    except:
        print("Error clicking search button")
    
    # Click advanced search
    try:
        busqueda_avanzada=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "búsqueda avanzada »"))
                )
        busqueda_avanzada.click()
    except:
        print("Error clicking advanced search")
        
    # Choose 50 results per page
    try:
        WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'consejos'))) # Wait for all options to load
        desplegables = driver.find_elements(By.CLASS_NAME, 'consejos') # Get all options
        select = Select(desplegables[2]) # Take the third
        select.select_by_value("50")
    except: 
        print("Error selecting the number of results per page")

    # Choose news from the last year
    try:
        WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'consejos')) # Wait for all options to load
                )
        select = Select(desplegables[0]) # Take the first
        select.select_by_value("365")
    except: 
        print("Error selecting the number of results per page")
        
    # Choose 70% match percentage
    try:
        select = Select(desplegables[3]) # Take the fourth
        select.select_by_value("70")
    except: 
        print("Error selecting the match percentage")
        
    # Send keys of the company name and submit
    try:
        insertar_nombre=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.ID, "q"))
                )
        insertar_nombre.send_keys(empresa)
        insertar_nombre.send_keys(Keys.ENTER)
    
    except:
        print("Error sending keys of the company name")
        
    # Click a button to sort news by date
    try:
        boton_ordenar_fecha=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Ordenar por FECHA"))
                )
        boton_ordenar_fecha.click()
    except:
        print("Error with the button to sort by date")

    # Click on economy to only show economic news
    try:
        boton_economia=WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.LINK_TEXT, "Economía"))
                )
        boton_economia.click()
    except:
        print("Error with the button for economic news")
    
    lista=[]
    # Collect data from each page and then click on the next page button if it exists; if it doesn't exist, break the loop
    while True:
        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.TAG_NAME, "li"))) # Wait for all li elements to load
            
            todos_los_li = driver.find_elements(By.TAG_NAME, "li")
        
            # We only save the news that have the company name in their text (title or subtitle)
        except:
            print("Error getting the li elements of the news")
        
    # Filter important news and save dates (coherence 80% or more)
        try:
            for i in todos_los_li:
                if empresa.lower() in i.text.lower():
                    elemento_a = i.find_element(By.TAG_NAME, 'a')
                    titulo = elemento_a.text
                    enlace = elemento_a.get_attribute('href')
                    # Cambia el formato con el de las fechas del gráfico para plotear
                    fecha_sucia = i.find_element(By.CLASS_NAME, 'fecha').text
                    fecha_object = datetime.strptime(fecha_sucia, '%d/%m/%Y')
                    lista.append((fecha_object, titulo, enlace))
        except:
            print("Error filtering that the company name is in the title or subtitle and saving it")
            
    # Go to the next page    
        try:
            boton_siguiente_pag=WebDriverWait(driver, 2).until(
                        EC.element_to_be_clickable((By.LINK_TEXT, "Siguiente »"))
            )
            
            boton_siguiente_pag.click()
        except:
            break
    
    # Close the driver
    time.sleep(1)
    driver.quit()
    
    # Return the list of news
    return lista

def generate_financial_summary(raw_data):
    """
    
        Filter financial data and generate a formatted table with key metrics and interpretations.
        
        Parameters:
            raw_data: dict - Dictionary containing raw financial metrics from web scraping and API calls.
        Returns:
            String containing a formatted table with filtered metrics, their values, and economic interpretations.
    
    """
    
    # Definition of metrics to filter and their explanations
    # Format: 'Original_Key': ('Readable_Name', 'Description/Importance')
    metrics_map = {
        'Price': ('Current Price', 'Current market value of the stock.'),
        'Market Cap': ('Market Capitalization', 'Total size of the company in the market.'),
        'Perf Year': ('Annual Performance', 'Percentage change in stock price over the last year.'),
        'P/E': ('P/E Ratio', 'Price/Earnings. Indicates how expensive the stock is.'),
        'Forward P/E': ('Forward P/E', 'Expected Price/Earnings ratio (lower values indicate potential improvement).'),
        'Target Price': ('Target Price', 'Price that analysts expect within 12 months.'),
        'consensus': ('Consensus', 'Average analyst opinion (Buy/Hold/Sell).'),
        'targetHigh': ('Analysts Ceiling', 'The most optimistic price target recorded.'),
        'EPS next Y': ('EPS Growth', 'Expected earnings growth for the next year.'),
        'ROE': ('ROE (%)', 'Return on Equity. Measures efficiency of capital use.'),
        'Debt/Eq': ('Debt/Capital', 'Leverage level. Low values indicate financial strength.'),
        'Profit Margin': ('Profit Margin', 'Percentage of revenue converted to profit.'),
        'RSI (14)': ('RSI Index', 'Indicates if the stock is overbought (>70) or oversold (<30).'),
        'revenueAvg': ('Revenue 2030 (Est)', 'Long-term revenue projection according to API.'),
        'numAnalystsEps': ('Number of Analysts', 'Quantity of experts covering this company.')
    }

    table_data = []
    
    # Filtering process (requirement for extra points)
    for key, (label, description) in metrics_map.items():
        value = raw_data.get(key, "N/A")
        table_data.append([label, value, description])

    # Table generation with tabulate
    headers = ["Metric", "Value", "Economic Interpretation"]
    
    return tabulate(table_data, headers=headers, tablefmt='rounded_grid')

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat() # Convierte la fecha a string "YYYY-MM-DD"
    raise TypeError ("Type %s not serializable" % type(obj))

def main():
    """
    
    Main server function to receive the ticker symbol from the client,
    fetch financial data, generate a summary (graphical and textual report), and send it back to the client.
    
    """
    
    # Server setup
    socket_server = socket(AF_INET, SOCK_STREAM)
    
    IP_ADDRESS = gethostbyname(gethostname())
    PORT = 10000
    socket_server.bind(('0.0.0.0', PORT))
    socket_server.listen()
    
    print(f"Server is listening for connections at IP {IP_ADDRESS} and port {PORT}...")
    
    # To be able to have multiple clients, this part should be in a loop:
    while True:
        # Wait for client connection
        (socket_connection, address) = socket_server.accept()
        
        print(f"Connection established with {address}")
        
        # Main loop to handle client requests
        while True:
            # Receive data from the client
            ticker = socket_connection.recv(4096).decode().strip()
            
            if ticker == 'EXIT':
                print("Exit command received. Shutting down the server.")
                break
            
            print(f"Received ticker symbol: {ticker.upper()}")
            
            # Fetch data and generate summary
            graph_data = get_graph_data(ticker)
            estimations, information = get_estimations(ticker), get_information(ticker)
            combined_data = {**estimations, **information}
            summary_table = generate_financial_summary(combined_data)
            news = get_news(ticker)
            
            # Make the response
            response = {
                'graph': graph_data,
                'summary_table': summary_table,
                'news': news
            }
            
            # Send the graph and summary back to the client
            socket_connection.send(json.dumps(response, default=json_serial).encode())            
            print("Response sent to the client.")
        
        # Close the connection
        socket_connection.close()
        print("Connection closed.")
        
        exit = input("Do you want to shut down the server? (y/n): ")
        if exit.lower() == 'y':
            break
        
    # Close the server socket
    socket_server.close()
    print("Server shut down.")

if __name__ == "__main__":
    main()
