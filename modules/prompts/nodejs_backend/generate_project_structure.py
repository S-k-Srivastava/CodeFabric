prompt = """
You are an expert Node.js backend developer tasked with designing a project structure before development begins. Your goal is to create a list of files that form a professional, maintainable, and scalable architecture, adhering to SOLID principles (Single Responsibility, Open-Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion).

The files must be listed in the exact order of generation, ensuring that any file only depends on files created before it. For example, if there are five files—A, B, C, D, and E—then B can only depend on A, C can only depend on A and B, D can only depend on A, B, and C, and E can depend on A, B, C, and D. This enforces a clear dependency hierarchy and prevents circular dependencies.

Project Description:
{project_description}

Additional Instructions:
- Ensure each file has a clear purpose and aligns with SOLID principles.
- Also include the dependencies for each file i.e all other files path that each file depends on.
   Example :
   There  are 3 files A,B,C.
   If A is to be imported in B and used, then path of A must be added to dependencies of B.
   If B is to be imported in C and used, then path of B must be added to dependencies of C.
   so on...

- Keep the dependencies file paths accurate.

- Also list the file as per dependency order. Any file should not be listed before its dependency file.

- Include breif purpose for each file and how it should use dependencies.
- Use standard Nodejs Folder structure (e.g put everything in seperate folders in `src` and server.js in root).
- Use seperate model,repository,controller and Services and routes. Keep them in seperate folders in src.
- Create a Custom class for throwing Error and Custom Response class.
- You must include every file needed to run the backend app except `package,json`.
- Create .env if needed to store sensitive data.
- At the end include server.js.
- Use Capital Camel case for file naming.

Response Format:
{format}
"""
