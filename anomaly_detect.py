# Launch every 5 seconds

import requests
from sender import answer_message

def find_anomalies(sensor_id, sensors_data, allowed_measurements, threshold=0.15):
    measurement_sum = {}
    measurement_count = {}
    for point in sensors_data[1:]:
        for measurement, value_data in point['Measurements'].items():
            if measurement not in allowed_measurements:
                continue
            value = value_data['value']
            measurement_sum[measurement] = measurement_sum.get(measurement, 0) + value
            measurement_count[measurement] = measurement_count.get(measurement, 0) + 1

    measurement_average = {}
    for measurement, count in measurement_count.items():
        total = measurement_sum[measurement]
        measurement_average[measurement] = total / count

    last_point = sensors_data[0]
    for measurement, value_data in last_point['Measurements'].items():
        if measurement not in allowed_measurements:
            continue
        value = value_data['value']
        average_value = measurement_average[measurement]
        diff = abs(1 - (value / average_value))
        print(sensor_id, measurement, value, average_value, diff, diff > threshold)
        if diff > threshold:
            return True

    return False

sensors = [
    {'id': 'Doorway1', 'threshold': 0.15, 'message_type': 'door_open',
         'allowed_measurements': ['Temperature']},
    {'id': 'Ceiling1', 'threshold': 0.15, 'message_type': 'temperature_change',
         'allowed_measurements': ['Temperature']},
    {'id': 'Bench1', 'threshold': 0.15, 'message_type': 'too_many_person',
         'allowed_measurements': ['Carbon Dioxide concentration']},
    {'id': 'Bench1', 'threshold': 0.03, 'message_type': 'new_person',
         'allowed_measurements': ['Carbon Dioxide concentration']},
]

for sensor in sensors:
    response = requests.get(
        'https://apigtw.vaisala.com/hackjunction2018/saunameasurements/latest?SensorID={}&limit=100'
        .format(sensor['id'])
    ).json()
    if find_anomalies(sensor['id'], response, sensor['allowed_measurements'], sensor['threshold']):
        answer_message(sensor['message_type'])
