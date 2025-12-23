# Necessary imports
from socket import *
import json
import yfinance as yf
import plotly.graph_objects as go
import webbrowser

def make_graph(graph_data):
    """
    
    Create a Plotly graph for stock price evolution and save it as an image.
    
    Parameters:
        graph_data (dict): A dictionary containing 'dates' and 'prices' lists.
    
    Returns:
        str: The file path to the saved HTML graph.
    """
    
    ticker, dates, prices = graph_data['ticker'], graph_data['dates'], graph_data['prices']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, 
        y=prices, 
        mode='lines', 
        name=ticker.upper(),
        line = dict(color='royalblue', width=2),
        hovertemplate = '<b>Precio:</b> $%{y:.2f}<extra></extra>'
        )
    )
    
    fig.update_layout(
        title = f'{ticker.upper()} Stock Price Evolution Over the Last Year',
        xaxis_title = 'Date',
        yaxis_title = 'Closing Price (USD)',
        hovermode = 'x unified',
        template = 'plotly_white',
        hoverlabel = dict(bgcolor="white", font_size=13, font_family="Rockwell")
    )
    
    fig.write_html(f"stock_price_graph.html")

    return "stock_price_graph.html"

def main():
    """
    Main function to run the client that communicates with the server.
    Asks for the server's IP address and port number, sends a request for data,
    receives the response and shows it.

    """
    
    # Ask for server IP and port
    server_ip = input("Enter the server IP address: ")
    server_port = int(input("Enter the server port number: "))
    
    # Create a TCP socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    print(f"Connected to server at {server_ip}:{server_port}")
    
    while True:
        print("-" * 50)
        print("  0 to request stock data")
        print("  1 to exit")
        print("-" * 50)
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            client_socket.send(b'EXIT')
            print("Exiting the client.")
            break
        
        elif choice == '0':
            
            # Asks for the ticker
            ticker = None
            # Loop for checking valid ticker
            while not ticker:
                ticker = input("Enter the stock ticker symbol: ")
                if not yf.Ticker(ticker).info:
                    print("Invalid ticker symbol. Please try again.")
                    ticker = None
            
            # Send a request for data
            client_socket.send(ticker.encode())
            
            print(f"Request sent for ticker: {ticker.upper()}")
            
            # Receive the response from the server
            response = client_socket.recv(100000).decode()
            
            print("Received data from server\n\n\n")
            
            if response:
                try:
                    # Parse the JSON response
                    data = json.loads(response)
                
                except json.JSONDecodeError:
                    print("Error decoding JSON response from server.")
                    continue
            
            else:
                print("No response received from server.")
                continue
            
            # Display the received data
            graph_data, summary_table, news = data["graph"], data["summary_table"], data["news"]
            
            # Graph
            graph = make_graph(graph_data)
            
            webbrowser.open(graph)
            
            # Summary table
            print("Summary Table:\n")
            print(summary_table)
            
            # News
            print("\nNews:\n")
            for news_item in news:
                print(f"- Date: {news_item[0]}\n  Title: {news_item[1]}\n  Link: {news_item[2]}\n")
        
        else:
            print("Invalid choice. Please try again.")
    
    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()