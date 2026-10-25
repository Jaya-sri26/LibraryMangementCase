from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database
library = {
    "books": [
        {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "available": True, "borrower": None},
        {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "available": False, "borrower": "Rahul"},
        {"id": 3, "title": "DevOps Handbook", "author": "Gene Kim", "available": True, "borrower": None},
        {"id": 4, "title": "Python Crash Course", "author": "Eric Matthes", "available": False, "borrower": "Priya"},
        {"id": 5, "title": "Atomic Habits", "author": "James Clear", "available": True, "borrower": None},
    ]
}

@app.route("/")
def index():
    total = len(library["books"])
    available = sum(1 for b in library["books"] if b["available"])
    borrowed = total - available
    return render_template("index.html", total=total, available=available, borrowed=borrowed)

@app.route("/books")
def view_books():
    return render_template("view_books.html", books=library["books"], title="All Books")

@app.route("/available")
def view_available():
    avail_books = [b for b in library["books"] if b["available"]]
    return render_template("view_books.html", books=avail_books, title="Available Books")

@app.route("/borrowed")
def view_borrowed():
    borr_books = [b for b in library["books"] if not b["available"]]
    return render_template("view_books.html", books=borr_books, title="Borrowed Books")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        if title and author:
            new_id = max([b["id"] for b in library["books"]], default=0) + 1
            library["books"].append(
                {"id": new_id, "title": title, "author": author, "available": True, "borrower": None}
            )
        return redirect(url_for("view_books"))
    return render_template("add_book.html")

@app.route("/borrow/<int:book_id>", methods=["POST"])
def borrow_book(book_id):
    borrower_name = request.form.get("borrower_name")
    for book in library["books"]:
        if book["id"] == book_id:
            if borrower_name:
                book["available"] = False
                book["borrower"] = borrower_name
            break
    return redirect(url_for("view_books"))

@app.route("/return/<int:book_id>", methods=["POST"])
def return_book(book_id):
    for book in library["books"]:
        if book["id"] == book_id:
            book["available"] = True
            book["borrower"] = None
            break
    return redirect(url_for("view_books"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
