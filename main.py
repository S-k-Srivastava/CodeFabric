import asyncio
from modules.logging.logger import setup_logger
from modules.graph.developer_agent import DeveloperAgent
from modules.types.enums import Technologies
from modules.types.models import Requirements

# Inputs
process_id = 2
project_description =  """
Got it! Here's a **non-technical client-style project description** that only lists the **features** and **high-level expectations** for the **Node.js eCommerce backend**, based solely on what the client sees or expects the system to support:
### 🛒 **eCommerce Backend – Client Requirements (Feature-Based)**

We need a backend system to power an eCommerce application. This backend will handle all the business logic and data for the following key areas:
### 1. **User Accounts**

* Users can sign up and log in using email and password.
* Users can reset their passwords if forgotten.
* Each user should have a profile (name, phone number, shipping addresses).
* Admin users should have a separate login and access to manage the platform.
### 2. **Product Management**

* Admins should be able to add, update, or delete products.
* Each product will have a name, description, price, stock quantity, images, categories, tags, and SKU.
* Products can be listed by users and browsed with filters (price, category, etc.).
### 3. **Shopping Cart**

* Logged-in users can add or remove products from their cart.
* Cart should persist per user and update quantities.
* Show total cart value and individual item prices.
### 4. **Wishlist**

* Users can add and remove items to a wishlist for future purchase.
### 5. **Checkout & Orders**

* Users can place orders from their cart.
* Orders must capture shipping address, items purchased, price, discount (if any), and payment status.
* Order status: pending, confirmed, shipped, delivered, cancelled.
* Users can view their past orders.
### 6. **Payments**

* Integration with a payment gateway like Stripe or Razorpay.
* Support online card payments and possibly COD (Cash on Delivery).
* Payment success/failure should be tracked and linked to orders.
### 7. **Discounts & Coupons**

* Admin can create and manage discount codes.
* Users can apply valid coupons during checkout to get discounts.
### 8. **Admin Dashboard (Backend Only)**

* Admins should be able to manage users, products, orders, and coupons.
* Admin should have visibility into platform metrics like total sales, top products, etc.
### 9. **Notifications**

* Email or SMS notifications for order confirmation, shipping updates, and password resets.
### 10. **Search and Filters**

* Users can search for products using keywords.
* Filters by category, price range, rating, availability, etc.
### 11. **Reviews and Ratings**

* Users can leave reviews and ratings for purchased products.
* Admin can moderate or delete inappropriate reviews.
### 12. **Delivery & Shipping**

* Each order must store shipping address and estimated delivery time.
* Shipping charges may vary based on region or order value.
### 13. **Security**

* Data must be secured; no unauthorized access to user info or admin features.
* Users should be logged out automatically after inactivity.
### 14. **Scalability and Speed**
* Backend should be fast, support high traffic, and responsive for mobile and web.
Would you like a visual sitemap or API endpoint list based on this?

"""

setup_logger(process_id)

dev_agent = DeveloperAgent(
    process_id=process_id,
    requirements=Requirements(
        project_name="flipkart-clone",
        project_description=project_description,
        packages=[],
        technology=Technologies.NodeJS.value,
    )
)

dev_agent.run()