import requests
from datetime import datetime
import json
import matplotlib.pyplot as plt
import os

def main():
    headers = {"X-Api-Key": os.environ.get('API_KEY')}
    gateway_id = os.environ.get('GATEWAY_ID')
    start_date_int = int(datetime.fromisoformat(os.environ.get('START_DATE')).timestamp())
    end_date_int = int(datetime.fromisoformat(os.environ.get('END_DATE')).timestamp())

    response = requests.get(f"https://ivt-api.azitek.io/position_logs/{gateway_id}/{start_date_int}?timestamp_end={end_date_int}", headers=headers)
    gateway_positions = json.loads(response.content)

    beacon_data = dict()

    for beacon in gateway_positions:
        duration = beacon['last_seen_at'] - beacon['seen_at']

        if beacon['beacon_id'] not in beacon_data:
            beacon_data[beacon['beacon_id']] = {
                "occurrences": 0,
                "average_duration": 0
                }

        old_occurence_counter = beacon_data[beacon['beacon_id']]['occurrences']
        beacon_data[beacon['beacon_id']]['occurrences'] += 1
        beacon_data[beacon['beacon_id']]['average_duration'] = (beacon_data[beacon['beacon_id']]['average_duration'] * old_occurence_counter + duration) / (beacon_data[beacon['beacon_id']]['occurrences'])

    beacon_ids = list(beacon_data.keys())
    occurrences = [item['occurrences'] for item in beacon_data.values()]
    average_durations = [item['average_duration'] for item in beacon_data.values()]

    _, ax = plt.subplots(figsize=(15, 6))
    ax.bar(beacon_ids, occurrences, label='Ocorrências', color='blue')
    ax.set_xlabel('beacon_id')
    ax.set_ylabel('Ocorrências')
    ax.set_title('Ocorrências de beacon_id')
    ax.legend()

    ax2 = ax.twinx()
    ax2.plot(beacon_ids, average_durations, label='Duração Média', color='red', marker='o')
    ax2.set_ylabel('Duração Média')
    ax2.legend()

    for tick in ax.get_xticklabels():
        tick.set_rotation(45)

    plt.show()
        

if __name__ == "__main__":
    main()