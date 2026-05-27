# Week 4 Reflection

## 1. What is the difference between the SQLAlchemy model and the Pydantic schema?

The **SQLAlchemy model** (Book in models.py) represents the actual **database table structure**. It defines columns, data types, constraints (like primary keys and nullable fields), and how data is stored permanently in PostgreSQL.

The **Pydantic schema** (BookCreate, BookUpdate, BookResponse in schemas.py) represents **API request/response validation**. It defines what data the API accepts from clients and what it returns. Pydantic schemas validate incoming data and automatically convert SQLAlchemy objects to JSON.

Think of it this way:
- **SQLAlchemy model** = database blueprint
- **Pydantic schema** = API contract with clients

## 2. What does `Depends(get_db)` do? Why does every endpoint need it?

`Depends(get_db)` is a FastAPI dependency injection mechanism. When you add it to an endpoint:

```python
def get_books(db: Session = Depends(get_db)):
```

FastAPI automatically calls the `get_db()` function before running the endpoint, which provides a fresh database session (`db`). This session is what you use to query the database.

**Why every endpoint needs it:**
- Each request needs its own database session (for isolation and thread-safety)
- `get_db()` automatically closes the session after the request completes
- Without it, you have no way to access the database in your endpoint

It's similar to opening and closing a connection each time you need to talk to the database.

## 3. When you restarted the server and your data was still there — how does that feel compared to storing data in a Python list? What changed architecturally?

**Before (Week 3 - in-memory list):**
- Data lived only in RAM
- Server restart = data gone
- Only one process could access it

**After (Week 4 - PostgreSQL database):**
- Data persists on disk permanently
- Server restart = data still there ✅
- Multiple processes can access the same data

**Architecturally:**
- Week 3: `Client ↔ FastAPI (in-memory list)`
- Week 4: `Client ↔ FastAPI ↔ PostgreSQL (disk)`

The database acts as a persistent data layer, making the app scalable and reliable. This is essential for real applications.

## 4. What was the most confusing part of connecting the frontend to the backend?

**CORS (Cross-Origin Resource Sharing)** was the key learning. Without adding the CORS middleware to FastAPI, the browser would block requests from the Next.js frontend (running on port 3000) to the backend (port 8000) because they're different origins.

The error would be silent in the frontend but browsers would block the request. Adding:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    ...
)
```

fixed it, allowing the frontend to make API calls to the backend.

## 5. When does CORS become a problem and why? In your own words.

CORS is a browser security feature that prevents websites from making requests to different domains/ports without permission.

**Why it exists:** Imagine you visit `malicious.com` — without CORS, that site could make requests to your bank's website on your behalf and steal your data.

**When it's a problem:**
- Frontend and backend on different origins (ports, domains)
- Browser blocks the request automatically
- You need the backend to explicitly allow it

In production, you'd set `allow_origins` to your actual domain (e.g., `["https://myapp.com"]`) instead of allowing everything.

## 6. What is the difference between useEffect with `[]` and without it?

**useEffect with `[]` (dependency array):**
```javascript
useEffect(() => {
  fetchBooks(); // runs ONCE on mount
}, []);
```
- Runs exactly **once** when the component mounts
- Perfect for fetching initial data
- `[]` tells React "no dependencies, don't re-run"

**useEffect without dependency array:**
```javascript
useEffect(() => {
  console.log("runs after EVERY render");
});
```
- Runs **after every render**
- Can cause infinite loops if you update state inside it
- Rarely what you want

**In the books list:** We use `[]` because we only want to fetch books once when the page loads. Without it, we'd fetch every time the component re-renders (which is many times), hammering the API.
