 
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
import os

app = Flask(__name__)

# ---------------- DATABASE CONNECTION ----------------
def get_db_connection():
    return mysql.connector.connect(
        host=os.environ.get("MYSQLHOST"),
        user=os.environ.get("MYSQLUSER"),
        password=os.environ.get("MYSQLPASSWORD"),
        database=os.environ.get("MYSQLDATABASE"),
        port=int(os.environ.get("MYSQLPORT"))
    )
# Fetch all users
#.execute("SELECT * FROM user")   # use users if your table name is user

#rows = cursor.fetchall()

#print("Login Table Data:")
#print("------------------")

#for row in rows:
#    print(row)

@app.route("/")
def landing():
    return render_template("landing.html")


# ---------------- LOGIN PAGE ----------------
@app.route('/login')
def index():
    return render_template("login.html")

# ---------------- LOGIN LOGIC ----------------
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM user WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        if user['role'] == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('home'))
    else:
        return render_template("login.html", message="Invalid Username or Password")

# ---------------- HOME ----------------
@app.route('/home')
def home():
    return render_template("home.html")

# ---------------- BOOK PAGES ----------------
@app.route('/book')
def book():
    return render_template("book.html")
@app.route('/check_card', methods=['POST'])
def check_card():

    card_number = request.form['card_number']
    card_type = request.form['card_type']

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM card_holder
        WHERE card_number=%s AND card_type=%s
    """,(card_number, card_type))

    user = cursor.fetchone()

    if user:
        return redirect(url_for('users', card_number=card_number))
    else:
        return render_template("book.html", message="Invalid card details")

@app.route('/users/<card_number>')
def users(card_number):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM card_holder
        WHERE card_number=%s
    """,(card_number,))

    user = cursor.fetchone()

    if not user:
        cursor.close()
        conn.close()
        return redirect(url_for('book'))

    # 2️⃣ Get Stock Based On Card Type
    cursor.execute("""
        SELECT * FROM stock
        WHERE card_type=%s
    """, (user['card_type'],))

    items = cursor.fetchall()

    cursor.close()
    conn.close()

    
    return render_template("users.html", user=user, items=items)
    

# ---------------- STOCK PAGES ----------------
@app.route('/stock')
def stock():

    card_type = request.args.get('card_type')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if card_type:
        cursor.execute("SELECT * FROM stock WHERE card_type=%s", (card_type,))
    else:
        cursor.execute("SELECT * FROM stock")

    items = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("stock.html", items=items)

# ---------------- NOTICE PAGES ----------------

@app.route('/notice')
def notice():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM notices
        WHERE status='active'
        ORDER BY 
            CASE 
                WHEN type='shop' THEN 1
                WHEN type='government' THEN 2
            END,
            created_at DESC
    """)

    notices = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("notice.html", notices=notices)


#----------------- ABOUT PAGE ----------------
@app.route('/about')
def about():
    return render_template("about.html")



# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # -------- Members --------
    card_type = request.args.get("card_type")
    section = request.args.get("section")

    if card_type and card_type != "ALL":
       cursor.execute("SELECT * FROM card_holder WHERE card_type = %s", (card_type,))
    else:
       cursor.execute("SELECT * FROM card_holder")

    members = cursor.fetchall()
    total_customers = len(members)

    # -------- Stock --------
    cursor.execute("SELECT * FROM stock")
    stock = cursor.fetchall()
    total_stock = len(stock)

    # -------- Reports --------
    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    reports = cursor.fetchall()
    total_reports = len(reports)

   
    # -------- Bookings --------
    cursor.execute("""
        SELECT b.id,
           c.card_number,
           c.card_type,
           b.booking_date,
           b.booking_time,
           b.status
        FROM bookings b
        JOIN card_holder c ON b.card_holder_id = c.id
        ORDER BY b.created_at DESC
    """)
    bookings = cursor.fetchall()
    total_bookings = len(bookings)

    # -------- Chart Data --------
    cursor.execute("""
        SELECT card_type, COUNT(*) as total
        FROM card_holder
        GROUP BY card_type
    """)
    chart_data = cursor.fetchall()

    chart_labels = [row['card_type'] for row in chart_data]
    chart_values = [row['total'] for row in chart_data]

    # -------- Notices --------
    cursor.execute("""
    SELECT * FROM notices
    ORDER BY created_at DESC
    """)
    all_notices = cursor.fetchall()

   
    # -------- Activities --------
    cursor.execute("""
    SELECT * FROM activities
    ORDER BY created_at DESC
    LIMIT 10
    """)
    activities = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template(
        "admin.html",
        members=members,
        stock=stock,
        reports=reports,
        bookings=bookings,
        total_customers=total_customers,
        total_bookings=total_bookings,
        total_reports=total_reports,
        total_stock=total_stock,
        chart_labels=chart_labels,
        chart_values=chart_values,
        activities=activities,
        all_notices=all_notices
        
    )
# ---------------- ADD MEMBER ----------------
@app.route('/add_member', methods=['POST'])
def add_member():
    conn = get_db_connection()
    cursor = conn.cursor()

    gender = request.form['gender']

    if gender == "female":
        profile_image = "images/girl.jpg"
    else:
        profile_image = "images/boy.jpg"

    cursor.execute("""
        INSERT INTO card_holder
        (name, card_number, card_type, members, mobile, username, profile_image, gender)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        request.form['name'],
        request.form['card_number'],
        request.form['card_type'],
        request.form['members'],
        request.form['mobile'],
        request.form['username'],
        profile_image,
        gender
    ))
    name = request.form['name']

    cursor.execute(
    "INSERT INTO activities (message) VALUES (%s)",
    ("New member added: " + name,)
)

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='addMember'))

