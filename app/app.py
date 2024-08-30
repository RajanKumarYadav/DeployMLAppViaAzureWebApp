# Importing the Library
import pandas as pd
from flask import request, Flask, jsonify
import joblib

# Initialize Flask application
app = Flask(__name__)

# Load the model
model = joblib.load('model_diabetes_prediction.joblib')  # This can be your Model Registry/or any cloud location

@app.route('/diabetesPrediction', methods=['POST'])
def diabetesPrediction():
    try:
        data = request.json
        df = pd.DataFrame(data["data"])
        
        # Dataframe Creation
        df = df[['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']]
        
        # Ensure correct data types
        df.Pregnancies = df.Pregnancies.astype('int64')
        df.Glucose = df.Glucose.astype('int64')
        df.BloodPressure = df.BloodPressure.astype('int64')
        df.SkinThickness = df.SkinThickness.astype('int64')
        df.Insulin = df.Insulin.astype('int64')
        df.BMI = df.BMI.astype('float64')
        df.DiabetesPedigreeFunction = df.DiabetesPedigreeFunction.astype('float64')
        df.Age = df.Age.astype('int64')
        
        input_data = df.iloc[:,:]

        # Make prediction
        prediction_value = model.predict(input_data)

        # Map prediction values to messages
        if prediction_value[0] == 0:
            result_message = "Negative"
        elif prediction_value[0] == 1:
            result_message = "Positive"
        else:
            result_message = "Unknown"  # Handle unexpected values if necessary

        # Format the result into the desired structure
        formatted_result = {
            "Based on your test report, the diabetes result is:": result_message
        }

        return jsonify(formatted_result)

    except Exception as e:
        # Handle unexpected errors
        return jsonify({'error': str(e)}), 500

# Run the Flask application
if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=80)
