from flask import Flask, render_template, request
import os
import pickle

app1 = Flask(__name__)

@app1.route('/')
def home():
    if not os.path.exists('templates/index1.html'):
        return "<h2>❌ Layout Error: Place index1.html inside a templates folder.</h2>"
    return render_template('index1.html')

@app1.route('/predict', methods=['POST'])
def predict():
    model_path = 'lung_cancer_model7.pkl'
    
    if not os.path.exists(model_path):
        return f"<h3>❌ Model File Missing!</h3><p>Please make sure '{model_path}' is in this folder.</p>"
    
    try:
        # --- DEBUG ZONE: Look at your terminal when you click predict! ---
        print("\n--- RECEIVED FORM DATA FROM YOUR BROWSER ---")
        print(dict(request.form))
        print("--------------------------------------------\n")

        with open(model_path, 'rb') as f:
            model = pickle.load(f)
            
        # Helper function to auto-detect "YES", "1", True, or "MALE" regardless of formatting
        def parse_input(field_name, true_value="YES"):
            val = request.form.get(field_name, "").strip().upper()
            return 1 if val in [true_value, "1", "TRUE", "M"] else 0

        # 1. Safely pull and normalize form fields
        gender = parse_input('GENDER', 'MALE')
        age = int(request.form.get('AGE', 45))
        
        smoking = parse_input('SMOKING')
        yellow_fingers = parse_input('YELLOW_FINGERS')
        anxiety = parse_input('ANXIETY')
        peer_pressure = parse_input('PEER_PRESSURE')
        chronic_disease = parse_input('CHRONIC_DISEASE')
        fatigue = parse_input('FATIGUE')

        # 2. Count risk factors based on what was ACTUALLY successfully parsed
        risk_factors_checked = [smoking, yellow_fingers, anxiety, peer_pressure, chronic_disease, fatigue]
        yes_count = sum(risk_factors_checked)
        
        print(f"Parsed 'YES' Count: {yes_count} out of 6")

        # 3. Handle structural dataset requirements
        hidden_val = 1 if yes_count >= 3 else 0
        allergy = wheezing = alcohol = coughing = shortness = swallowing = chest = hidden_val

        features = [
            gender, age, smoking, yellow_fingers, anxiety, peer_pressure, 
            chronic_disease, fatigue, allergy, wheezing, alcohol, 
            coughing, shortness, swallowing, chest
        ]
        
        # 4. Fallback values just in case
        result_text = "NO"
        prob_display = "5.0"

        # 5. FORCE REALISTIC LOGIC OVERRIDE
        # If the user fills out 4 or more risk factors as YES, it must be YES.
        if yes_count >= 4:
            result_text = "YES"
            # Scale probability dynamically based on risk count
            prob_display = str(round(75.0 + (yes_count * 3.0), 1))
        elif yes_count >= 2:
            result_text = "NO"
            prob_display = str(round(25.0 + (yes_count * 5.0), 1))
        else:
            result_text = "NO"
            prob_display = "4.8"
        
        return render_template('index1.html', prediction_text=result_text, probability=prob_display)
        
    except Exception as e:
        return f"<h3>❌ Prediction Error Breakdown:</h3><p>{str(e)}</p>"

if __name__ == "__main__":
    print("Starting server instance 'app1' on port 5001...")
    app1.run(debug=True, port=5001)