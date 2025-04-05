from uuid import uuid4
from modules.agents.graphs.nodejs_backend_developer import NodeJsBackendDeveloper
import asyncio
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.logging.logger import setup_logger
setup_logger()

project_name = "blogger"
project_description="""
I’m looking to have a **Node.js backend** developed for a web application using **MongoDB** as the database. Below is a complete and detailed project description. Please follow standard best practices and ensure the code is clean, modular, and well-documented.

---

### 🔧 **Tech Stack**
- **Backend Framework**: Node.js with Express.js
- **Database**: MongoDB (with Mongoose ODM)
- **Authentication**: JWT (JSON Web Tokens)
- **Password Handling**: bcrypt
- **Validation**: express-validator or Joi
- **Environment Configuration**: dotenv
- **API Documentation**: Swagger (optional but preferred)

---

### ✅ **Core Features**

#### 1. **Authentication & User Management**
- **Signup**  
  - Fields: name, email, password  
  - Password should be hashed before saving  
  - On successful signup, send a JWT token  

- **Login**  
  - Email & password validation  
  - On success, return JWT token  

- **Forgot Password**  
  - Accepts email, sends a reset link with token (can be mocked)  
  - Reset password endpoint using token  

- **Profile Info**  
  - Get user profile  
  - Update profile (name, email, password)

> Note: Protect routes using middleware that checks for valid JWT.

---

#### 2. **Blog Posts API**
- **Create Post**  
  - Fields: title, content, author (from auth), tags (optional), cover image (URL)  
  - Only authenticated users  

- **Get All Posts**  
  - Paginated response  
  - Optional filters: by author, by tag  

- **Get Single Post**  
  - Get post by ID  

- **Update Post**  
  - Only by post author  
  - Update title, content, tags, cover image  

- **Delete Post**  
  - Only by post author  

---

#### 3. **Comments**
- **Add Comment to Post**  
  - Only authenticated users  
  - Fields: postId, comment text  

- **Get Comments for Post**  
  - Paginated list of comments for a specific post  
  - Include commenter name and timestamp  

- **Delete Comment**  
  - Only by comment author or admin  

---

#### 4. **Likes**
- **Like/Unlike Post**  
  - Authenticated users can like or unlike a post  
  - Toggle-like functionality  
  - Prevent multiple likes by same user  

- **Get Like Count for Post**

---

### ⚙️ **Other Requirements**
- Use modular routing and controllers  
- Use services layer for logic separation (good architecture)  
- Error handling middleware  
- Use proper HTTP status codes and messages  
- Validation on inputs and request body  
- Store all timestamps (createdAt, updatedAt)
- Use MongoDB schema references (e.g., user ↔ posts, posts ↔ comments)

---

### 📁 Folder Structure (Suggested)
```
/project-root
  /controllers
  /routes
  /models
  /middlewares
  /services
  /utils
  .env
  server.js
```
"""

if __name__ == "__main__":
    process_id = project_name
    memory = DeveloperMemory(id=process_id)
    developer = NodeJsBackendDeveloper(
        id=process_id,
        project_name=project_name,
        project_description=project_description,
        memory=memory
    )
    asyncio.run(developer.arun())