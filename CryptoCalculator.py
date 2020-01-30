# -----------------
# Import statements
# -----------------
import tkinter as tk
from tkinter import ttk
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

WIDTH = 960
HEIGHT = 540
HELP_URL = 'https://coinmarketcap.com/'
API_KEY = ''    # <- PASTE YOUR API KEY HERE


def open_help_url():
    webbrowser.open_new(HELP_URL)


def convert(curr_string, fiat):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    formatted_curr_string = curr_string.replace(' ', '').upper()
    curr_key = formatted_curr_string.split(',')
    while '' in curr_key:
        curr_key.remove('')

    try:
        while True:
            formatted_curr_string.index(',,')
            formatted_curr_string = formatted_curr_string.replace(',,', ',')
    except ValueError as e:
        if formatted_curr_string.startswith(','):
            formatted_curr_string = formatted_curr_string[1:len(formatted_curr_string)]
        if formatted_curr_string.endswith(','):
            formatted_curr_string = formatted_curr_string[0:len(formatted_curr_string) - 1]

    params = {
        'symbol': formatted_curr_string,
        'convert': fiat
    }
    headers = {
        'Accepts': 'application.json',
        'X-CMC_PRO_API_KEY': API_KEY
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        print(data)

        currency_name = []
        currency_price = []

        for i in range(0, len(curr_key)):
            currency_name.append(data['data'][curr_key[i]]['name'] + ' \n(' + data['data'][curr_key[i]]['symbol'] + ')')
            currency_price.append(data['data'][curr_key[i]]['quote'][fiat]['price'])

        graph_figure = plt.Figure(figsize=(6, 5), dpi=100)
        graph_axis = graph_figure.add_subplot(1, 1, 1)
        graph_axis.bar(currency_name, currency_price)
        graph_canvas = FigureCanvasTkAgg(graph_figure, graph_frame)
        graph_canvas.draw()
        graph_axis.set_title('Cryptocurrency Prices')
        graph_axis.set_ylabel('Price (' + fiat + ')')
        for i, v in enumerate(currency_price):
            graph_axis.text(i, v + 3, str(round(v, 2)), ha='center', color='black')
        graph_canvas.get_tk_widget().place(relx=0, rely=0, relwidth=0.915, relheight=1)

    except KeyError as e:
        info_label['text'] = 'One or both crypto symbols is invalid.\n'
        info_label['text'] += 'Please use a supported\nabbreviated code.\n(e.g. BTC)'

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        info_label['text'] = 'One or both crypto symbols is invalid.'
        print(str(e))


# Create Tkinter window
root = tk.Tk()
root.title('Cryptocurrency Calculator')
root.iconbitmap('icon.ico')

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

background_image = tk.PhotoImage(file='background.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


# Top frame entry panel
top_frame = tk.Frame(root, bg='#ccc', bd=5)
top_frame.place(relx=0.5, rely=0.025, relwidth=0.85, relheight=0.15, anchor='n')

entry_curr = tk.Entry(top_frame, font=40)
entry_curr.place(relwidth=0.65, relheight=0.45)

combobox_fiat = ttk.Combobox(top_frame, font=40, values=[
    'AUD',
    'CAD',
    'CHF',
    'EUR',
    'GBP',
    'INR',
    'JPY',
    'RUB',
    'USD'
])
combobox_fiat.current(8)
combobox_fiat.place(rely=0.5, relwidth=0.65, relheight=0.45)

button = tk.Button(top_frame, text='Look Up Currency', font=40, command=lambda: convert(entry_curr.get(), combobox_fiat.get()))
button.place(relx=0.655, rely=0, relwidth=0.345, relheight=0.95)


# Graph panel
graph_frame = tk.Frame(root, bg='#ccc', bd=5)
graph_frame.place(relx=0.075, rely=0.2, relwidth=0.6, relheight=0.75, anchor='nw')

# Right-hand information panel
info_pane = tk.Frame(root, bg='#222', bd=5)
info_pane.place(relx=0.925, rely=0.2, relwidth=0.3, relheight=0.75, anchor='ne')

info_label = tk.Label(info_pane, bg='#222', fg='#fff', font=24)
info_label.place(relwidth=1, relheight=1)

help_button = tk.Button(info_pane, text='Supported Cryptocurrencies', font=40, command=lambda: open_help_url())
help_button.place(relx=0.5, rely=0.95, relwidth=0.9, height=48, anchor='s')


# Start GUI and main loop
root.mainloop()
