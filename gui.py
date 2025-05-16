import tkinter as tk
from tkinter import messagebox
from library import Book, DigitalBook, DigitalLibrary, BookNotAvailableError, books_by_author

lib = DigitalLibrary()

class LibraryGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        self.title_label = tk.Label(root, text="Title")
        self.title_entry = tk.Entry(root)

        self.author_label = tk.Label(root, text="Author")
        self.author_entry = tk.Entry(root)

        self.isbn_label = tk.Label(root, text="ISBN")
        self.isbn_entry = tk.Entry(root)

        self.ebook_var = tk.IntVar()
        self.ebook_checkbox = tk.Checkbutton(root, text="eBook", variable=self.ebook_var, command=self.toggle_download_size)

        self.download_label = tk.Label(root, text="Download Size (MB)")
        self.download_entry = tk.Entry(root)
        self.download_entry.configure(state='disabled')

        self.add_button = tk.Button(root, text="Add Book", command=self.add_book)
        self.lend_button = tk.Button(root, text="Lend Book", command=self.lend_book)
        self.return_button = tk.Button(root, text="Return Book", command=self.return_book)
        self.remove_button = tk.Button(root, text="Remove Book", command=self.remove_book)

        self.author_search_label = tk.Label(root, text="Search by Author")
        self.author_search_entry = tk.Entry(root)
        self.search_button = tk.Button(root, text="Search", command=self.search_books_by_author)

        self.display_button = tk.Button(root, text="Show Available Books", command=self.show_books)
        self.output = tk.Text(root, height=15, width=70)

        self.layout()

    def layout(self):
        self.title_label.grid(row=0, column=0)
        self.title_entry.grid(row=0, column=1)
        self.author_label.grid(row=1, column=0)
        self.author_entry.grid(row=1, column=1)
        self.isbn_label.grid(row=2, column=0)
        self.isbn_entry.grid(row=2, column=1)

        self.ebook_checkbox.grid(row=3, column=0)
        self.download_label.grid(row=3, column=1)
        self.download_entry.grid(row=3, column=2)

        self.add_button.grid(row=4, column=0)
        self.lend_button.grid(row=4, column=1)
        self.return_button.grid(row=4, column=2)
        self.remove_button.grid(row=4, column=3)

        self.author_search_label.grid(row=5, column=0)
        self.author_search_entry.grid(row=5, column=1)
        self.search_button.grid(row=5, column=2)

        self.display_button.grid(row=6, column=0, columnspan=4)
        self.output.grid(row=7, column=0, columnspan=4)

    def toggle_download_size(self):
        if self.ebook_var.get():
            self.download_entry.configure(state='normal')
        else:
            self.download_entry.configure(state='disabled')
            self.download_entry.delete(0, tk.END)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        isbn = self.isbn_entry.get()
        if self.ebook_var.get():
            try:
                size = float(self.download_entry.get())
                book = DigitalBook(title, author, isbn, size)
                lib.add_digital_book(book)
            except ValueError:
                messagebox.showerror("Invalid Input", "Download size must be a number")
                return
        else:
            book = Book(title, author, isbn)
            lib.add_book(book)
        self.output.insert(tk.END, f"Book added: {book}\n")

    def lend_book(self):
        isbn = self.isbn_entry.get()
        try:
            book = lib.lend_book(isbn)
            self.output.insert(tk.END, f"Book lent: {book}\n")
        except BookNotAvailableError as e:
            messagebox.showerror("Error", str(e))

    def return_book(self):
        isbn = self.isbn_entry.get()
        lib.return_book(isbn)
        self.output.insert(tk.END, f"Book returned: ISBN {isbn}\n")

    def remove_book(self):
        isbn = self.isbn_entry.get()
        lib.remove_book(isbn)
        self.output.insert(tk.END, f"Book removed: ISBN {isbn}\n")

    def show_books(self):
        self.output.insert(tk.END, "\nAvailable Books:\n")
        for book in lib:
            self.output.insert(tk.END, str(book) + "\n")

    def search_books_by_author(self):
        author = self.author_search_entry.get()
        self.output.insert(tk.END, f"\nBooks by {author}:\n")
        for book in books_by_author(lib, author):
            self.output.insert(tk.END, str(book) + "\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()