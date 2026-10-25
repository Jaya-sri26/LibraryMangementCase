from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory database
library = {
    "books": [
        {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt", "available": True},
        {"id": 2, "title": "Clean Code", "author": "Robert C. Martin", "available": False},
        {"id": 3, "title": "DevOps Handbook", "author": "Gene Kim", "available": True},
    ]
}

@app.route("/")
def index():
    total = len(library["books"])
    available = sum(1 for b in library["books"] if b["available"])
    return render_template("index.html", total=total, available=available, borrowed=total - available)

@app.route("/books")
def view_books():
    return render_template("view_books.html", books=library["books"], title="All Books")

@app.route("/available")
def view_available():
    avail = [b for b in library["books"] if b["available"]]
    return render_template("view_books.html", books=avail, title="Available Books")

@app.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        if title and author:
            new_id = max([b["id"] for b in library["books"]], default=0) + 1
            library["books"].append({"id": new_id, "title": title, "author": author, "available": True})
        return redirect(url_for("view_books"))
    return render_template("add_book.html")

@app.route("/toggle/<int:book_id>", methods=["POST"])
def toggle_availability(book_id):
    for book in library["books"]:
        if book["id"] == book_id:
            book["available"] = not book["available"]
            break
    return redirect(request.referrer or url_for("view_books"))

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
