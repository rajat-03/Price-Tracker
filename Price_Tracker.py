import bs4
import urllib.request
import smtplib
import time
import datetime
import csv
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
from twilio.rest import Client

# Create the main window
top = Tk()
top.geometry("612x408")
top.config(bg="black")
top.minsize(612, 408)
top.maxsize(612, 408)
top.title("Price Tracker")

# Create the title label
title = Label(top, text="PRICE TRACKER", font="comicsansms 30 bold underline", bg="black", fg="yellow")
title.pack(pady=20)

# Create the URL input label and entry
input_url = Label(top, text="ENTER THE  PRODUCT'S FLIPKART URL.", font="Arial 15", bg="black", fg="yellow")
input_url.pack()
url_entry = Entry(top, font="Arial 15")
url_entry.pack(pady=10)

# Create the desired price input label and entry
desire_price = Label(top, text="ENTER THE DESIRED PRICE", font="Arial 15", bg="black", fg="yellow")
desire_price.pack()
inp_dp = Entry(top, font="Arial 15")
inp_dp.pack(pady=10)

# Create the mobile number input label and entry
phone_label = Label(top, text="ENTER YOUR MOBILE NUMBER", font="Arial 15", bg="black", fg="yellow")
phone_label.pack()
phone_entry = Entry(top, font="Arial 15")
phone_entry.pack(pady=10)

# Function to check the price
def check_price():
    url = url_entry.get()
    desired_price = float(inp_dp.get())
    user_phone_number = phone_entry.get()

    if not desired_price:
        messagebox.showerror("Error", "Desired price is empty.")
        return

    try:
        desired_price = float(desired_price)
    except ValueError:
        messagebox.showerror("Error", "Invalid desired price.")
        return

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'
    }
    req = urllib.request.Request(url, headers=headers)

    try:
        read_url = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        messagebox.showerror("Error", f"HTTP Error: {e.code}")
        return

    parse = bs4.BeautifulSoup(read_url, 'html.parser')

    # Extract the price element based on Flipkart's HTML structure
    price_element = parse.find('div', {'class': '_30jeq3 _16Jk6d'})
    product_name_element = parse.find('span', {'class': 'B_NuCI'})

    if price_element and product_name_element:
        prices = price_element.get_text()
        prices = float(prices.replace(",", "").replace("₹", ""))
        product_name = product_name_element.get_text()

        if prices <= desired_price:
            send_sms(product_name, prices, user_phone_number)
        else:
            print(f"Current Price: ₹{prices}")

    else:
        print(parse)  # Print the parsed HTML for troubleshooting
        messagebox.showerror("Error", "Price or product name not found on the page")

    # Call the check_price function again after 1 minute
    top.after(60000, check_price)

# Rest of your code...

# Function to send an SMS message
def send_sms(product_name, price, user_phone_number):
    # Configure your Twilio account settings
    account_sid = 'ACa000ac3b73dafacd10da86f91fb35ffb'
    auth_token = 'e164a794cc9ea758d43441ce66c1fb28'
    twilio_phone_number = "+12298007160"

    # Initialize the Twilio Client
    client = Client(account_sid, auth_token)

    # Create the SMS message body with the product name
    body = f"Price Alert: The price for {product_name} has reached or dropped below the desired price.\nPrice: ₹{price}"

    # Send the SMS message using Twilio
    message = client.messages.create(
        body=body,
        from_=twilio_phone_number,
        to= "+91"+user_phone_number
    )

# Create the button to start tracking
start_button = Button(top, text="Start Tracking", font="Arial 15", command=check_price)
start_button.pack(pady=20)

top.mainloop()

