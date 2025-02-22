# buzzline-06-rueckert

## Golf Round Live Tracker

Author: Trent Rueckert
Date: 2/21/2025

## Overview
This repository contains a real-time golf round tracker, where a Kafka producer generates random golf round scores and stores them in dictionaries to be logged in the log folder. A Kafka consumer reads from the database and generates a line chart depicting the hole-by-hole scores of 4 golfers.

## Project Setup
### 1️. Create and Activate Virtual Environment
Before running the scripts, set up a virtual environment:
```powershell
# Create virtual environment
py -m venv .venv

# Activate virtual environment (Windows)
venv\Scripts\activate
```

### Install Required Dependencies
Ensure all necessary libraries are installed:
```powershell
pip install -r requirements.txt
```

## Running the Producer/Consumer
### Start the Producer
Run the producer to generate the hole-by-hole and total round scores.
```powershell
py -m producers.golf_producer
```
This generates a new round (18 holes) of golf scores every 5 seconds

### Start the Consumer
Run the consumer to gather the hole/round/tournament scores and create the line chart.
```powershell
py -m consumers.golf_consumer
```
This script:
- Creates the line chart with all of the golfers' scores.
- Offsets the relative golf scores if the golfers finish the 18th hole with the same score to avoid overlap.

---
## Visualization

![alt text](<"C:\Users\trent\OneDrive\Documents\Screenshot 2025-02-21 Golfers.png">)

