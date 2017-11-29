===============
Product Catalog
===============

An simple app to manage the products in a catalog (portfolio for example)

[under development ...]

Requirements
------------
- Django 1.11
- django-mptt 0.8.7
- Pillow 4.2.1
- django-extensions 1.9.1

Quick start
-----------

1. Add "product_catalog" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'product_catalog',
        'mptt',
        'django_extensions',
    ]


2. Include the product_catalog URLconf in your project urls.py like this::

    url(r'^catalog/', include('product_catalog.urls'))

3. Run `python manage.py migrate` to create the product_catalog models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a product / categories (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/catalog/ .


Optional
--------
if you want to use front-end product management, you must add
`product_catalog.context_processors.product_front_management` to the `context_processors`::

    TEMPLATES = [
        {
            [...]
            'OPTIONS': {
                'context_processors': [
                    [...]
                    'product_catalog.context_processors.product_front_management'
                ],
            },
        },
    ]

Settings parameters
-------------------
- **PRODUCT_CATALOG_PAGINATION**
    **Default value:** 10
    Integer used to paginate the products.

- **PRODUCT_CATALOG_PRODUCT_BASE_MODEL**
    **Default value:** 'product_catalog.models.product_abstract.AbstractProduct'
    String defining the base model path for the Entry model.

- **PRODUCT_CATALOG_UPLOAD_TO**
    **Default value:** 'uploads/product_catalog/%Y/%m/%d/'
    Path to upload image


**# Add / Update / Delete on front settings**

- **PRODUCT_CATALOG_FRONT_MANAGEMENT**
    **Default value:** True
    If 'True' allow to manage (create/update/delete) products in front.
    False to deactivate

- PRODUCT_CATALOG_PERMISSION_OPTIONS_SUPERUSER = 0
- PRODUCT_CATALOG_PERMISSION_OPTIONS_STAFF = 1
- PRODUCT_CATALOG_PERMISSION_OPTIONS_OWNER = 2

- **PRODUCT_CATALOG_ACCESS_PERMISSION**
    **Default value:** PRODUCT_CATALOG_PERMISSION_OPTIONS_OWNER

- **PRODUCT_CATALOG_FORM_FIELDS**
    **Default value:** ['title', 'status', 'excerpt', 'content', 'categories', 'image']
    list of available fields in update and create product form

- **PRODUCT_CATALOG_FORM_UPDATE_FIELDS**
    **Default value:** FORM_FIELDS
    list of available fields in update product form

- **PRODUCT_CATALOG_FORM_CREATE_FIELDS**
    **Default value:** FORM_FIELDS
    list of available fields in create product form
