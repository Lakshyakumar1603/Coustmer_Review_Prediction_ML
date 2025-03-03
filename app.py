from flask import Flask, render_template, request
import joblib
import mysql.connector

# Load the pre-trained model
model = joblib.load("logistic_regression.lb")

# Create a Flask app
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/application')  #server address
def application():
    return render_template('user_data.html')

@app.route('/userdata', methods=['GET', 'POST'])
def userdata():
    if request.method == 'POST':
        # Get data from the form and cast to int to avoid int64 error
        gender = int(request.form['gender'])
        customer_type = int(request.form['customer_type'])
        type_of_travel = int(request.form['typeoftravel'])
        flight_class = int(request.form['flight_class'])
        age = int(request.form['age'])
        flight_distance = int(request.form['flight_distance'])
        flght_enterment = int(request.form['flght_enterment'])
        bagage_handling = int(request.form['bagage_handling'])
        cleaning = int(request.form['cleaning'])
        deprtr_delay = int(request.form['deprtr_delay'])
        arival_delay = int(request.form['arival_delay'])

        # Establish connection to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="customer"
        )
        cursor = conn.cursor(buffered=True)

        # Initialize class variables based on flight class input
        Class_Eco = 0
        Class_Eco_Plus = 0
        if flight_class == 0:
            # Economy class
            Class_Eco = 1
        elif flight_class == 1:
            # Economy plus class
            Class_Eco_Plus = 1
        else:
            # Business class
            Class_Eco = 0
            Class_Eco_Plus = 0

        # Prepare data for prediction
        unseen_data_points = [[gender, customer_type, type_of_travel,
                               Class_Eco, Class_Eco_Plus, age, flight_distance, flght_enterment,
                               bagage_handling, cleaning, deprtr_delay, arival_delay]]

        # Get the model prediction
        output = model.predict(unseen_data_points)[0]

        # Prepare the data to be inserted into the database
        data = (int(gender), int(customer_type), int(type_of_travel), int(Class_Eco), int(Class_Eco_Plus), int(age), 
                int(flight_distance), int(flght_enterment), int(bagage_handling), int(cleaning), 
                int(deprtr_delay), int(arival_delay), int(output))

        # Insert data into the MySQL database
        cursor.execute("""
            INSERT INTO data (male, ct, totpt, ce, cep, age, fd, ie, bh, clean, ddim, adim, p)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, data)

        # Commit the transaction
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return f"Prediction result: {'Satisfied' if output == 1 else 'Not Satisfied'}"

@app.route('/dashboard')
def dashboard():
    # Establish connection to the MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="customer"
    )
    cursor = conn.cursor()

    # Fetch data from the database
    cursor.execute("SELECT COUNT(*) FROM data WHERE p = 1")  # count satisfied users
    satisfied_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM data WHERE p = 0")  # count unsatisfied users
    unsatisfied_count = cursor.fetchone()[0]

    # Close the database connection
    cursor.close()
    conn.close()

    # Render the dashboard page and pass data to the template
    return render_template('dashboard.html', satisfied_count=satisfied_count, unsatisfied_count=unsatisfied_count)

if __name__ == "__main__":
    app.run(debug=True)
