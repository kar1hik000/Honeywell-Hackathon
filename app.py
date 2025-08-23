import pandas as pd
import streamlit as st
import spacy

@st.cache_data
def load_data():
    return pd.read_csv('Flight_Schedule_without_missing.csv')

def main():
    st.title("Intelligent Flight Scheduling")

    df = load_data()

    st.sidebar.header("Explore the Data")
    origin = st.sidebar.selectbox("Origin", sorted(df['origin'].dropna().unique()))
    dest = st.sidebar.selectbox("Destination", sorted(df['destination'].dropna().unique()))
    filtered = df[(df['origin'] == origin) & (df['destination'] == dest)]
    st.write(f"Flights from {origin} to {dest}")
    st.dataframe(filtered)

    st.header("Busiest time slots")
    df['hour'] = pd.to_datetime(df['scheduledDepartureTime'], errors='coerce').dt.hour
    counts = df.groupby('hour').size().reset_index(name='flights').dropna()
    st.bar_chart(counts.set_index('hour'))

    busiest = counts.sort_values('flights', ascending=False).iloc[0]
    least = counts.sort_values('flights', ascending=True).iloc[0]
    st.write(f"Busiest hour: {int(busiest['hour'])}:00 with {int(busiest['flights'])} flights")
    st.write(f"Least busy hour: {int(least['hour'])}:00 with {int(least['flights'])} flights")

    st.header("NLP Query")
    nlp = spacy.load('en_core_web_sm')
    question = st.text_input("Ask about flight schedule:")
    if question:
        doc = nlp(question.lower())
        if 'busiest' in question or 'busy' in question:
            st.write(f"The busiest hour is {int(busiest['hour'])}:00 with {int(busiest['flights'])} flights.")
        elif 'best' in question or 'least' in question:
            st.write(f"The best time to avoid congestion is {int(least['hour'])}:00 with {int(least['flights'])} flights.")
        else:
            st.write("Currently, I can answer questions about the busiest or best times.")

    st.header("Schedule tuner")
    flight = st.selectbox("Select flight number", sorted(df['flightNumber'].unique()))
    current_time = df[df['flightNumber'] == flight]['scheduledDepartureTime'].iloc[0]
    default_hour = pd.to_datetime(current_time, errors='coerce').hour or 0
    new_hour = st.slider("New departure time (hour)", 0, 23, default_hour)
    hourly_counts = counts.set_index('hour')['flights']
    st.line_chart(hourly_counts)
    st.write(f"If flight {flight} departs at {new_hour}:00, around {int(hourly_counts.get(new_hour, 0))} flights are scheduled in that hour.")

    st.header("Cascading impact")
    freq = df['flightNumber'].value_counts().head(5)
    st.write("Flights with highest frequency (potential cascading impact):")
    st.table(freq)

if __name__ == '__main__':
    main()
