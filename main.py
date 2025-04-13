from uuid import uuid4
from modules.agents.graphs.nodejs_backend_developer import NodeJsBackendDeveloper
import asyncio
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.logging.logger import setup_logger
from modules.types.common.models.requirements import Requirements
setup_logger()

project_name = "blogger_llama_3_3_70b"
project_description="""
### Project Overview
The Book Manager project is a comprehensive online bookstore platform aiming to provide a robust and scalable Node.js web application. It serves both customers and administrators, offering distinct functionalities through a secure RESTful API. The platform encompasses user management, book catalog management, shopping cart functionality, order processing, and an administrative dashboard. Key objectives include delivering a fast, user-friendly, and secure application with a focus on clean code and maintainability.

### Technology Stack
- Node.js
- Relational database (e.g., PostgreSQL)
- Cloud storage service (e.g., AWS S3)
- Third-party payment gateway (e.g., Stripe)
- JWT for authentication
- Containerization for deployment

### Technical Requirements

#### User Management
- **Registration**:
  - HTTP Method: POST
  - Endpoint: /api/register
  - Request Body: { email, password, firstName, lastName, phoneNumber }
  - Response: JSON with authentication token (JWT) and user details
  - Authentication: None
- **Login**:
  - HTTP Method: POST
  - Endpoint: /api/login
  - Request Body: { email, password }
  - Response: JSON with authentication token (JWT) and user details
  - Authentication: None
- **Update Profile**:
  - HTTP Method: PUT
  - Endpoint: /api/user
  - Request Body: { firstName, lastName, phoneNumber, password (optional) }
  - Response: JSON with updated user details
  - Authentication: Bearer token (JWT)
- **Forgot Password**:
  - HTTP Method: POST
  - Endpoint: /api/forgotpassword
  - Request Body: { email }
  - Response: JSON with message indicating password reset link sent
  - Authentication: None
- **Reset Password**:
  - HTTP Method: POST
  - Endpoint: /api/resetpassword
  - Request Body: { password, confirmPassword }
  - Response: JSON with message indicating password reset success
  - Authentication: Password reset token

#### Book Catalog
- **Browse Books**:
  - HTTP Method: GET
  - Endpoint: /api/books
  - Query Parameters: filter (genre, author, priceRange), sort (price, publicationDate)
  - Response: JSON array of book objects
  - Authentication: None
- **Search Books**:
  - HTTP Method: GET
  - Endpoint: /api/search
  - Query Parameters: query (title, author, ISBN)
  - Response: JSON array of book objects
  - Authentication: None

#### Shopping Cart
- **Add to Cart**:
  - HTTP Method: POST
  - Endpoint: /api/cart
  - Request Body: { bookId, quantity }
  - Response: JSON with updated cart details
  - Authentication: Bearer token (JWT)
- **View Cart**:
  - HTTP Method: GET
  - Endpoint: /api/cart
  - Response: JSON with cart details
  - Authentication: Bearer token (JWT)
- **Update Cart Quantity**:
  - HTTP Method: PUT
  - Endpoint: /api/cart/{bookId}
  - Request Body: { quantity }
  - Response: JSON with updated cart details
  - Authentication: Bearer token (JWT)
- **Remove from Cart**:
  - HTTP Method: DELETE
  - Endpoint: /api/cart/{bookId}
  - Response: JSON with updated cart details
  - Authentication: Bearer token (JWT)

#### Order Processing
- **Place Order**:
  - HTTP Method: POST
  - Endpoint: /api/order
  - Request Body: { shippingAddress, paymentMethod }
  - Response: JSON with order details
  - Authentication: Bearer token (JWT)
- **Get Order History**:
  - HTTP Method: GET
  - Endpoint: /api/orders
  - Response: JSON array of order objects
  - Authentication: Bearer token (JWT)

#### Admin Dashboard
- **Add Book**:
  - HTTP Method: POST
  - Endpoint: /api/admin/book
  - Request Body: { title, author, ISBN, genre, publicationYear, price, quantity, coverImageURL, description }
  - Response: JSON with book details
  - Authentication: Bearer token (JWT) with admin role
- **Update Book**:
  - HTTP Method: PUT
  - Endpoint: /api/admin/book/{bookId}
  - Request Body: { title, author, ISBN, genre, publicationYear, price, quantity, coverImageURL, description }
  - Response: JSON with updated book details
  - Authentication: Bearer token (JWT) with admin role
- **Delete Book**:
  - HTTP Method: DELETE
  - Endpoint: /api/admin/book/{bookId}
  - Response: JSON with message indicating book deletion
  - Authentication: Bearer token (JWT) with admin role
- **Get Orders**:
  - HTTP Method: GET
  - Endpoint: /api/admin/orders
  - Response: JSON array of order objects
  - Authentication: Bearer token (JWT) with admin role
- **Update Order Status**:
  - HTTP Method: PUT
  - Endpoint: /api/admin/order/{orderId}
  - Request Body: { status }
  - Response: JSON with updated order details
  - Authentication: Bearer token (JWT) with admin role

#### Security
- All API endpoints require authentication and authorization checks.
- Validate all user inputs to prevent SQL injection, XSS, and CSRF.
- Implement rate limiting for login and password reset endpoints.

#### Internationalization
- Support English and Spanish languages for API responses.
- Use i18n library for Node.js.

#### Review System
- **Create Review**:
  - HTTP Method: POST
  - Endpoint: /api/review
  - Request Body: { bookId, rating, reviewText }
  - Response: JSON with review details
  - Authentication: Bearer token (JWT)
- **Get Reviews**:
  - HTTP Method: GET
  - Endpoint: /api/reviews/{bookId}
  - Response: JSON array of review objects
  - Authentication: None

#### Wishlist
- **Add to Wishlist**:
  - HTTP Method: POST
  - Endpoint: /api/wishlist
  - Request Body: { bookId }
  - Response: JSON with wishlist details
  - Authentication: Bearer token (JWT)
- **Get Wishlist**:
  - HTTP Method: GET
  - Endpoint: /api/wishlist
  - Response: JSON array of book objects
  - Authentication: Bearer token (JWT)

#### Promotional Discounts
- **Create Discount**:
  - HTTP Method: POST
  - Endpoint: /api/admin/discount
  - Request Body: { bookId, discountPercentage, expirationDate }
  - Response: JSON with discount details
  - Authentication: Bearer token (JWT) with admin role
- **Get Discounts**:
  - HTTP Method: GET
  - Endpoint: /api/admin/discounts
  - Response: JSON array of discount objects
  - Authentication: Bearer token (JWT) with admin role

### Features
#### Functional Features
- User registration and login
- Book catalog with search and filter options
- Shopping cart with persistence across sessions
- Order processing with payment gateway integration
- Admin dashboard for managing books, orders, and users
- Review system for books
- Wishlist feature for users
- Promotional discounts for books

#### Non-Functional Features
- Security: authentication, authorization, input validation, rate limiting
- Performance: caching, optimized database queries, horizontal scaling
- Usability: user-friendly API, meaningful error messages, i18n support
- Maintainability: clean code, modular design, containerization

### Schema-Relevant Details
- **Users**:
  - id (primary key)
  - email (unique)
  - password (hashed)
  - firstName
  - lastName
  - phoneNumber
  - profilePictureURL
- **Books**:
  - id (primary key)
  - title
  - author
  - ISBN (unique)
  - genre
  - publicationYear
  - price
  - quantity
  - coverImageURL
  - description
- **Orders**:
  - id (primary key)
  - userId (foreign key)
  - orderDate
  - status
  - totalCost
  - shippingAddress
- **OrderItems**:
  - id (primary key)
  - orderId (foreign key)
  - bookId (foreign key)
  - quantity
- **Reviews**:
  - id (primary key)
  - userId (foreign key)
  - bookId (foreign key)
  - rating
  - reviewText
- **Wishlist**:
  - id (primary key)
  - userId (foreign key)
  - bookId (foreign key)
- **Discounts**:
  - id (primary key)
  - bookId (foreign key)
  - discountPercentage
  - expirationDate

Note: The schema design should consider relationships between entities, data types, and constraints to ensure data integrity and efficient querying.
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
        memory=memory
    )
    asyncio.run(developer.arun())