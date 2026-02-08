import random
from django.contrib.auth import get_user_model
from accounts.models import Address
from vendors.models import Vendor
from categories.models import Category, Product
from orders.models import Order, OrderItem
from payments.models import Payment
from courier.models import Delivery
from django.utils import timezone
from decimal import Decimal


User = get_user_model()

def run_seed():
    # --- USERS ---
    print("Creating an admmin...", end='')
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@fastyums.com',
        password='adminpass',
        role=User.Roles.ADMIN
    )
    print("Done✅")

    # Vendors
    print("Creating 2 vendor users...", end='')
    vendor_users = []
    for i in range(2):
        u = User.objects.create_user(
                username=f'vendor_{i+1}',
                email=f'vendor.{i+1}@fastyums.com',
                password='vendorpass',
                role=User.Roles.VENDOR
            )
        vendor_users.append(u)
    print("Done✅")

    # Couriers
    print("Creating 3 couriers...", end='')
    courier_users = []
    for i in range(3):
        u = User.objects.create_user(
                username=f'courier_{i+1}',
                email=f'courier.{i+1}@fastyums.com',
                password='courierpass',
                role=User.Roles.COURIER
            )
        courier_users.append(u)
    print("Done✅")

    # Customers
    print("Creating 5 customers...", end='')
    customer_users = []
    for i in range(5):
        u = User.objects.create_user(
                username=f'customer_{i+1}',
                email=f'customer.{i+1}@fastyums.com',
                password='customerpass',
                role=User.Roles.CUSTOMER
            )
        customer_users.append(u)
    print("Done✅")

    # --- VENDORS ---
    print("Creating vendors...", end='')
    vendors = []
    for u in vendor_users:
        vendor = Vendor.objects.create(
            owner=u,
            name=f"{u.username}'s Restaurant",
            description="Delicious food"
        )
        vendors.append(vendor)
    print("Done✅")

    # --- CATEGORIES ---
    print("Creating categories 'Fast Food', 'Drinks' & 'Desserts'...", end='')
    categories = []
    for name in ['Fast Food', 'Drinks', 'Desserts']:
        cat = Category.objects.create(name=name)
        categories.append(cat)
    print("Done✅")

    # --- PRODUCTS ---
    print("Creating 2 products by categories and vendors...", end='')
    products = []
    for vendor in vendors:
        for cat in categories:
            for j in range(2):
                p = Product.objects.create(
                    vendor=vendor,
                    category=cat,
                    name=f"{cat.name} Item {j+1} ({vendor.name})",
                    price=Decimal(random.randint(500, 5000)),
                    quantity=random.randint(10, 50),
                    available=True
                )
                products.append(p)
    print("Done✅")

    # --- ADDRESSES ---
    print("Creating address for all users...", end='')
    all_users = vendor_users + courier_users + customer_users
    for user in all_users:
        for n in range(random.randint(1, 2)):
            Address.objects.create(
                content_object=user,
                name=f"{user.username} Address {n+1}",
                street=f"{random.randint(100,999)} Main St",
                city="Calabar",
                state="NG-CR",
                country="Nigeria",
                is_default=(n==0)
            )

    # Adding 1 address for each vendor too (GenerocRelation)
    for vendor in vendors:
        Address.objects.create(
            content_object=vendor,
            name=f"{vendor.name} HQ",
            street=f"{random.randint(100,999)}, Vendor St",
            city="Calabar",
            state="NG-CR",
            country="Nigeria",
            is_default=True
        )
    print("Done✅")

    # --- ORDERS & ORDERITEMS ---
    print("Generating orders...", end='')
    orders = []
    for customer in customer_users:
        for k in range(2):
            order = Order.objects.create(
                user=customer,
                total_price=0,
                status=Order.Status.PENDING,
                address=customer.addresses.filter(is_default=True).first().to_dict
            )
            total = 0
            for _ in range(random.randint(1, 3)):
                product = random.choice(products)
                quantity = random.randint(1, 5)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price_at_purchase=product.price
                )
                total += product.price * quantity
            order.total_price = total
            order.save()
            orders.append(order)
    print("Done✅")

    # --- PAYMENTS ---
    print("Making payment for orders...", end='')
    for order in orders:
        Payment.objects.create(
            order=order,
            tx_ref=f"TX-{order.order_id}",
            amount=order.total_price,
            status=random.choice([Payment.PaymentStatus.SUCCESSFUL, Payment.PaymentStatus.PENDING])
        )
    print("Done✅")

    # --- DELIVERIES ---
    print("Delivering orders...", end='')
    for order in orders:
        if order.status != Order.Status.CANCELLED:
            Delivery.objects.create(
                order=order,
                courier=random.choice(courier_users),
                status=random.choice([
                    Delivery.DeliveryStatus.PENDING,
                    Delivery.DeliveryStatus.ASSIGNED
                ]),
                estimated_delivery_time=timezone.now() + timezone.timedelta(minutes=random.randint(20, 120))
            )
    print("Done✅")

    print("Seeding complete!")
