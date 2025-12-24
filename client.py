# Necessary imports
from socket import *
import json
import yfinance as yf
import plotly.graph_objects as go
import webbrowser
from datetime import datetime

def make_graph(graph_data, news):
    """
    Create a Plotly graph for stock price evolution and save it as an image.
    
    Parameters:
        graph_data (dict): A dictionary containing 'dates' and 'prices' lists.
    
    Returns:
        str: The file path to the saved HTML graph.
    """
    ticker, dates_raw, prices = graph_data['ticker'], graph_data['dates'], graph_data['prices']
    
    # Convert date strings to datetime objects
    dates = [datetime.fromisoformat(d) if isinstance(d, str) else d for d in dates_raw]
    
    # 1. Plotea el gráfico de la evolución del stock
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dates, 
        y=prices, 
        mode='lines', 
        name=ticker.upper(),
        line=dict(color='royalblue', width=2),
        hovertemplate='<b>Precio:</b> $%{y:.2f}<extra></extra>'
    ))

    for new in news:
        # 2. Convertir la fecha de la noticia a datetime
        try:
            # new[0] is already a string in ISO format
            date_new = datetime.fromisoformat(new[0]) if isinstance(new[0], str) else new[0]
            title_new = new[1]
        except (ValueError, TypeError, AttributeError) as e:
            print(f"Error processing news date: {e}")
            continue

        # Plotea solo las noticias que coinciden con dias en los que la bolsa está abierta
        if date_new in dates:
            # Plotea las noticias como lineas verticales infinitas
            fig.add_vline(
                x=date_new, 
                line_width=1, 
                line_dash="dash", 
                line_color="grey"
            )

            fig.add_trace(go.Scatter(
                x=[date_new],
                y=[prices[dates.index(date_new)]],
                mode='markers',
                marker=dict(size=0, opacity=0),
                name='Noticia',
                text=[f"<b>Noticia:</b> {title_new}"],
                hovertemplate='%{text}<extra></extra>',
                showlegend=False
            ))

    fig.update_layout(
        title = f'{ticker.upper()} Stock Price Evolution Over the Last Year',
        xaxis_title = 'Date',
        yaxis_title = 'Closing Price (USD)',
        hovermode='x unified',
        hoverdistance=5,
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
            
            try:
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
                
                # Check if there was an error in the response
                if 'error' in data:
                    print(f"\nError from server: {data['error']}\n")
                    continue
                
                # Display the received data
                graph_data, summary_table, news = data["graph"], data["summary_table"], data["news"]
                
                # Graph
                graph = make_graph(graph_data, news)
                
                webbrowser.open(graph)
                
                # Summary table
                print("Summary Table:\n")
                print(summary_table)
                
                # News
                print("\nNews:\n")
                # Convert dates for comparison
                dates_set = set(datetime.fromisoformat(d) if isinstance(d, str) else d for d in graph_data['dates'])
                
                for new in news:
                    try:
                        # Convert news date to datetime for comparison
                        news_date = datetime.fromisoformat(new[0]) if isinstance(new[0], str) else new[0]
                        
                        # Check if the news date matches a trading day
                        if news_date in dates_set:
                            # Format date as YYYY-MM-DD only (without time)
                            date_formatted = news_date.strftime('%Y-%m-%d') if hasattr(news_date, 'strftime') else str(news_date).split('T')[0]
                            print(f"- Date: {date_formatted}\n  Title: {new[1]}\n  Link: {new[2]}\n")
                    except (ValueError, TypeError, AttributeError):
                        continue
            
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
                print(f"\nConnection error: {e}")
                print("Lost connection to server. Exiting...\n")
                break
            except Exception as e:
                print(f"\nUnexpected error: {e}")
                print("Please try again.\n")
        
        else:
            print("Invalid choice. Please try again.")
    
    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()