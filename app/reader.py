__author__ = 'chitrangadakaushik'

import csv
import bisect

labels = []


def get_shake_status(lo, hi):
    if lo == '1' and hi == '0':
        return 'NOT_SHAKING'
    elif lo == '0' and hi == '1':
        return 'SHAKING'
    elif lo is None or hi is None:
        # timestamp before the first recorded label or after the last recorded label
        return 'UNIDENTIFIED_STATUS'
    else: # some other unidentified value
        return 'UNIDENTIFIED_STATUS'


def read_data(sensor_file, label_file):
    with open(label_file, 'rb') as lbl_file:
        lbl = csv.reader(lbl_file, delimiter=',')
        lbl.next()  # skip the header
        for row in lbl:
            labels.append((int(row[0]), row[1]))

    timestamps = [label[0] for label in labels]

    data = dict()

    with open(sensor_file, 'rb') as sensor_file:
        sensor = csv.reader(sensor_file, delimiter=',')
        sensor.next()
        for row in sensor:
            ts = int(row[0])
            index = bisect.bisect(timestamps, ts)
            low = labels[index - 1][1] if index > 0 else None
            high = labels[index][1] if index < len(labels) else None
            data[int(row[0])] = dict(label=get_shake_status(low, high), acc_x=float(row[1]), acc_y=float(row[2]),
                                     acc_z=float(row[3]), roll=float(row[4]), pitch=float(row[5]), yaw=float(row[6]),
                                     av_x=float(row[7]), av_y=float(row[8]), av_z=float(row[9]))

    return data


def main():
    data = read_data('/Users/chitrangadakaushik/GitHub/shake-detection/data/p.sensor.csv',
                     '/Users/chitrangadakaushik/GitHub/shake-detection/data/p.lbl.csv')
    for ts in data:
        print ts, data[ts]

    print len(data)


if __name__ == '__main__':
    main()


