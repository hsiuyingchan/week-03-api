import requests
import json

BASE_URL = "http://localhost:8000"

def print_test(step, name, response, expected_check=None):
    """Print test results in a readable format"""
    status = "✅" if response.status_code < 400 else "❌"
    print(f"\n{status} Step {step}: {name}")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    if expected_check:
        print(f"   {expected_check}")

def run_tests():
    print("=" * 60)
    print("🧪 BOOK TRACKER API - AUTOMATED TEST SEQUENCE")
    print("=" * 60)

    # Step 1: GET /books - should return empty list
    print("\n--- STEP 1: GET /books (empty list) ---")
    response = requests.get(f"{BASE_URL}/books")
    print_test(1, "GET /books", response, "✓ Should be empty: []")

    # Step 2: POST /books - add "Dune"
    print("\n--- STEP 2: POST /books - Add 'Dune' ---")
    dune_data = {
        "title": "Dune",
        "author": "Frank Herbert",
        "status": "read",
        "rating": 5
    }
    response = requests.post(f"{BASE_URL}/books", json=dune_data)
    print_test(2, "POST /books (Dune)", response, "✓ Should return id: 1")
    dune_id = response.json()["id"]

    # Step 3: POST /books - add "1984"
    print("\n--- STEP 3: POST /books - Add '1984' ---")
    book1984_data = {
        "title": "1984",
        "author": "George Orwell",
        "status": "reading"
    }
    response = requests.post(f"{BASE_URL}/books", json=book1984_data)
    print_test(3, "POST /books (1984)", response, "✓ Should return id: 2")
    book1984_id = response.json()["id"]

    # Step 4: POST /books - add "Clean Code"
    print("\n--- STEP 4: POST /books - Add 'Clean Code' ---")
    clean_code_data = {
        "title": "Clean Code",
        "author": "Robert Martin",
        "status": "want_to_read"
    }
    response = requests.post(f"{BASE_URL}/books", json=clean_code_data)
    print_test(4, "POST /books (Clean Code)", response, "✓ Should return id: 3")
    clean_code_id = response.json()["id"]

    # Step 5: GET /books - should return all 3
    print("\n--- STEP 5: GET /books (all 3 books) ---")
    response = requests.get(f"{BASE_URL}/books")
    print_test(5, "GET /books", response, f"✓ Should have 3 books")

    # Step 6: GET /books?status=reading - filter
    print("\n--- STEP 6: GET /books?status=reading (filter) ---")
    response = requests.get(f"{BASE_URL}/books", params={"status": "reading"})
    print_test(6, "GET /books?status=reading", response, "✓ Should return only '1984'")

    # Step 7: GET /books/{book_id} - get Dune
    print("\n--- STEP 7: GET /books/1 (get Dune) ---")
    response = requests.get(f"{BASE_URL}/books/{dune_id}")
    print_test(7, f"GET /books/{dune_id}", response, "✓ Should return Dune")

    # Step 8: PUT /books/{book_id} - update 1984
    print("\n--- STEP 8: PUT /books/2 (update 1984) ---")
    update_data = {
        "status": "read",
        "rating": 4
    }
    response = requests.put(f"{BASE_URL}/books/{book1984_id}", json=update_data)
    print_test(8, f"PUT /books/{book1984_id}", response, "✓ Should show status='read', rating=4")

    # Step 9: GET /books/stats - statistics
    print("\n--- STEP 9: GET /books/stats (statistics) ---")
    response = requests.get(f"{BASE_URL}/books/stats")
    print_test(9, "GET /books/stats", response, "✓ Should show: total=3, reading=0, read=2, want_to_read=1, avg=4.5")

    # Step 10: DELETE /books/{book_id} - delete Clean Code
    print("\n--- STEP 10: DELETE /books/3 (delete Clean Code) ---")
    response = requests.delete(f"{BASE_URL}/books/{clean_code_id}")
    print_test(10, f"DELETE /books/{clean_code_id}", response, "✓ Should confirm deletion")

    # Step 11: GET /books - should have 2 books
    print("\n--- STEP 11: GET /books (2 books remaining) ---")
    response = requests.get(f"{BASE_URL}/books")
    final_books = response.json()
    print_test(11, "GET /books", response, f"✓ Should have only 2 books")

    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS COMPLETED!")
    print("=" * 60)
    print(f"\nFinal state: {len(final_books)} books in database")
    print(f"Remaining books: {[b['title'] for b in final_books]}")

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to server!")
        print("Make sure your server is running: uvicorn main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")
