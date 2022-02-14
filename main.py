import streamlit as st
import pandas as pd
import plotly.express as px
from modules import module as mod

# Drop-down menu options
death_causes = ('090  Accidentes de tráfico',
                '098  Suicidio y lesiones autoinfligidas',
                '092  Caídas accidentales',
                '093  Ahogamiento, sumersión y sofocación accidentales',
                '095  Envenenamiento accidental por psicofármacos y drogas de abuso',
                '099  Agresiones (homicidio)',
                '091  Otros accidentes de transporte',
                '101  Complicaciones de la atención médica y quirúrgica',
                '096  Otros envenenamientos accidentales',
                '094  Accidentes por fuego, humo y sustancias calientes')


# Data extraction function
def data_extract(path):
    deaths = pd.read_csv(path, sep=';', thousands='.')
    deaths['cause_code'] = deaths['Causa de muerte'].apply(mod.cause_code)
    deaths['cause_group'] = deaths['Causa de muerte'].apply(mod.cause_types)
    deaths['cause_name'] = deaths['Causa de muerte'].apply(mod.cause_name)
    return deaths

# Data transformation function
def data_transform(df, sel):
    group = ['Periodo','Sexo', 'Causa de muerte']
    dataset = mod.row_filter(df, 'Sexo', ['Hombres', 'Mujeres'])
    dataset = mod.row_filter(dataset, 'Edad', ['Todas las edades'])
    dataset = mod.row_filter(dataset, 'Causa de muerte', [sel])
    dataset = mod.groupby_sum(dataset, group)
    dataset = mod.pivot_table(dataset, ['Sexo'], 'Periodo')
    return dataset

# Data download function
@st.cache
def convert_df(df):
    return df.to_csv().encode('utf-8')

if __name__ == "__main__":
    path = st.sidebar.text_input('Ruta del dataset', './data/7947.csv')
    selector = st.sidebar.selectbox("Seleccione una causa de muerte", death_causes)
    data = data_extract(path)
    trans_data = data_transform(data, selector)
    fig = px.bar(trans_data, x="Periodo", y=["Hombres", "Mujeres"], barmode="group", height=500)
    fig.update_layout(xaxis_title="Año", yaxis_title="Número de muertes", legend_title="Sexo")
    fig.update_xaxes(dtick=1)
    csv = convert_df(trans_data)

    # We love streamlit
    st.sidebar.download_button(label="Download data as CSV", data=csv, file_name='plot_data.csv', mime='text/csv',)
    st.title("Histórico de muertes en España por causas externas")
    st.image("https://media.traveler.es/photos/613762b7ea50dbd37eaded5b/master/pass/196675.jpg")
    st.header("Dataset original")
    st.dataframe(data)
    #st.header("Dataset procesado")
    #st.dataframe(trans_data)
    #st.header("Gráfico de evolución")
    #st.plotly_chart(fig, use_container_width=True)
    st.balloons()