from kafka import KafkaProducer
import json
import time
import random
from utils.utils_logger import logger  # Import the existing logger

# Sample golfers
golfers = ["Xander Schauffele", "Scottie Scheffler", "Rory McIlroy", "Ludvig Aberg"]

# Par values for 18 holes
par_values = [4, 3, 4, 5, 4, 3, 4, 5, 4, 3, 4, 4, 5, 4, 3, 5, 4, 4]

# Number of holes per round and total holes per tournament
holes_per_round = 18
total_holes_in_tournament = 72

# Track rounds and total holes played
total_holes_played = 0
round_number = 1

# Kafka producer setup function
def create_kafka_producer():
    """
    Create and return a Kafka producer.
    """
    kafka_server = 'localhost:9092'  # Replace with your Kafka server details
    try:
        producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        logger.info(f"Kafka producer connected to {kafka_server}")
        return producer
    except Exception as e:
        logger.error(f"Kafka connection failed: {e}")
        return None

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

# Function to start a new round (reset scores for all golfers)
def start_new_round():
    global round_number
    global total_holes_played

    logger.info(f"Starting Round {round_number}...")
    round_number += 1
    total_holes_played = 0

# Function to start a new tournament
def start_new_tournament():
    global round_number
    global total_holes_played

    logger.info("Starting New Tournament...")
    round_number = 1
    total_holes_played = 0

# Main Function to Stream Data
def stream_golf_scores():
    """
    Simulate golf score updates and stream to Kafka.
    """

    global total_holes_played

    logger.info("START golf score producer...")

    # Attempt to create Kafka producer
    producer = create_kafka_producer()
    if not producer:
        logger.error("Failed to create Kafka producer, exiting...")
        return

    try:
        while True:
            # Generate the golf score updates
            update = generate_hole_update()
            logger.info(f"Streaming golf scores: {update}")

            # Send to Kafka topic "golf-updates"
            producer.send("golf-updates", value=update)
            logger.info(f"Sent golf score data to Kafka topic 'golf-updates': {update}")

            total_holes_played += holes_per_round

            # Check if 18 holes are completed for the current round
            if total_holes_played >= holes_per_round:
                start_new_round()
            
            # Check if 72 holes are completed for the tournament
            if total_holes_played >= total_holes_in_tournament:
                start_new_tournament()

            time.sleep(5)

    except KeyboardInterrupt:
        logger.warning("Producer interrupted by user.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        if producer:
            producer.close()
            logger.info("Kafka producer closed.")
        logger.info("Producer shutting down.")

# Conditional Execution
if __name__ == "__main__":
    stream_golf_scores()