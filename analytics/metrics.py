from collections import defaultdict
from datetime import datetime
from typing import Dict, List


class MetricsEngine:
    """
    Computes business metrics from generated customer events.
    """

    def __init__(self, events: List[dict]):
        self.events = events

    def total_visitors(self) -> int:
        """Total customers entering the store."""
        return len(
            [e for e in self.events if e.get("event_type") == "entry"]
        )

    def queue_abandonment_rate(self) -> float:
        completed = len(
            [e for e in self.events if e.get("event_type") == "queue_completed"]
        )

        abandoned = len(
            [e for e in self.events if e.get("event_type") == "queue_abandoned"]
        )

        total = completed + abandoned

        if total == 0:
            return 0.0

        return round((abandoned / total) * 100, 2)

    def average_queue_wait(self) -> float:
        waits = [
            e["wait_seconds"]
            for e in self.events
            if e.get("event_type") in ("queue_completed", "queue_abandoned")
        ]

        if not waits:
            return 0.0

        return round(sum(waits) / len(waits), 2)

    def zone_popularity(self) -> Dict[str, int]:
        zones = defaultdict(int)

        for event in self.events:
            if event.get("event_type") == "zone_entered":
                zones[event["zone_name"]] += 1

        return dict(sorted(zones.items(), key=lambda x: x[1], reverse=True))

    def peak_hour(self):
        hours = defaultdict(int)

        for event in self.events:
            if event.get("event_type") == "entry":
                ts = datetime.fromisoformat(event["event_timestamp"])
                hours[ts.hour] += 1

        if not hours:
            return None

        return max(hours, key=hours.get)