import streamlit as st


def somma(l1:float, l2:float):
    a = l1+l2
    return a

def main():
    st.title('Area rettangolo')
    st.text('proviamo questo front-end')
    num1 = st.slider('Inserisci lato1 rettandolo',0,100,2)
    num2 = st.slider('Inserisci lato2 rettangolo',0,100,3)
    r = somma(num1,num2)
    if st.button('mostra risultato'):
        st.write('la somma è', r)

if __name__ == '__main__':
    main()