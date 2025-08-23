# Honeywell Hackathon

This project provides an interactive interface for analyzing flight schedules.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
2. Start the application:
   ```bash
   streamlit run app.py
   ```

## Features
- Browse flights by origin and destination.
- Visualize busiest and least busy time slots.
- Query the data using natural-language prompts about the busiest or best times to fly.
- Tune a flight's departure time and view the congestion impact.
- Highlight flights with the highest frequency for cascading-impact analysis.
