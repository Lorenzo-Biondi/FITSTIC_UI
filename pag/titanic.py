import streamlit as st
import joblib
import pandas as pd

def load_model():
    """Load the trained Titanic survival prediction model."""
    try:
        return joblib.load("Titanic.pkl")
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None

def setup_page():
    
    st.title("🚢 Titanic Survival Predictor")
    st.markdown("""
    This app predicts passenger survival on the Titanic based on historical data.
    Enter the passenger information below to get a prediction.
    """)

def get_passenger_input():
    """Collect passenger information based on the exact model features."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Passenger Information")
        
        pclass = st.selectbox(
            "Passenger Class",
            options=[1, 2, 3],
            help="1st = Upper Class, 2nd = Middle Class, 3rd = Lower Class"
        )
        
        sex = st.radio(
            "Sex",
            options=["male", "female"],
            horizontal=True
        )
        
        age = st.number_input(
            "Age",
            min_value=0,
            max_value=100,
            value=30,
            step=1,
            help="Age in years"
        )
        
        embarked = st.selectbox(
            "Port of Embarkation",
            options=["C", "Q", "S"],
            format_func=lambda x: {
                "C": "Cherbourg",
                "Q": "Queenstown",
                "S": "Southampton"
            }[x],
            help="Port where passenger boarded the Titanic"
        )
    
    with col2:
        st.subheader("Family Information & Fare")
        
        sibsp = st.number_input(
            "Number of Siblings/Spouses Aboard",
            min_value=0,
            max_value=8,
            value=0,
            help="Number of siblings or spouses traveling with the passenger"
        )
        
        parch = st.number_input(
            "Number of Parents/Children Aboard",
            min_value=0,
            max_value=6,
            value=0,
            help="Number of parents or children traveling with the passenger"
        )
        
        fare = st.slider(
            "Ticket Fare (in £)",
            min_value=0.0,
            max_value=600.0,
            value=32.0,
            step=0.5,
            help="Ticket fare in pounds (£)"
        )

    # Create feature dictionary exactly matching model features
    features = {
        'Pclass': pclass,
        'Sex': sex,
        'Age': age,
        'SibSp': sibsp,
        'Parch': parch,
        'Fare': fare,
        'Embarked': embarked
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

def display_results(prediction, probability, input_data):
    """Display the prediction results with context."""
    st.markdown("---")
    st.subheader("Prediction Results")
    
    if prediction is not None:
        survival_probability = probability[1] * 100
        
        # Create columns for the prediction display
        col1, col2 = st.columns(2)
        
        with col1:
            if prediction == 1:
                st.success("### Predicted: SURVIVED")
            else:
                st.error("### Predicted: DID NOT SURVIVE")
                
        with col2:
            st.metric(
                label="Survival Probability",
                value=f"{survival_probability:.1f}%"
            )
        
        # Display feature importance analysis
        st.markdown("### Key Factors Analysis")
        
        factors = []
        
        # Analyze passenger class
        class_risk = {
            1: "Higher chance of survival in 1st class",
            2: "Moderate chance of survival in 2nd class",
            3: "Lower chance of survival in 3rd class"
        }
        factors.append(class_risk[input_data['Pclass']])
        
        # Analyze gender
        if input_data['Sex'] == 'female':
            factors.append("Being female significantly increased survival chances")
        else:
            factors.append("Being male significantly decreased survival chances")
        
        # Analyze age
        if input_data['Age'] < 18:
            factors.append("Children had better survival chances")
        
        # Analyze family size
        total_family = input_data['SibSp'] + input_data['Parch']
        if total_family == 0:
            factors.append("Traveling alone affected survival chances")
        elif total_family > 4:
            factors.append("Large family groups had more difficulty staying together")
        
        # Display analysis
        for factor in factors:
            st.markdown(f"- {factor}")
        
        # Display input summary
        st.markdown("### Passenger Summary")
        summary_col1, summary_col2 = st.columns(2)
        
        with summary_col1:
            st.markdown(f"""
            - Class: {input_data['Pclass']}
            - Gender: {input_data['Sex'].title()}
            - Age: {input_data['Age']} years
            - Port: {input_data['Embarked']}
            """)
        
        with summary_col2:
            st.markdown(f"""
            - Family members aboard: {total_family}
            - Ticket fare: £{input_data['Fare']:.2f}
            """)

def main():
    """Main function to run the Streamlit app."""
    setup_page()
    
    model = load_model()
    if not model:
        return
    
    with st.expander("ℹ️ How to Use", expanded=False):
        st.markdown("""
        1. Enter passenger information in all fields
        2. Click 'Predict Survival' to see results
        3. Review the analysis of survival factors
        
        Note: All fields are required for accurate prediction.
        """)
    
    input_data = get_passenger_input()
    
    if st.button("🔍 Predict Survival", type="primary"):
        with st.spinner("Analyzing passenger data..."):
            prediction, probability = make_prediction(model, input_data)
            display_results(prediction, probability, input_data)
    
    st.sidebar.markdown("""
    ### About the Features
    
    - **Passenger Class (Pclass)**: 1st, 2nd, or 3rd class
    - **Sex**: Male or Female
    - **Age**: Age in years
    - **SibSp**: Number of siblings/spouses aboard
    - **Parch**: Number of parents/children aboard
    - **Fare**: Passenger fare in pounds
    - **Embarked**: Port of Embarkation
        - C = Cherbourg
        - Q = Queenstown
        - S = Southampton
    """)

if __name__ == "__main__":
    main()