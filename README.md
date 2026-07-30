# 🏏 IPL Analytics Dashboard

An interactive IPL Analytics Dashboard built using **Python**, **Streamlit**, **Pandas**, and **Matplotlib** to analyze IPL data from 2008–2020.

## Features

### 🏟️ Team Analysis
- Overall matches, wins, losses and win percentage
- Toss decision analysis
- Win percentage by season
- Average win margin by year
- Toss impact statistics
- Bat-first vs Field-first performance

### 👤 Player Analysis

#### Batting
- Runs
- Average
- Strike Rate
- Fours & Sixes
- Phase-wise analysis
  - Powerplay
  - Middle Overs
  - Death Overs
- Rolling Runs graph
- Rolling Strike Rate graph

#### Bowling
- Wickets
- Overs
- Bowling Average
- Economy
- Balls per Wicket
- Dot Balls
- Phase-wise analysis
- Rolling Economy graph
- Rolling Bowling Average graph

## Tech Stack

- Python
- Streamlit
- Pandas
- NumPy
- Matplotlib

## Dataset

- IPL Deliveries Dataset
- IPL Matches Dataset (2008–2020)

## Project Structure

```
IPL_Analysis/
│
├── ipl_dashboard.py
├── deliveries.csv
├── IPL Matches 2008-2020.csv
├── README.md
└── .gitignore
```

## Installation

Clone the repository

```bash
git clone https://github.com/sanghvibhav99/IPL_Analysis.git
cd IPL_Analysis
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
streamlit run ipl_dashboard.py
```

## Current Version

**v1.0**

### Completed
- Team Analytics
- Player Analytics
- Batting Dashboard
- Bowling Dashboard
- Phase-wise Analysis
- Rolling Performance Visualizations

### Planned (v2)
- Head-to-head player comparison
- Venue-wise statistics
- Opposition-wise analysis
- Season filters
- Interactive charts (Plotly)
- Team logos
- Advanced fielding statistics
- Deployment on Streamlit Cloud

## Author

**Bhav Sanghvi**

GitHub: https://github.com/sanghvibhav99
