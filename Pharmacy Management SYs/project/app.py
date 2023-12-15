

from flask import Flask, render_template, request, redirect, send_from_directory, url_for
import mysql.connector

app = Flask(__name__)

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Niraj@1531",
    database="pharmacy"
)


cursor = db.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS medicines (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        quantity INT,
        price DECIMAL(10, 2)
    )
""")


def add_medicine(name, quantity, price):
    cursor.execute("INSERT INTO medicines (name, quantity, price) VALUES (%s, %s, %s)", (name, quantity, price))
    db.commit()

def delete_medicine(name):
    cursor.execute("delete from medicines where name = %s ", (name,))
    db.commit()
# Function to view the inventory
def view_inventory():
    cursor.execute("SELECT * FROM medicines")
    medicines = cursor.fetchall()

    return medicines

# Function to sell a medicine
def sell_medicine(medicine_id, quantity_sold):
    cursor.execute("SELECT * FROM medicines WHERE id = %s", (medicine_id,))
    medicine = cursor.fetchone()

    if medicine:
        if medicine[2] >= quantity_sold:
            total_price = quantity_sold * medicine[3]
            cursor.execute("UPDATE medicines SET quantity = quantity - %s WHERE id = %s", (quantity_sold, medicine_id))
            db.commit()
            return f"Sold {quantity_sold} units of {medicine[1]} for Rs.{total_price:.2f}"
        else:
            return "Insufficient quantity in stock."
    else:
        return "Medicine not found in inventory."

# Menu-driven interface
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        add_medicine(name, quantity, price)
    return render_template('add.html')

@app.route('/delete/<string:name>', methods=['GET', 'POST'])
def delete(name):
    if request.method == 'POST':
        delete_medicine(name)
        return redirect(url_for('index'))  # Redirect to your main page after deletion
    return render_template('delete.html', name=name)




@app.route('/view')
def view():
    medicines = view_inventory()
    return render_template('view.html', medicines=medicines)


@app.route('/sell', methods=['GET', 'POST'])
def sell():
    if request.method == 'POST':
        medicine_id = int(request.form['medicine_id'])
        quantity_sold = int(request.form['quantity_sold'])
        message = sell_medicine(medicine_id, quantity_sold)
        return message
    medicines = view_inventory()
    return render_template('sell.html', medicines=medicines)


# Serve static files (CSS, images, etc.)
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('', filename)


if __name__ == '__main__':
    app.run(debug=True)
