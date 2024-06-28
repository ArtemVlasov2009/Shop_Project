import flask
import flask_login
from flask_mail import Message
from shop_page.models import Product
from project.settings import db
from project.send_mail import mail
from registration_page.models import User
import requests

def send_telegram_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        if response.status_code == 200:
            print("Message sent successfully to Telegram.")
        else:
            print(f"Failed to send message to Telegram. Status code: {response.status_code}")
            print(response.json())  # Print the response JSON for debugging
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Telegram. Error: {e}")

def show_basket_page():
    if flask.request.cookies:
        list_id_products = flask.request.cookies.get('products').split(' ')
        
        list_products = []
        list_same_id = []
        
        for id_products in list_id_products:
            count_products = list_id_products.count(id_products)
            if id_products not in list_same_id:
                product = Product.query.get(id_products)
                if product:  # Ensure product is not None
                    product.count = count_products
                    list_products.append(product)
                    list_same_id.append(id_products)
                else:
                    print(f"Product with ID {id_products} not found.")
        
        if flask.request.method == 'POST':
            # Forming the text with product information
            products_info = '\n'.join([f"🛒 {product.name} (Кількість: {product.count})" for product in list_products])
            
            # Get the current user's email and name
            current_user = flask_login.current_user
            if current_user.is_authenticated:
                user_email = current_user.email
                user_name = current_user.name
            else:
                # If the user is not authenticated, you can use default values or handle this case differently
                user_email = 'default@example.com'
                user_name = 'Anonymous'
            
            msg = Message(
                'Hello',
                sender='nikitagodovanyj@gmail.com',
                recipients=[user_email],
                body=f'!\n\nВітаємо, ви купили:\n{products_info}'
            )
            mail.send(msg)

            # Send a message to the Telegram bot
            telegram_token = '7361656280:AAHdFpd4ce7f_Ri-JYL4O_nj_SmR2nHWD9M'
            chat_id = '-1002192574892_5'
            telegram_text = f'👤 Покупець: {user_name}\n✉️ Email: {user_email}\n\n🎉 Вітаємо, ви купили:\n{products_info}'
            send_telegram_message(telegram_token, chat_id, telegram_text)
        
        return flask.render_template(template_name_or_list='basket.html', products=list_products)
    else:
        return flask.render_template(template_name_or_list='basket.html')
