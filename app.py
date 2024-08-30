from flask import Flask, request, render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__)
model = pickle.load(open("c1_flight_rf.pkl", "rb"))


@app.route("/")
@cross_origin()
def home():
    return render_template("home.html")


@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":

        # Source and Destination
        Source = request.form["Source"]
        Destination = request.form["Destination"]

        # Validation to check if Source and Destination are the same
        if Source == Destination:
            return render_template('home.html', prediction_text="Error: Source and Destination cannot be the same.")

        # Date_of_Journey
        date_dep = request.form["Dep_Time"]
        journey_day = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").day)
        journey_month = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").month)

        # Departure
        dep_hour = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").hour)
        dep_min = int(pd.to_datetime(date_dep, format="%Y-%m-%dT%H:%M").minute)

        # Arrival
        date_arr = request.form["Arrival_Time"]

        arrival_day = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").day)
        arrival_month = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").month)

        arrival_hour = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").hour)
        arrival_min = int(pd.to_datetime(date_arr, format="%Y-%m-%dT%H:%M").minute)

        # Calculate total duration in minutes considering the full date and time
        dep_total_minutes = journey_day * 24 * 60 + dep_hour * 60 + dep_min
        arr_total_minutes = arrival_day * 24 * 60 + arrival_hour * 60 + arrival_min

        # Calculate the difference in minutes
        duration_total_minutes = arr_total_minutes - dep_total_minutes

        # Handle invalid input cases
        if duration_total_minutes < 0:
            return render_template('home.html',
                                   prediction_text="Error: Arrival time must be later than departure time.")
        if duration_total_minutes == 0:
            return render_template('home.html',
                                   prediction_text="Error: Arrival time must not be the same as departure time.")

        # Convert the total duration in minutes back to hours and minutes
        Duration_hour = duration_total_minutes // 60
        Duration_mins = duration_total_minutes % 60

        # Total Stops
        Total_Stops = int(request.form["stops"])

        # Airline
        airline = request.form['airline']
        if airline == 'Jet Airways':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 1
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif airline == 'IndiGo':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 1
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif airline == 'Air India':
            Airline_AirIndia = 1
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif airline == 'Multiple carriers':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 1
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 0

        elif airline == 'SpiceJet':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 1
            Airline_Vistara = 0
            Airline_Other = 0

        elif airline == 'Vistara':
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 1
            Airline_Other = 0

        elif airline == 'GoAir':
            Airline_AirIndia = 0
            Airline_GoAir = 1
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0

        else:
            Airline_AirIndia = 0
            Airline_GoAir = 0
            Airline_IndiGo = 0
            Airline_JetAirways = 0
            Airline_MultipleCarriers = 0
            Airline_SpiceJet = 0
            Airline_Vistara = 0
            Airline_Other = 1

        # Source encoding
        if Source == 'Delhi':
            Source_Delhi = 1
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0

        elif Source == 'Kolkata':
            Source_Delhi = 0
            Source_Kolkata = 1
            Source_Mumbai = 0
            Source_Chennai = 0

        elif Source == 'Mumbai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 1
            Source_Chennai = 0

        elif Source == 'Chennai':
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 1

        else:
            Source_Delhi = 0
            Source_Kolkata = 0
            Source_Mumbai = 0
            Source_Chennai = 0

        # Destination encoding
        if Destination == 'Cochin':
            Destination_Cochin = 1
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        elif Destination == 'Delhi':
            Destination_Cochin = 0
            Destination_Delhi = 1
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        elif Destination == 'Hyderabad':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 1
            Destination_Kolkata = 0

        elif Destination == 'Kolkata':
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 1

        else:
            Destination_Cochin = 0
            Destination_Delhi = 0
            Destination_Hyderabad = 0
            Destination_Kolkata = 0

        prediction = model.predict([[
            Total_Stops,
            journey_day,
            journey_month,
            dep_hour,
            dep_min,
            arrival_hour,
            arrival_min,
            Duration_hour,
            Duration_mins,
            Airline_AirIndia,
            Airline_GoAir,
            Airline_IndiGo,
            Airline_JetAirways,
            Airline_MultipleCarriers,
            Airline_Other,
            Airline_SpiceJet,
            Airline_Vistara,
            Source_Chennai,
            Source_Kolkata,
            Source_Mumbai,
            Destination_Cochin,
            Destination_Delhi,
            Destination_Hyderabad,
            Destination_Kolkata,
        ]])

        output = round(prediction[0], 2)

        return render_template('home.html', prediction_text="Your Flight Ticket price is Rs. {}".format(output))

    return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True)
