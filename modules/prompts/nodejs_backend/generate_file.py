prompt = """
Given the following context from your project's vectorstore and the target file to generate, please create complete, production-ready JavaScript code for the specified file.

**ALLOWED NPM PACKAGES**:
{packages}

**CONTEXT**: 
{context}

**TASK**: 
Generate the complete implementation for this file: {file}
About the File : {documentation}
Path of file : `{path}`

**INSTRUCTIONS**:
1. Analyze the context which contains either:
   - Just the project description 
   - Project description plus previously generated files

2. Create a complete implementation of the requested file with proper:
   - ES6+ JavaScript syntax
   - Appropriate commenting
   - Consistent code style
   - Required imports/exports

3. ERROR HANDLING ARCHITECTURE:
   - Repository/Data Access Layer: Throw specific, detailed errors with meaningful messages
   - Service Layer: Catch repository errors, enrich context if needed, then re-throw 
   - Controller Layer: Catch all errors from service layer and translate to appropriate HTTP responses,This must only call service,
   do not write route code here.
   - DO NOT swallow errors in lower layers (repositories, services)
   - DO NOT handle HTTP responses anywhere except controllers
   - Along with throwing Custom Error , must log the complete original error using console.log 

4. Ensure compatibility with dependencies and other files visible in the context
   - Reuse existing patterns, naming conventions, and architectural decisions
   - Maintain consistent error class hierarchy if present
   - Follow the same import/export patterns

5. Include ALL necessary imports and dependencies that appear in previously generated files
   - If modules like Express, Mongoose, etc. were used in other files, use them consistently
   - Match the exact import syntax used in other files

6. Implement complete business logic, not placeholder stubs
   - Write full implementations of all methods, not just their signatures
   - Include proper validation, error handling, and edge cases

7.ENSURE Server.js only use routers,routers only called controller functions,controller functions only calls services functions,service must only
call repository functions and repository performs DB operations only (based on model).

**PROJECT DESCRIPTION**:
{project_description}

**RESPONSE FORMAT**: (DO NOT GENERATE ANY EXTRA TEXT, JUST CODE WRAPPED WITH BELOW SYNTAX.IF YOU DO YOU DIE)
```javascript
code goes here
```

Please precisely generate the complete code for {file} that would seamlessly integrate with the existing codebase shown in the context.
"""