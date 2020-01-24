# -----------------
# Import statements
# -----------------
import tkinter as tk
from tkinter import ttk
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import webbrowser

WIDTH = 960
HEIGHT = 540
MAX_BAR_HEIGHT = 0.75
HELP_URL = 'https://coinmarketcap.com/'
API_KEY = ''    # <- PASTE YOUR API KEY HERE


def open_help_url():
    webbrowser.open_new(HELP_URL)


def convert(curr1, curr2, fiat):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    curr1 = curr1.upper();
    curr2 = curr2.upper();
    params = {
        # 'slug': curr1 + ',' + curr2,
        'symbol': curr1 + "," + curr2,
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

        name1 = data['data'][curr1]['name']
        name2 = data['data'][curr2]['name']
        symbol1 = data['data'][curr1]['symbol']
        symbol2 = data['data'][curr2]['symbol']
        price1 = round(float(data['data'][curr1]['quote'][fiat]['price']), 2)
        price2 = round(float(data['data'][curr2]['quote'][fiat]['price']), 2)
        rank1 = data['data'][curr1]['cmc_rank']
        rank2 = data['data'][curr2]['cmc_rank']

        graph_title['text'] = name1 + ' to ' + name2
        if price1 > price2:
            height1 = MAX_BAR_HEIGHT
            height2 = price2 / price1 * MAX_BAR_HEIGHT
        else:
            height1 = price1 / price2 * MAX_BAR_HEIGHT
            height2 = MAX_BAR_HEIGHT

        curr_1_bar.place(relx=0.2, rely=0.9, relwidth=0.1, relheight=height1, anchor='s')
        curr_2_bar.place(relx=0.35, rely=0.9, relwidth=0.1, relheight=height2, anchor='s')
        curr_1_label['text'] = name1 + " (" + symbol1 + ")\n" + str(price1) + ' ' + fiat
        curr_2_label['text'] = name2 + " (" + symbol2 + ")\n" + str(price2) + ' ' + fiat
        curr_1_label.place(relx=0.2, rely=0.91, anchor='n')
        curr_2_label.place(relx=0.35, rely=0.91, anchor='n')
        curr_1_price_label['text'] = str(price1)+" "+fiat
        curr_2_price_label['text'] = str(price2)+" "+fiat
        graph_middleground['bg']='#000'

        info_label['text'] = '1 ' + symbol1 + ' = ' + str(round(price1 / price2, 10)) + ' ' + symbol2 + '.\n'
        info_label['text'] += name1 + ' is currently ranked #' + str(rank1) + '.\n'
        info_label['text'] += name2 + ' is currently ranked #' + str(rank2) + '.'

    except KeyError as e:
        info_label['text'] = 'One or both crypto symbols is invalid.\n'
        info_label['text'] += 'Please use a supported abbreviated code.\n(e.g. BTC)'

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        info_label['text'] = 'One or both crypto symbols is invalid.'
        print(e)


# Create Tkinter window
root = tk.Tk()
root.title("Cryptocurrency Calculator")
root.iconbitmap('icon.ico')

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT)
canvas.pack()

background_image = tk.PhotoImage(file='background.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)


# Top frame entry panel
top_frame = tk.Frame(root, bg='#ccc', bd=5)
top_frame.place(relx=0.5, rely=0.025, relwidth=0.85, relheight=0.15, anchor='n')

entry_curr_1 = tk.Entry(top_frame, font=40)
entry_curr_1.place(relwidth=0.57, relheight=0.45)

entry_curr_2 = tk.Entry(top_frame, font=40)
entry_curr_2.place(rely=0.5, relwidth=0.57, relheight=0.45)

combobox_fiat = ttk.Combobox(top_frame, font=40, values=[
    "AUD",
    "CAD",
    "CHF",
    "EUR",
    "GBP",
    "INR",
    "JPY",
    "RUB",
    "USD"
])
combobox_fiat.current(8)
combobox_fiat.place(relx=0.575, relwidth=0.425, relheight=0.45)

button = tk.Button(top_frame, text="Look Up Currency", font=40, command=lambda: convert(entry_curr_1.get(), entry_curr_2.get(), combobox_fiat.get()))
button.place(relx=0.575, rely=0.5, relwidth=0.425, relheight=0.45)


# Center frame output panel
center_frame = tk.Frame(root, bg='#ccc', bd=5)
center_frame.place(relx=0.5, rely=0.2, relwidth=0.85, relheight=0.775, anchor='n')

# Left-hand graph panel
graph_background = tk.Label(center_frame, bg='#eee')
graph_middleground = tk.Label(center_frame, bg='#eee')
graph_foreground = tk.Label(center_frame, bg='#eee')
graph_background.place(relwidth=1, relheight=1)
graph_middleground.place(relx=0.1, rely=0.91, relwidth=0.36, relheight=MAX_BAR_HEIGHT+0.02, anchor='sw')
graph_foreground.place(relx=0.105, rely=0.9, relwidth=0.35, relheight=MAX_BAR_HEIGHT, anchor='sw')

graph_title = tk.Label(center_frame, font=160, fg='#000')
graph_title.place(relx=0.1, rely=0.1, anchor='w')
curr_1_bar = tk.Frame(center_frame, bg='#e33')
curr_2_bar = tk.Frame(center_frame, bg='#33e')
curr_1_label = tk.Label(center_frame, fg='#000')
curr_2_label = tk.Label(center_frame, fg='#000')
curr_1_price_label = tk.Label(center_frame, fg='#000')
curr_2_price_label = tk.Label(center_frame, fg='#000')


# Right-hand information panel
info_pane = tk.Frame(center_frame, bg='#222', bd=5)
info_pane.place(relx=0.575, relwidth=0.425, relheight=1)
info_label = tk.Label(info_pane, font=16, bg='#444', fg='#fff')
info_label.place(relwidth=1, relheight=1)

help_button = tk.Button(info_pane, text='Supported Cryptocurrencies', font=40, command=lambda: open_help_url())
help_button.place(relx=0.5, rely=0.95, relwidth=0.9, height=48, anchor='s')


# Start GUI and main loop
root.mainloop()
