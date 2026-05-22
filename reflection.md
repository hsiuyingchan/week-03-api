## Week 3 Reflection

1. What was the most confusing thing about Python compared to JavaScript?
   Indentation matters in Python. A small space mistake breaks the program, unlike JavaScript with curly braces. Also, the "self" parameter in classes was new.

2. What does an HTTP status code tell you? Give one example.
   Status codes tell if the request succeeded or failed. For example, 404 means "not found" — we used it when a book ID doesn't exist.

3. What was the difference between a path parameter and a query parameter?
   Path parameters identify a resource: /books/1 gets book #1. Query parameters filter: /books?status=reading filters by status.

4. What would happen to all the data if you restarted the server right now? Why is that a problem, and what will we use to fix it?
   All data would be lost because it's stored in memory. When the server restarts, the data disappears. We need a database to save data permanently on disk.
