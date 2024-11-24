import streamlit as st
import joblib
import pandas as pd

def load_model():
    """Load the trained diabetes prediction model."""
    try:
        return joblib.load("model_el.pkl")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def setup_page():
    """Configure the Streamlit page with title and description."""
    st.set_page_config(
        page_title="Diabetes Risk Predictor",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("🏥 Diabetes Risk Predictor")
    st.markdown("""
    This application estimates diabetes risk based on various health metrics. 
    The model is trained on the Pima Indians Diabetes Dataset from the National Institute of 
    Diabetes and Digestive and Kidney Diseases.
    
    ⚕️ **Note**: This tool is for educational purposes only and should not replace professional medical advice.
    """)

def get_patient_input():
    """Collect patient health metrics."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Basic Health Metrics")
        
        pregnancies = st.number_input(
            "Number of Pregnancies",
            min_value=0,
            max_value=20,
            value=0,
            help="Number of times pregnant"
        )
        
        glucose = st.slider(
            "Glucose Level (mg/dL)",
            min_value=0,
            max_value=200,
            value=85,
            help="Plasma glucose concentration after 2 hours in an oral glucose tolerance test"
        )
        
        blood_pressure = st.slider(
            "Blood Pressure (mm Hg)",
            min_value=0,
            max_value=200,
            value=70,
            help="Diastolic blood pressure"
        )
        
        skin_thickness = st.slider(
            "Skin Thickness (mm)",
            min_value=0,
            max_value=100,
            value=20,
            help="Triceps skin fold thickness"
        )
    
    with col2:
        st.subheader("Additional Measurements")
        
        insulin = st.slider(
            "Insulin Level (mu U/ml)",
            min_value=0,
            max_value=846,
            value=79,
            help="2-Hour serum insulin"
        )
        
        bmi = st.number_input(
            "BMI",
            min_value=0.0,
            max_value=70.0,
            value=23.0,
            step=0.1,
            help="Body Mass Index"
        )
        
        diabetes_pedigree = st.number_input(
            "Diabetes Pedigree Function",
            min_value=0.0,
            max_value=2.5,
            value=0.32,
            step=0.01,
            help="Diabetes pedigree function (a function which scores likelihood of diabetes based on family history)"
        )
        
        age = st.number_input(
            "Age",
            min_value=0,
            max_value=120,
            value=30,
            step=1,
            help="Age in years"
        )

    features = {
        'Pregnancies': pregnancies,
        'Glucose': glucose,
        'BloodPressure': blood_pressure,
        'SkinThickness': skin_thickness,
        'Insulin': insulin,
        'BMI': bmi,
        'DiabetesPedigreeFunction': diabetes_pedigree,
        'Age': age
    }
    
    return features

def make_prediction(model, input_data):
    """Make a prediction using the loaded model."""
    try:
        df = pd.DataFrame([input_data])
        prediction = model.predict(df)
        probability = model.predict_proba(df)[0]
        return prediction[0], probability
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
        return None, None

def assess_risk_factors(input_data):
    """Assess risk factors based on medical guidelines."""
    risk_factors = []
    
    # Glucose assessment
    if input_data['Glucose'] >= 140:
        risk_factors.append("⚠️ High glucose level indicates increased risk")
    elif input_data['Glucose'] >= 100:
        risk_factors.append("⚠️ Borderline glucose level")
    
    # BMI assessment
    if input_data['BMI'] >= 30:
        risk_factors.append("⚠️ BMI indicates obesity (BMI ≥ 30)")
    elif input_data['BMI'] >= 25:
        risk_factors.append("⚠️ BMI indicates overweight (BMI 25-29.9)")
    
    # Blood Pressure assessment
    if input_data['BloodPressure'] >= 90:
        risk_factors.append("⚠️ Elevated blood pressure")
    
    # Age assessment
    if input_data['Age'] >= 45:
        risk_factors.append("⚠️ Age is a risk factor (≥ 45 years)")
    
    # Family history assessment (using diabetes pedigree function)
    if input_data['DiabetesPedigreeFunction'] >= 0.8:
        risk_factors.append("⚠️ Strong family history of diabetes")
    
    return risk_factors

def display_results(prediction, probability, input_data):
    """Display the prediction results with medical context."""
    st.markdown("---")
    st.subheader("Risk Assessment Results")
    
    if prediction is not None:
        risk_probability = probability[1] * 100
        
        # Create columns for the prediction display
        col1, col2 = st.columns(2)
        
        with col1:
            if prediction == 1:
                st.error("### Higher Risk of Diabetes")
            else:
                st.success("### Lower Risk of Diabetes")
        
        with col2:
            st.metric(
                label="Risk Probability",
                value=f"{risk_probability:.1f}%"
            )
        
        # Display risk factors
        st.markdown("### Risk Factor Analysis")
        risk_factors = assess_risk_factors(input_data)
        
        if risk_factors:
            for factor in risk_factors:
                st.markdown(factor)
        else:
            st.markdown("✅ No major risk factors identified in the provided metrics")
        
        # Health recommendations
        st.markdown("### General Health Recommendations")
        st.info("""
        Remember these key factors for diabetes prevention:
        - Maintain a healthy weight
        - Exercise regularly (at least 150 minutes per week)
        - Eat a balanced diet rich in whole grains, lean proteins, and vegetables
        - Monitor blood glucose levels regularly if you're at risk
        - Get regular medical check-ups
        
        **Important**: This is a screening tool only. Please consult healthcare professionals for proper medical advice and diagnosis.
        """)

def main():
    """Main function to run the Streamlit app."""
    setup_page()
    
    model = load_model()
    if not model:
        return
    
    with st.expander("ℹ️ How to Use This Tool", expanded=False):
        st.markdown("""
        1. Enter your health metrics in all fields
        2. Click 'Analyze Risk' to see results
        3. Review the risk analysis and recommendations
        
        **Important Notes:**
        - All measurements should be taken after 8 hours of fasting
        - Glucose values are from a 2-hour oral glucose tolerance test
        - Consult your healthcare provider for proper medical advice
        """)
    
    input_data = get_patient_input()
    
    if st.button("🔍 Analyze Risk", type="primary"):
        with st.spinner("Analyzing health metrics..."):
            prediction, probability = make_prediction(model, input_data)
            display_results(prediction, probability, input_data)
    
    st.sidebar.markdown("""
    ### About This Tool
    
    This diabetes risk predictor uses the following metrics:
    
    - **Pregnancies**: Number of times pregnant
    - **Glucose**: Plasma glucose concentration (2 hours after glucose tolerance test)
    - **Blood Pressure**: Diastolic blood pressure (mm Hg)
    - **Skin Thickness**: Triceps skin fold thickness (mm)
    - **Insulin**: 2-Hour serum insulin (mu U/ml)
    - **BMI**: Body Mass Index
    - **Diabetes Pedigree**: A function scoring family history
    - **Age**: Age in years
    
    **Source**: National Institute of Diabetes and Digestive and Kidney Diseases
    
    **Disclaimer**: This tool is for educational purposes only and should not be used for medical diagnosis.
    """)

if __name__ == "__main__":
    main()