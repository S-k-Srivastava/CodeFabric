from uuid import uuid4
from modules.agents.graphs.nodejs_backend_developer import NodeJsBackendDeveloper
import asyncio
from modules.agents.memory.developer_memory import DeveloperMemory
from modules.logging.logger import setup_logger
setup_logger()

project_name = "todo_app"
project_description="""
Project Name : todo_app

Project Description : 

"Design a comprehensive authentication system integrated with a todo management application. Outline the **explicit data models**, their types, and all necessary API routes. Follow these specifications:

1. **Data Models**:  
   - **User Model**:  
     - `id` (Unique Identifier, type: UUID)  
     - `username` (String, unique, required)  
     - `email` (String, unique, required, validated format)  
     - `password` (String, required, hashed via bcrypt)  
     - `created_at` (DateTime, default: now)  
     - `updated_at` (DateTime, default: now)  

   - **Todo Model**:  
     - `id` (Unique Identifier, type: UUID)  
     - `user_id` (UUID, foreign key to User.id)  
     - `title` (String, required, max 100 chars)  
     - `description` (String, optional, max 500 chars)  
     - `status` (Enum: 'pending', 'in_progress', 'completed', default: 'pending')  
     - `due_date` (DateTime, optional)  
     - `created_at` (DateTime, default: now)  
     - `updated_at` (DateTime, default: now)  

   - **Task Model**:  
     - `id` (Unique Identifier, type: UUID)  
     - `todo_id` (UUID, foreign key to Todo.id)  
     - `title` (String, required, max 150 chars)  
     - `description` (String, optional, max 500 chars)  
     - `priority` (Enum: 'low', 'medium', 'high', default: 'medium')  
     - `status` (Enum: 'not_started', 'in_progress', 'done', default: 'not_started')  
     - `assigned_to` (UUID, foreign key to User.id, nullable)  
     - `due_date` (DateTime, optional)  
     - `created_at` (DateTime, default: now)  
     - `updated_at` (DateTime, default: now)  

2. **Authentication System**:  
   - Use JWT (JSON Web Tokens) for stateless authentication.  
   - Token refresh mechanism (optional but preferred).  
   - Password strength validation (min 8 chars, 1 uppercase, 1 symbol).  

3. **API Routes**:  
   - **User Routes**:  
     - `POST /api/auth/register`: Register a new user (email, username, password).  
       - Request Body: `{ username, email, password }`  
       - Response: `201 Created` with user data (exclude password).  

     - `POST /api/auth/login`: Log in (email/username + password).  
       - Request Body: `{ email_or_username, password }`  
       - Response: `200 OK` with JWT `access_token` and `refresh_token`.  

     - `POST /api/auth/logout`: Invalidate JWT token (requires auth).  
       - Response: `204 No Content`.  

     - `GET /api/auth/me`: Fetch current user data (requires auth).  
       - Response: `200 OK` with user details (exclude password).  

   - **Todo Routes** (all require JWT authentication):  
     - `GET /api/todos`: Fetch all todos for the logged-in user.  
       - Query Params: Filter by `status`, `due_date` (optional).  
       - Response: `200 OK` with array of todos.  

     - `POST /api/todos`: Create a new todo.  
       - Request Body: `{ title, description?, status?, due_date? }`  
       - Response: `201 Created` with created todo.  

     - `GET /api/todos/:id`: Fetch a specific todo by ID (user must own it).  
       - Response: `200 OK` with todo or `404 Not Found`.  

     - `PUT /api/todos/:id`: Update a todo (full update, user must own it).  
       - Request Body: `{ title?, description?, status?, due_date? }`  
       - Response: `200 OK` with updated todo.  

     - `DELETE /api/todos/:id`: Delete a todo (user must own it).  
       - Response: `204 No Content`.  

   - **Task Routes** (all require JWT authentication):  
     - `GET /api/todos/:todo_id/tasks`: Fetch all tasks under a specific todo.  
       - Query Params: Filter by `status`, `priority`, `assigned_to` (optional).  
       - Response: `200 OK` with array of tasks.  

     - `POST /api/todos/:todo_id/tasks`: Create a new task under a todo.  
       - Request Body: `{ title, description?, priority?, status?, assigned_to?, due_date? }`  
       - Response: `201 Created` with created task.  

     - `GET /api/tasks/:id`: Fetch a specific task by ID (user must own the parent todo).  
       - Response: `200 OK` with task or `404 Not Found`.  

     - `PUT /api/tasks/:id`: Update a task (full update, user must own the parent todo).  
       - Request Body: `{ title?, description?, priority?, status?, assigned_to?, due_date? }`  
       - Response: `200 OK` with updated task.  

     - `DELETE /api/tasks/:id`: Delete a task (user must own the parent todo).  
       - Response: `204 No Content`. 

      **Database**:
      Simply use json stored in local for CRUD operations. if json not exists then for first time it should create
      a new one for all there dbs (in db folder).

      Create .env for jwt secret  and  other stuffs (use any random secret key from your side).
---
"""

if __name__ == "__main__":
    process_id = "8baaf912-7a63-4696-af8a-f376a2b97a99"
    memory = DeveloperMemory(id=process_id)
    developer = NodeJsBackendDeveloper(
        id=process_id,
        project_name=project_name,
        project_description=project_description,
        memory=memory
    )
    asyncio.run(developer.arun())