from flask import jsonify, request
import json
from datetime import datetime, timedelta

with open('colorado-14ers.json', 'r') as f:
    peaks = json.load(f)


# # Apply filters and sorting to API response
# def apply_filters(f):
#     def wrapper(*args, **kwargs):
#         d = f(*args, **kwargs)
#         print(d)
#         data = d.get_json()
#         to_delete = set()
#
#         # weather
#         precip = int(request.args.get('precip'))
#
#         tomorrow = (datetime.today() + timedelta(days=1)).isoformat()
#         tomorrow = tomorrow.split('T')[0]
#         for name, peak in data.items():
#             for period in peak['weather']:
#                 day = period['startTime'].split('T')[0]
#                 if day == tomorrow and period['isDaytime']:
#                     print(period['probabilityOfPrecipitation']['value'])
#                     if period['probabilityOfPrecipitation']['value'] is None:
#                         pass
#                     elif period['probabilityOfPrecipitation']['value'] >= precip:
#                         to_delete.add(name)
#
#         # class
#         cls = int(request.args.get('class'))
#         if cls is not None:
#             for name, peak in data.items():
#                 if peak['class'] != cls:
#                     to_delete.add(name)
#
#         # range
#         rng = request.args.get('range')
#         if rng is not None:
#             for name, peak in data.items():
#                 if peak['range'] != rng:
#                     to_delete.add(name)
#
#         # delete
#         for name in to_delete:
#             del data[name]
#
#         # ordering
#         ordering = request.args.get('ordering')
#         if ordering is None:
#             ordering = 'rank'
#
#         # limit
#         start = 0
#         limit = request.args.get('limit')
#         if limit:
#             limit = int(limit)
#             if limit < 0:
#                 start = limit
#                 limit = None
#
#         sorted_peaks = sorted(data.values(), key=lambda x: x[ordering])[start:limit]
#
#         return jsonify(sorted_peaks)
#
#     return wrapper


def apply_filters(peaks):
    data = peaks.copy()

    to_delete = set()

    # weather
    precip = int(request.args.get('precip', 100))

    tomorrow = (datetime.today() + timedelta(days=1)).isoformat()
    tomorrow = tomorrow.split('T')[0]
    for name, peak in data.items():
        for period in peak['weather']:
            day = period['startTime'].split('T')[0]
            if day == tomorrow and period['isDaytime']:
                if period['probabilityOfPrecipitation']['value'] is None:
                    pass
                elif period['probabilityOfPrecipitation']['value'] > precip:
                    to_delete.add(name)

    # class
    cls = request.args.get('class')
    if cls is not None:
        cls = int(cls)
        for name, peak in data.items():
            if peak['class'] != cls:
                to_delete.add(name)

    # range
    rng = request.args.get('range')
    if rng is not None:
        for name, peak in data.items():
            if peak['range'] != rng:
                to_delete.add(name)

    # delete
    for name in to_delete:
        del data[name]

    # ordering
    ordering = request.args.get('ordering')
    if ordering is None:
        ordering = 'rank'

    # limit
    start = 0
    limit = request.args.get('limit')
    if limit:
        limit = int(limit)
        if limit < 0:
            start = limit
            limit = None

    sorted_peaks = sorted(data.values(), key=lambda x: x[ordering])[start:limit]

    return sorted_peaks
