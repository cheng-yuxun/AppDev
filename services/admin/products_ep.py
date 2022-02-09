from PIL import Image
from flask import Blueprint, render_template, request, redirect, url_for
import os
import os.path
import shelve
from data.db_ep import get_db
import shelve
from data.Product import Product
from services.forms.form_product import CreateProductForm, AddOrder

endpoint = Blueprint("products", __name__)
basedir = os.getcwd()

@endpoint.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open(get_db(), 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from Product.db.")

        product = Product(create_product_form.name.data, create_product_form.ptype.data,
                                  create_product_form.price.data, create_product_form.comments.data, create_product_form.stock.data)
        img = Image.open(request.files['image'])
        img.load()
        img.resize((1200, 600))
        img.convert('RGB')
        img.save(f"{basedir}/static/media/img_prod/{product.get_product_id()}.png")
        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict
        db.close()
        print(f"Product Key {product.get_product_id()} has been added successfully!")
        return redirect(url_for('products.retrieve_product'))
    return render_template('admin/products/createProduct.html', form=create_product_form)

@endpoint.route('/retrieveProduct')
def retrieve_product():
    products_dict = {}
    db = shelve.open(get_db(), 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)
    form = AddOrder(request.form)

    return render_template('admin/products/retrieveProduct.html', count=len(products_list), products_list=products_list, form=form)


@endpoint.route('/updateProduct/<id>/', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open(get_db(), 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_name(update_product_form.name.data)
        product.set_ptype(update_product_form.ptype.data)
        product.set_price(update_product_form.price.data)
        product.set_comments(update_product_form.comments.data)
        product.set_stock(update_product_form.stock.data)
        
        if request.files["image"].filename != "":
            img = Image.open(request.files["image"])
            img.load()
            img.resize((1200, 600))
            img.convert("RGB")
            img.save(f"{basedir}/static/media/img_prod/{product.get_product_id()}.png")
            print("image has been replaced")

        db['Products'] = products_dict
        db.close()

        return redirect(url_for('products.retrieve_product'))
    else:
        product_dict = {}
        db = shelve.open(get_db(), 'r')
        product_dict = db['Products']
        db.close()

        product = product_dict.get(id)
        update_product_form.name.data = product.get_name()
        update_product_form.ptype.data = product.get_ptype()
        update_product_form.price.data = product.get_price()
        update_product_form.comments.data = product.get_comments()
        update_product_form.stock.data = product.get_stock()

        return render_template('admin/products/update/updateProduct.html', form=update_product_form)

@endpoint.route('/deleteProduct/<id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open(get_db(), 'w')
    products_dict = db['Products']

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()

    return redirect(url_for('products.retrieve_product'))

@endpoint.route('/product_preview/<id>/', methods=['GET', 'POST'])
def product_preview(id):
    db = shelve.open(get_db(), 'r')
    products_dict = db['Products']
    db.close()
    products_id = products_dict.get(id)
    print(f'--- Retrieving Product {products_id.get_product_id()} Data ---')
    return render_template('admin/products/product_preview.html', products_id=products_id)

@endpoint.route('/product_details/<id>/', methods=['GET', 'POST'])
def product_details(id):
    db = shelve.open(get_db(), 'r')
    products_dict = db['Products']
    db.close()
    products_id = products_dict.get(id)
    print(f'--- Retrieving Product {products_id.get_product_id()} Data ---')
    return render_template('admin/admin_productdetails.html', products_id=products_id)

@endpoint.route("/status_products/<id>", methods=["POST"])
def status_products(id):
    db = shelve.open(get_db(), "w")
    products_dict = db['Products']
    products_id = products_dict.get(id)
    if products_id.get_status() == "Available":
        print(f"Product Key {products_id.get_product_id()} has been deactivated!")
        products_id.set_status("Unavailable")
    else:
        print(f"Product Key {products_id.get_product_id()} has been activated!")
        products_id.set_status("Available")
    db["Products"] = products_dict
    db.close()
    return redirect(request.referrer)