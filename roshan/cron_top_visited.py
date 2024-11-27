import os
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'roshan.settings')
import django
django.setup()
from api.models import Product

top_products = Product.objects.order_by('-visits')[:10]

cdir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(cdir, f"daily_visits/top_products_{datetime.now().strftime('%Y-%m-%d')}.csv")

with open(file_path, mode='w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Visits' , 'Product Name', 'Category Name'])

    for product in top_products:
        category_name = product.category.name
        writer.writerow([product.visits ,product.name, category_name])

print(f"Top 10 products generated! {file_path}")