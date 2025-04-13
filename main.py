from uuid import uuid4
from modules.agents.graphs.nodejs_backend_developer import NodeJsBackendDeveloper
import asyncio
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.logging.logger import setup_logger
from modules.types.common.models.requirements import Requirements
from modules.llms.llms import deep_infra_with_temperature
setup_logger()

project_name = "blogger_llama_3_3_70b"
project_description="""
### Project Overview
The Book Manager is an online bookstore platform designed to facilitate book sales and community engagement through a secure, scalable, and user-friendly Node.js web application. It targets two primary user types: **customers**, who browse, purchase, and review books, and **administrators**, who manage inventory, orders, and promotions. The platform prioritizes fast performance, robust security, and maintainable code to deliver a seamless experience for up to 50,000 concurrent users.

**Objectives**:
- Provide a comprehensive book catalog with intuitive search and filter options.
- Enable secure user account management and transaction processing.
- Offer administrators tools to manage books, orders, and discounts efficiently.
- Support community engagement through book reviews and wishlists.

---

### Technology Stack
- **Backend**: Node.js with Express.js for building a RESTful API.
- **Database**: MongoDB for flexible, schema-less storage of user, book, and order data.
- **Cloud Storage**: AWS S3 for storing book cover images and user profile pictures.
- **Payment Gateway**: Stripe for processing credit card and digital wallet payments.
- **Authentication**: JSON Web Tokens (JWT) for secure user sessions.
- **Containerization**: Docker for consistent development and deployment environments.
- **Caching**: Redis for caching frequently accessed book catalog data.
- **Testing**: Jest for unit and integration tests.
- **Internationalization**: i18n-node for English and Spanish API responses.

---

### Technical Requirements

#### User Management
- **Registration**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/register`
  - **Request Body**: `{ email, password, firstName, lastName, phoneNumber, address }`
  - **Response**: JSON with JWT token and user details `{ id, email, firstName, lastName }`.
  - **Authentication**: None
  - **Details**: Passwords require 8+ characters, including one letter and one number, hashed with bcrypt.
- **Login**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/login`
  - **Request Body**: `{ email, password }`
  - **Response**: JSON with JWT token and user details `{ id, email, firstName, lastName }`.
  - **Authentication**: None
- **Update Profile**:
  - **HTTP Method**: PUT
  - **Endpoint**: `/api/user`
  - **Request Body**: `{ firstName, lastName, phoneNumber, address, password (optional) }`
  - **Response**: JSON with updated user details.
  - **Authentication**: Bearer token (JWT)
- **Forgot Password**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/forgotpassword`
  - **Request Body**: `{ email }`
  - **Response**: JSON `{ message: "Password reset link sent" }`
  - **Authentication**: None
  - **Details**: Sends a reset link via email, valid for 1 hour.
- **Reset Password**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/resetpassword`
  - **Request Body**: `{ token, password, confirmPassword }`
  - **Response**: JSON `{ message: "Password reset successful" }`
  - **Authentication**: Reset token

#### Book Catalog
- **Browse Books**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/books`
  - **Query Parameters**: `genre (fiction, non-fiction, sci-fi, mystery, biography), author, priceRange (min, max), sort (price-asc, price-desc, publicationDate-desc)`
  - **Response**: JSON array of books, limited to 50 per request.
  - **Authentication**: None
- **Search Books**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/search`
  - **Query Parameters**: `query (title, author, ISBN)`
  - **Response**: JSON array of books, limited to 50 per request.
  - **Authentication**: None

#### Shopping Cart
- **Add to Cart**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/cart`
  - **Request Body**: `{ bookId, quantity }`
  - **Response**: JSON with updated cart `{ items: [{ bookId, title, quantity, price }], total }`.
  - **Authentication**: Bearer token (JWT)
  - **Details**: Maximum 10 units per book.
- **View Cart**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/cart`
  - **Response**: JSON with cart details `{ items: [{ bookId, title, quantity, price }], total }`.
  - **Authentication**: Bearer token (JWT)
  - **Details**: Persists for 30 days across sessions.
- **Update Cart Quantity**:
  - **HTTP Method**: PUT
  - **Endpoint**: `/api/cart/:bookId`
  - **Request Body**: `{ quantity }`
  - **Response**: JSON with updated cart.
  - **Authentication**: Bearer token (JWT)
- **Remove from Cart**:
  - **HTTP Method**: DELETE
  - **Endpoint**: `/api/cart/:bookId`
  - **Response**: JSON with updated cart.
  - **Authentication**: Bearer token (JWT)

#### Order Processing
- **Place Order**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/order`
  - **Request Body**: `{ shippingAddress, paymentMethod (credit-card, apple-pay, google-pay) }`
  - **Response**: JSON `{ orderId, status, total, items }`.
  - **Authentication**: Bearer token (JWT)
  - **Details**: Supports statuses: pending, processing, shipped, delivered.
- **Get Order History**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/orders`
  - **Response**: JSON array of orders `{ orderId, orderDate, status, total }`.
  - **Authentication**: Bearer token (JWT)

#### Admin Dashboard
- **Add Book**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/admin/book`
  - **Request Body**: `{ title, author, ISBN, genre, publicationYear, price, quantity, coverImageURL, description, format (hardcover, paperback, e-book) }`
  - **Response**: JSON with book details.
  - **Authentication**: Bearer token (JWT) with admin role
- **Update Book**:
  - **HTTP Method**: PUT
  - **Endpoint**: `/api/admin/book/:bookId`
  - **Request Body**: `{ title, author, ISBN, genre, publicationYear, price, quantity, coverImageURL, description, format }`
  - **Response**: JSON with updated book details.
  - **Authentication**: Bearer token (JWT) with admin role
- **Delete Book**:
  - **HTTP Method**: DELETE
  - **Endpoint**: `/api/admin/book/:bookId`
  - **Response**: JSON `{ message: "Book deleted" }`
  - **Authentication**: Bearer token (JWT) with admin role
- **Get Orders**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/admin/orders`
  - **Response**: JSON array of orders `{ orderId, userId, orderDate, status, total }`.
  - **Authentication**: Bearer token (JWT) with admin role
- **Update Order Status**:
  - **HTTP Method**: PUT
  - **Endpoint**: `/api/admin/order/:orderId`
  - **Request Body**: `{ status (pending, processing, shipped, delivered) }`
  - **Response**: JSON with updated order details.
  - **Authentication**: Bearer token (JWT) with admin role
- **Bulk Upload Books**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/admin/books/bulk`
  - **Request Body**: CSV file with columns `{ title, author, ISBN, genre, publicationYear, price, quantity, description, format }`
  - **Response**: JSON `{ message: "Books uploaded", count }`
  - **Authentication**: Bearer token (JWT) with admin role

#### Security
- **Authentication**: JWT tokens expire after 24 hours; refresh tokens valid for 7 days.
- **Authorization**: Role-based access (customer, admin).
- **Input Validation**: Sanitize inputs to prevent NoSQL injection, XSS, and CSRF.
- **Rate Limiting**: 10 login attempts per IP per minute; 5 password reset requests per IP per hour.
- **Encryption**: AES-256 for sensitive data (e.g., payment details in transit).
- **Two-Factor Authentication**: Optional for users via email OTP.

#### Internationalization
- Supports English and Spanish for API responses and error messages.
- Uses i18n-node with locale detection based on user profile settings.

#### Review System
- **Create Review**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/review`
  - **Request Body**: `{ bookId, rating (1–5), reviewText }`
  - **Response**: JSON with review details.
  - **Authentication**: Bearer token (JWT)
  - **Details**: Users can submit one review per book; no edits allowed.
- **Get Reviews**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/reviews/:bookId`
  - **Response**: JSON array of reviews `{ userId, rating, reviewText, createdAt }`.
  - **Authentication**: None

#### Wishlist
- **Add to Wishlist**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/wishlist`
  - **Request Body**: `{ bookId }`
  - **Response**: JSON with wishlist details.
  - **Authentication**: Bearer token (JWT)
  - **Details**: Maximum 50 books per wishlist.
- **Get Wishlist**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/wishlist`
  - **Response**: JSON array of books `{ bookId, title, author, price }`.
  - **Authentication**: Bearer token (JWT)

#### Promotional Discounts
- **Create Discount**:
  - **HTTP Method**: POST
  - **Endpoint**: `/api/admin/discount`
  - **Request Body**: `{ bookId, discountPercentage (1–50), expirationDate }`
  - **Response**: JSON with discount details.
  - **Authentication**: Bearer token (JWT) with admin role
  - **Details**: Applied automatically at checkout.
- **Get Discounts**:
  - **HTTP Method**: GET
  - **Endpoint**: `/api/admin/discounts`
  - **Response**: JSON array of discounts `{ bookId, discountPercentage, expirationDate }`.
  - **Authentication**: Bearer token (JWT) with admin role

#### Notifications
- **Order Confirmation**: Email sent to users after placing an order.
- **Order Status Update**: Email sent when order status changes (e.g., shipped).
- **Low Stock Alert**: Email sent to admins when book quantity falls below 10.

---

### Features

#### Functional Features
- User registration, login, and profile management.
- Book catalog with search by title, author, ISBN, and filters by genre, price, and publication date.
- Shopping cart persistent for 30 days, supporting up to 10 units per book.
- Order processing with Stripe integration for credit cards, Apple Pay, and Google Pay.
- Admin dashboard for managing books, orders, discounts, and bulk uploads.
- Review system allowing 1–5 star ratings and text reviews.
- Wishlist for saving up to 50 books.
- Promotional discounts applied automatically at checkout.
- Email notifications for order updates and low stock alerts.

#### Non-Functional Features
- **Security**: JWT authentication, role-based authorization, input sanitization, rate limiting, and AES-256 encryption.
- **Performance**: API response time under 200ms for 95% of requests; Redis caching for catalog queries; MongoDB indexes for fast searches.
- **Scalability**: Horizontal scaling with Docker containers; supports 50,000 concurrent users.
- **Usability**: Clear error messages in English and Spanish; RESTful API with OpenAPI documentation.
- **Maintainability**: Modular Express.js routes, Jest test coverage >80%, and ESLint for code quality.

---

### Schema-Relevant Details
MongoDB collections are designed for flexibility and performance:

- **Users**:
  - `_id`: ObjectId (primary key)
  - `email`: String (unique, required)
  - `password`: String (hashed, required)
  - `firstName`: String (required)
  - `lastName`: String (required)
  - `phoneNumber`: String
  - `address`: String
  - `profilePictureURL`: String
  - `role`: String (customer, admin, default: customer)
  - `createdAt`: Date
  - `lastLogin`: Date
- **Books**:
  - `_id`: ObjectId (primary key)
  - `title`: String (required)
  - `author`: String (required)
  - `ISBN`: String (unique, required)
  - `genre`: String (fiction, non-fiction, sci-fi, mystery, biography)
  - `publicationYear`: Number
  - `price`: Number (required)
  - `quantity`: Number (required)
  - `coverImageURL`: String
  - `description`: String
  - `format`: String (hardcover, paperback, e-book)
- **Orders**:
  - `_id`: ObjectId (primary key)
  - `userId`: ObjectId (reference to Users)
  - `orderDate`: Date
  - `status`: String (pending, processing, shipped, delivered)
  - `totalCost`: Number
  - `shippingAddress`: String
  - `paymentStatus`: String (pending, completed)
- **OrderItems**:
  - `_id`: ObjectId (primary key)
  - `orderId`: ObjectId (reference to Orders)
  - `bookId`: ObjectId (reference to Books)
  - `quantity`: Number
  - `unitPrice`: Number
- **Reviews**:
  - `_id`: ObjectId (primary key)
  - `userId`: ObjectId (reference to Users)
  - `bookId`: ObjectId (reference to Books)
  - `rating`: Number (1–5)
  - `reviewText`: String
  - `createdAt`: Date
- **Wishlist**:
  - `_id`: ObjectId (primary key)
  - `userId`: ObjectId (reference to Users)
  - `bookId`: ObjectId (reference to Books)
- **Discounts**:
  - `_id`: ObjectId (primary key)
  - `bookId`: ObjectId (reference to Books)
  - `discountPercentage`: Number (1–50)
  - `expirationDate`: Date

**Notes**:
- MongoDB indexes on `email` (Users), `ISBN` (Books), and `bookId` (Reviews, Wishlist, Discounts) ensure fast queries.
- References use ObjectId to maintain relationships without rigid schemas.
- Timestamps (`createdAt`) track creation for auditing.
"""

if __name__ == "__main__":
    process_id = project_name
    memory = DeveloperMemory(id=process_id)
    requirements = Requirements(
        project_name=project_name,
        description=project_description,
        packages=[]
    )
    developer = NodeJsBackendDeveloper(
        id=process_id,
        requirements=requirements,
        llm_with_temperature=deep_infra_with_temperature,
        memory=memory
    )
    asyncio.run(developer.arun())