===============
Product Catalog
===============

An ultra simple app to manage the products in a catalog (portfolio for example)

under development ...

Requirements
------------
- Django==1.11.5
- django-mptt==0.8.7
- Pillow==4.2.1
- django-extensions==1.9.1

Quick start
-----------

1. Add "product_catalog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'product_catalog',
    ]


2. Include the product_catalog URLconf in your project urls.py like this::

    url(r'^catalog/', include('product_catalog.urls'))

3. Run `python manage.py migrate` to create the product_catalog models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a product / categories (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/catalog/ .