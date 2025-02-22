from kafka import KafkaProducer
import json
import time
import random

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample golfers
golfers = ["Xander Schauffele", "Scottie Scheffler", "Rory McIlroy", "Ludvig Aberg"]

# Par values for 18 holes (not used in plot anymore, but needed for relative score calculation)
par_values = [4, 3, 4, 5, 4, 3, 4, 5, 4, 3, 4, 4, 5, 4, 3, 5, 4, 4]

# Number of holes per round and total holes per tournament
holes_per_round = 18
total_holes_in_tournament = 72

# Track rounds and total holes played
total_holes_played = 0
round_number = 1

# Generate random golf scores for 18 holes
def generate_hole_update():
    scores = {}
    
    for golfer in golfers:
        # Generate a list of scores for each hole (18 holes)
        golfer_scores = {f"hole_{i+1}": random.randint(2, 7) for i in range(18)}
        total_score = sum(golfer_scores.values())
        relative_score = total_score - sum(par_values)

        scores[golfer] = {
            "scores": golfer_scores,
            "relative_score": relative_score
        }
    
    return scores

# Function to start a new round
def start_new_round():
    global round_number
    global total_holes_played

    print(f"Starting Round {round_number}...")
    round_number += 1
    total_holes_played = 0

# Function to start a new tournament
def start_new_tournament():
    global round_number
    global total_holes_played

    print("Starting New Tournament...")
    round_number = 1
    total_holes_played = 0

if __name__ == "__main__":
    print("Starting Golf Producer...")
    
    while True:
        update = generate_hole_update()
        producer.send("golf-updates", update)
        print(f"Produced: {update}")
        
        total_holes_played += holes_per_round
        
        # Check if 18 holes are completed for the current round
        if total_holes_played >= holes_per_round:
            start_new_round()
        
        # Check if 72 holes are completed for the tournament
        if total_holes_played >= total_holes_in_tournament:
            start_new_tournament()
        
        time.sleep(5)