@app.route("/delete_member/<int:id>")
def delete_member(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM card_holder WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("admin", section='customers'))

@app.route("/edit_member/<int:id>", methods=["GET","POST"])
def edit_member(id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        name = request.form["name"]
        card_number = request.form["card_number"]
        card_type = request.form["card_type"]
        members = request.form["members"]
        mobile = request.form["mobile"]
        username = request.form["username"]

        cursor.execute("""
            UPDATE card_holder
            SET name=%s, card_number=%s, card_type=%s, members=%s, mobile=%s, username=%s
            WHERE id=%s
        """,(name,card_number,card_type,members,mobile,username,id))

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("admin", section='customers'))

    cursor.execute("SELECT * FROM card_holder WHERE id=%s",(id,))
    edit_member = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit.html", edit_member=edit_member)
# ---------------- REPORT ----------------
@app.route('/report')
def report():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reports ORDER BY created_at DESC")
    reports = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("report.html", reports=reports)

@app.route('/add_stock', methods=['POST'])
def add_stock():

    conn = get_db_connection()
    cursor = conn.cursor()

    item_name = request.form['item_name']
    card_type = request.form['card_type']
    fixed_qty = request.form['fixed_qty']
    price = request.form['price']
    available_qty = int(request.form['available_qty'])


    # auto set image based on item
    if item_name.lower() == "rice":
        image = "images/rice.jpg"
    elif item_name.lower() == "sugar":
        image = "images/sugar.jpg"
    elif item_name.lower() == "wheat":
        image = "images/wheat.jpg"
    elif item_name.lower() == "kerosene":
        image = "images/kerosene.jpg"
    else:
        image = "images/default.jpg"

    cursor.execute("""
        INSERT INTO stock (item_name, card_type, fixed_qty, price,available_qty  , image)
        VALUES (%s,%s,%s,%s,%s,%s)
    """,(item_name,card_type,fixed_qty,price,available_qty,image))
    cursor.execute(
    "INSERT INTO activities (message) VALUES (%s)",
    ("Stock updated: " + item_name,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='stock'))

@app.route('/delete_stock/<int:id>')
def delete_stock(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM stock WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('admin', section='stock'))

# ---------------- SAVE REPORT ----------------
@app.route('/save_report', methods=['POST'])
def save_report():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reports (title, description, name, card_number)
        VALUES (%s,%s,%s,%s)
    """, (
        request.form['title'],
        request.form['description'],
        request.form['name'],
        request.form['card_number']
    ))
    cursor.execute(
    "INSERT INTO activities (message) VALUES (%s)",
    ("New complaint from card no " + request.form['card_number'],))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('report'))

# ---------------- SAVE BOOKING ----------------
@app.route('/save_booking', methods=['POST'])
def save_booking():

    conn = get_db_connection()
    cursor = conn.cursor()

    card_holder_id = request.form['card_holder_id']
    booking_date = request.form['booking_date']
    booking_time = request.form['booking_time']
    card_type = request.form['card_type']
    card_number = request.form['card_number'] 

    cursor.execute("""
        INSERT INTO bookings (card_holder_id, card_type, booking_date, booking_time, total_amount, status)
        VALUES (%s,%s,%s,%s,%s,'Pending')
   """, (
       card_holder_id,
       card_type, 
       booking_date, 
       booking_time, 
       0
    ))
    cursor.execute(
    "INSERT INTO activities (message) VALUES (%s)",
    ("New booking from card no " + card_number,))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('users', card_number=card_number))

@app.route("/update_booking/<int:id>/<action>")
def update_booking(id, action):
    conn = get_db_connection()
    cursor = conn.cursor()

    if action == "approve":
        status = "Approved"
    else:
        status = "Rejected"

    cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (status, id))
    cursor.execute(
    "INSERT INTO activities (message) VALUES (%s)",
    ("Booking " + status + " (ID: " + str(id) + ")",))

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("admin", section='booking'))

# ---------------- SIGNUP ----------------
@app.route('/signup')
def signup():
    return render_template("signup.html")
@app.route('/signup_user', methods=['POST'])
def signup_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    username = request.form['username']
    password = request.form['password']

    cursor.execute("SELECT * FROM user WHERE username=%s", (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return render_template("signup.html", message="Username already exists")

    cursor.execute(
        "INSERT INTO user (username, password, role) VALUES (%s, %s, %s)",
        (username, password, "user")
    )

    conn.commit()
    cursor.close()
    conn.close()

    return render_template("login.html", message="Signup successful!")

# -------- Notices section --------
@app.route('/add_notice', methods=['POST'])
def add_notice():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notices (title, message, type, status)
        VALUES (%s, %s, %s, 'active')
    """, (
        request.form['title'],
        request.form['message'],
        request.form['type']
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='notice'))

@app.route('/activate_notice/<int:id>')
def activate_notice(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE notices SET status='active' WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='notice'))

@app.route('/deactivate_notice/<int:id>')
def deactivate_notice(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("UPDATE notices SET status='inactive' WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='notice'))

@app.route('/delete_notice/<int:id>')
def delete_notice(id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM notices WHERE id=%s", (id,))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for('admin', section='notice'))

if __name__ == "__main__":

    app.run(debug=True)
