"""
golf_consumer.py

Consume json messages from a Kafka topic and visualize golf scores in real-time.

"""

import matplotlib.pyplot as plt
from kafka import KafkaConsumer
import json
import numpy as np

# Define Kafka consumer
consumer = KafkaConsumer(
    "golf-updates",
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

plt.ion()
fig, ax = plt.subplots(figsize=(6, 4))

# Hole labels for x-axis
holes = [f"Hole {i+1}" for i in range(18)]

lines = {}
relative_score_texts = {}

# Set up the plot
ax.set_title("Hole-by-Hole Golf Scores")
ax.set_xlabel("Hole Number")
ax.set_ylabel("Score")
ax.set_xticks(np.arange(18))
ax.set_xticklabels(holes, rotation=45)
ax.set_ylim(0, 8)

round_number = 1
total_holes_played = 0
holes_per_round = 18
total_holes_in_tournament = 72

print("Starting Golf Consumer...")

# Horizontal offset function to shift text to the left or right to avoid overlap
def get_horizontal_offset(golfer, x_position, score, current_texts):
    offset = 0
    for other_golfer, other_text in current_texts.items():
        other_x = other_text.get_position()[0]
        other_score = lines[other_golfer].get_ydata()[-1]

        # If the scores are identical, apply a horizontal offset
        if abs(score - other_score) < 0.1 and abs(x_position - other_x) < 0.6:
            offset = 1
    return offset

for message in consumer:
    data = message.value

    # For each golfer, plot their hole-by-hole performance
    for golfer, golfer_data in data.items():
        scores = list(golfer_data['scores'].values())
        relative_score = golfer_data['relative_score']

        print(f"{golfer} - Relative Score: {relative_score:+d}")

        # Check if this golfer already has a line. If not, create one
        if golfer not in lines:
            lines[golfer] = ax.plot(holes, scores, label=golfer)[0]
        else:
            # Update the line with the new scores
            lines[golfer].set_ydata(scores)

        # If text already exists, remove it to avoid overlap
        if golfer in relative_score_texts:
            relative_score_texts[golfer].remove()

        # Horizontal position of the text (for the last hole)
        x_position = 17  # 17 corresponds to the last hole (Hole 18)

        # Get the dynamic horizontal offset based on nearby texts
        horizontal_offset = get_horizontal_offset(golfer, x_position, scores[-1], relative_score_texts)

        # Add relative score text at the end of the golfer's line with horizontal offset
        relative_score_texts[golfer] = ax.text(x_position + horizontal_offset, scores[-1], 
                                                f"{relative_score:+d}", color='black', fontsize=12, ha='center')

    # Update the round and tournament tracking
    total_holes_played += holes_per_round

    # Check if a new round needs to start (after 18 holes)
    if total_holes_played >= holes_per_round:
        round_number += 1
        total_holes_played = 0
        print(f"Round {round_number} has started!")

    # Check if a new tournament needs to start
    if total_holes_played >= total_holes_in_tournament:
        round_number = 1
        total_holes_played = 0
        print("New Tournament has started!")

        # Clear all relative score texts before a new round starts
        for text in relative_score_texts.values():
            text.remove()
        relative_score_texts.clear()

    ax.legend()
    plt.draw()
    plt.pause(0.1)

plt.show()
