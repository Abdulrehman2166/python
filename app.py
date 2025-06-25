from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pyttsx3

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'


issued_books = []

available_books = [
    {'title': 'Harry Potter', 'author': 'J.K. Rowling'},
    {'title': 'Sherlock Holmes', 'author': 'Arthur Conan Doyle'},
    {'title': 'Lord of the Rings', 'author': 'J.R.R. Tolkien'},
    {'title': 'Hamlet', 'author': 'William Shakespeare'},
    {'title': 'Pride and Prejudice', 'author': 'Jane Austen'},
    {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
    {'title': '1984', 'author': 'George Orwell'},
]


students = [
    {'username': 'malkashujaat', 'password': 'malka123'},
    {'username': 'student', 'password': 'student123'}
]


librarian_credentials = {
    'email': 'admin@gmail.com',
    'password': 'admin123'
}


engine = pyttsx3.init()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        author = request.form.get('author').strip()
        user_name = request.form.get('user_name').strip()

        book_found = False
        for book in available_books:
            if book['title'] == title and book['author'] == author:
                available_books.remove(book)
                
                issued_books.append({'title': title, 'author': author, 'user_name': user_name})
                book_found = True
                flash('Book has been issued successfully!', 'success')
                
                break
        
        if not book_found:
            flash('Book is not available.', 'error')
        
        book_issued = book_found  
        return render_template('issuebook.html', available_books=available_books, book_issued=book_issued)

    return render_template('issuebook.html', available_books=available_books)

@app.route('/login_student', methods=['GET', 'POST'])
def login_student():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        student = next((s for s in students if s['username'] == username and s['password'] == password), None)
        
        if student:
            session['username'] = username
            session['role'] = 'student'
            flash('Logged in successfully!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials.', 'error')
       
    return render_template('loginstu.html')

@app.route('/login_librarian', methods=['GET', 'POST'])
def login_librarian():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email == librarian_credentials['email'] and password == librarian_credentials['password']:
            session['username'] = email
            session['role'] = 'librarian'
            flash('Logged in successfully!', 'success')
            return redirect(url_for('librarian_home'))
        else:
            flash('Invalid credentials.', 'error')
 
    return render_template('loginlib.html')

@app.route('/librarian_home')
def librarian_home():
    if 'role' in session and session['role'] == 'librarian':
        return render_template('librarian_home.html')
    else:
        flash('Access denied!', 'error')
        return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        if role == 'student':
            students.append({'username': username, 'password': password})
        elif role == 'librarian':
            librarian_credentials['email'] = username
            librarian_credentials['password'] = password
        
        flash('Successfully registered!', 'success')
        return redirect(url_for('login_student'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))  

@app.route('/read_summary')
def read_summary():
    return render_template('readsummary.html')

@app.route('/upload_summary', methods=['POST'])
def upload_summary():
    summary = request.form.get('summary')
    if summary:
        
        engine.say(summary)
        engine.runAndWait()
    return redirect(url_for('home'))

@app.route('/issued_books')
def issued_books_view():
    if 'role' in session and session['role'] == 'librarian':
        return render_template('issued_books.html', issued_books=issued_books)
    else:
        flash('Access denied!', 'error')
        return redirect(url_for('home'))

@app.route('/registered_students')
def registered_students_view():
    if 'role' in session and session['role'] == 'librarian':
        return render_template('registered_students.html', students=students)
    else:
        flash('Access denied!', 'error')
        return redirect(url_for('home'))

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if 'role' in session and session['role'] == 'librarian':
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            students.append({'username': username, 'password': password})
            flash('Student added successfully!', 'success')
            return redirect(url_for('registered_students_view'))
        return render_template('add_student.html')
    else:
        flash('Access denied!', 'error')
        return redirect(url_for('home'))

@app.route('/remove_student', methods=['POST'])
def remove_student():
    if 'role' in session and session['role'] == 'librarian':
        username = request.form.get('username')
        global students
        students = [s for s in students if s['username'] != username]
        flash('Student removed successfully!', 'success')
        return redirect(url_for('registered_students_view'))
    else:
        flash('Access denied!', 'error')
        return redirect(url_for('home'))

@app.route('/about')
def about():
    if 'role' in session and session['role'] == 'student':
        return render_template('aboutus.html')
    else:
        flash('Please login to access this page', 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)