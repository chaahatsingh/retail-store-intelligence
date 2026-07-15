from collections import defaultdict
from datetime import datetime


class CustomerMetrics:

    def __init__(self, events, store_id):
        self.events = [
            e for e in events
            if (
                e.get("store_id") == store_id
                or e.get("store_code") == store_id
            )
        ]

    def total_visitors(self):
        return sum(
            1
            for e in self.events
            if e.get("event_type") == "entry"
        )

    def peak_hour(self):

        hourly = defaultdict(int)

        for event in self.events:

            if event.get("event_type") != "entry":
                continue

            ts = datetime.fromisoformat(
                event["event_timestamp"]
            )

            hourly[ts.hour] += 1

        if not hourly:
            return None

        return max(hourly, key=hourly.get)

    def hourly_footfall(self):

        hourly = defaultdict(int)

        for event in self.events:

            if event.get("event_type") != "entry":
                continue

            ts = datetime.fromisoformat(
                event["event_timestamp"]
            )

            hourly[ts.hour] += 1

        return dict(sorted(hourly.items()))