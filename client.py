from socket import *
import json
import yfinance as yf
import plotly.graph_objects as go
<<<<<<< HEAD
import webbrowser
import datetime as datetime

def make_graph(graph_data, news):
    """
    Create a Plotly graph for stock price evolution and save it as an image.
    
    Parameters:
        graph_data (dict): A dictionary containing 'dates' and 'prices' lists.
    
    Returns:
        str: The file path to the saved HTML graph.
    """
    ticker, dates, prices = graph_data['ticker'], graph_data['dates'], graph_data['prices']
    
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
            date_new = datetime.fromisoformat(new[0])
            title_new = new[1]
        except (ValueError, TypeError):
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
=======

def visualize_data(data, ticker):
    """
    Displays the summary table and generates an interactive Plotly chart.
    
    Args:
        data (dict): Dictionary containing 'quotes', 'news', and 'summary_table'.
        ticker (str): The stock symbol for the title.
    """
    
    # 1. Display summary table (Report)
    print("\n" + "="*50)
    print(f" INFORME FINANCIERO: {ticker}")
    print("="*50)
    
    if 'summary_table' in data:
        print(data['summary_table'])
    else:
        print("No hay tabla de resumen disponible.")
        
    print("\nGenerando gráfico interactivo ...")

    # 2. Prepare quote data
    quotes = data.get('quotes', {})
    if not quotes:
        print("No hay datos de cotización para graficar.")
        return

    dates = list(quotes.keys())
    prices = list(quotes.values())

    # 3. Prepare news data
    news_list = data.get('news', [])
    news_x = []
    news_y = []
    news_texts = []
    
    # Process news to place them on the chart
    # Note: News will only be plotted if their date matches a quote date 
    # to determine the Y-axis position (price).
    for item in news_list:
        if len(item) >= 2:
            n_date = item[0]
            n_title = item[1]
            # n_link = item[2] # Optional: access link if needed
            
            # Check if there is a quote for this exact date
            if n_date in quotes:
                news_x.append(n_date)
                news_y.append(quotes[n_date])
                # HTML format for hover: Bold title (Spanish label)
                news_texts.append(f"<b>Noticia:</b> {n_title}")

    # 4. Create the figure
    fig = go.Figure()

    # Trace 1: Stock Price Line
    fig.add_trace(go.Scatter(
        x=dates,
        y=prices,
        mode='lines',
        name='Cotización',
        line=dict(color='royalblue', width=2),
        hovertemplate='<b>Fecha:</b> %{x}<br><b>Precio:</b> $%{y:.2f}<extra></extra>'
    ))

    # Trace 2: News Markers
    if news_x:
        fig.add_trace(go.Scatter(
            x=news_x,
            y=news_y,
            mode='markers',
            name='Noticias Relevantes',
            marker=dict(color='red', size=10, symbol='circle'),
            text=news_texts, # The text containing the news title
            hovertemplate='%{text}<br><b>Fecha:</b> %{x}<br><b>Precio:</b> $%{y:.2f}<extra></extra>'
        ))

    # Layout configuration (Spanish titles)
    fig.update_layout(
        title=f'Evolución Histórica y Noticias de {ticker}',
        xaxis_title='Fecha',
        yaxis_title='Precio de Cierre ($)',
        hovermode="closest", # Highlights the point closest to the mouse
        template="plotly_white",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    # Show graph
    fig.show()
>>>>>>> ad0ab94241850d605caa07eb163b6f36cb632a93

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
                ticker = input("Enter the stock ticker symbol: ").upper().strip()
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
<<<<<<< HEAD
            graph_data, summary_table, news = data["graph"], data["summary_table"], data["news"]
            
            # Graph
            graph = make_graph(graph_data)
            
            webbrowser.open(graph)
            
            # Summary table
            print("Summary Table:\n")
            print(summary_table)
            
            # News
            print("\nNews:\n")
            for new in news:
                # Comprueba que la noticia se publique en un dia que la bolsa estuviera abierta para poder plotear
                if new in graph_data['dates']:
                    print(f"- Date: {new[0]}\n  Title: {new[1]}\n  Link: {new[2]}\n")
=======
            if data:
                visualize_data(data, ticker)
>>>>>>> ad0ab94241850d605caa07eb163b6f36cb632a93
        
        else:
            print("Invalid choice. Please try again.")
    
    # Close the socket
    client_socket.close()

if __name__ == "__main__":
    main()