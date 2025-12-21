# Necessary imports
from socket import *
import json
import yfinance as yf

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
            
            print(f"Request sent for ticker: {ticker}")
            
            # Receive the response from the server
            response = client_socket.recv(4096).decode()
            
            print("Received data from server")
            
            # Parse the JSON response
            data = json.loads(response)
            
            # Display the received data
            data["graph"].show()
            print("Summary Table:")
            print(data["summary_table"])
            print("News:")
            for news_item in data["news"]:
                print(f"- Date: {news_item[0]}\n  Title: {news_item[1]}\n  Link: {news_item[2]}\n")
        
        else:
            print("Invalid choice. Please try again.")
    
    # Close the socket
    client_socket.close()