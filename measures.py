import requests


def get_sensor_data(sensor_id, n=1):
    return requests.get(
        f'https://apigtw.vaisala.com/hackjunction2018/saunameasurements/latest?SensorID={sensor_id}&limit={n}'
    ).json()


def get_measurement(sensor_data, measurement='Temperature'):
    return sensor_data['Measurements'][measurement]['value']


def temp_stove():
    stove1 = get_measurement(get_sensor_data('Stove1')[0])
    stove2 = get_measurement(get_sensor_data('Stove2')[0])
    return (stove1 + stove2) / 2


def temp_inside():
    return get_measurement(get_sensor_data('Bench2')[0])


def oxygen():
    return get_measurement(get_sensor_data('Bench3')[0], 'Oxygen concentration')


def temp_outdoor():
    return get_measurement(get_sensor_data('Outdoor1')[0])


def highest_temperature():
    return max(map(get_measurement, get_sensor_data('Bench2', 1000)))


measurements = {
    'stove': temp_stove,
    'inside': temp_inside,
    'oxygen': oxygen,
    'outdoor': temp_outdoor,
    'highest_temperature': highest_temperature
}
