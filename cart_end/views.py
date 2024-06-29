import flask, flask_login
from shop_page.models import Product
from flask_mail import Message
from project.send_mail import mail

def show_cart_end_page():
    products_cookie = flask.request.cookies.get("products")
    print(products_cookie)
    if products_cookie:
        print(11111111111111111111111111111111111111111111)
        list_id_products = flask.request.cookies.get('products').split(' ')
        
        list_products = []
        list_same_id = []
        
        for id_products in list_id_products:
            count_products = list_id_products.count(id_products)
            if id_products not in list_same_id:
                product = Product.query.get(id_products)
                if product:
                    product.count = count_products
                    list_products.append(product)
                    list_same_id.append(id_products)
                else:
                    print(f"Product with ID {id_products} not found.")
        if flask.request.method == 'POST':
            # msg = Message(
            #     'Hello',
            #     sender='av3411261@gmail.com',
            #     recipients="av3411261@gmail.com",
            #     body=f'!\n\nВітаємо, ви купили:\n'
            # )
            # mail.send(msg)
            return flask.redirect('/Basket/')
    
        return flask.render_template(template_name_or_list= 'cart_end.html', products=list_products)
    else:
        return flask.render_template(template_name_or_list='cart_end.html')
