from flask import Flask, render_template, request
import joblib
import numpy as np

app = Flask(__name__)

# Load model
try:
    model = joblib.load("lung_cancer_model1.pkl")
    print("Model loaded successfully")
except Exception as e:
    print("Model loading failed:", e)
    model = None


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():

    if model is None:
        return "Model not loaded"

    try:
        features = np.array([[
            int(request.form['GENDER']),
            float(request.form['AGE']),
            int(request.form['SMOKING']),
            int(request.form['YELLOW_FINGERS']),
            int(request.form['ANXIETY']),
            int(request.form['PEER_PRESSURE']),
            int(request.form['CHRONIC_DISEASE']),
            int(request.form['FATIGUE'])
        ]])

        prediction = model.predict(features)

        # SAFE probability handling
        proba = model.predict_proba(features)

        if len(proba[0]) > 1:
            risk_score = proba[0][1]
        else:
            risk_score = proba[0][0]

        if prediction[0] == 1:
            result = "⚠️ High Risk: Lung Cancer Detected"
        else:
            result = "✅ Low Risk: No Lung Cancer Detected"

        return render_template(
            "index.html",
            prediction_text=result,
            probability=risk_score
        )

    except Exception as e:
        return f"Error during prediction: {str(e)}"

     

if __name__ == "__main__":
    app.run(debug=True)

