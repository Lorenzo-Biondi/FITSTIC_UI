import streamlit as st
import joblib as jbl
import pandas as pd

def somma(l1:float, l2:float):
    a = l1+l2
    return a

def main():

    def somma(l1:float, l2:float):
        a = l1+l2
        return a
    st.title('Pipeline streamlit')
    st.text('proviamo questo front-end')

    model = jbl.load(open('titanic_pipe.pkl'))

    Age= st.number_input('inserisci gli anni')
    Embarked = 'Q'
    Fare =7.8
    Parch = 0
    Pclass = 3
    Sex = 'female'
    SibSp = 0

    data = {
            "Pclass": [Pclass],
            "Sex": [Sex],
            "Age": [Age],
            "SibSp": [SibSp],
            "Parch": [Parch],
            "Fare": [Fare],
            "Embarked": [Embarked]
            }

    input_df = pd.DataFrame(data)
    res = model.predict(input_df).astype(int)[0]
    print(res)

    classes = {0:'died',
            1:'survived',
            }

    y_pred = classes[res]
    y_pred

    num1 = st.slider('Inserisci lato1 rettandolo',0,100,2)
    num2 = st.slider('Inserisci lato2 rettangolo',0,100,3)
    r = somma(num1,num2)
    if st.button('mostra risultato'):
        st.write('la somma è', r)
    

if __name__ == '__main__':
    main()