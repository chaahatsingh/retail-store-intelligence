from collections import defaultdict


class BusinessMetrics:

    def __init__(self, events, sales_summary, store_id):
        self.events = [
            e
            for e in events
            if (
                e.get("store_id") == store_id
                or e.get("store_code") == store_id
            )
        ]

        self.sales = sales_summary

    def zone_popularity(self):
        zones = defaultdict(int)

        for event in self.events:
            if event.get("event_type") == "zone_entered":
                zones[event["zone_name"]] += 1

        return dict(
            sorted(
                zones.items(),
                key=lambda x: x[1],
                reverse=True,
            )
        )

    def average_queue_wait(self):
        waits = [
            event["wait_seconds"]
            for event in self.events
            if event.get("event_type") in (
                "queue_completed",
                "queue_abandoned",
            )
        ]

        if not waits:
            return 0

        return round(sum(waits) / len(waits), 2)

    def queue_abandonment_rate(self):
        completed = sum(
            1
            for e in self.events
            if e.get("event_type") == "queue_completed"
        )

        abandoned = sum(
            1
            for e in self.events
            if e.get("event_type") == "queue_abandoned"
        )

        total = completed + abandoned

        if total == 0:
            return 0

        return round((abandoned / total) * 100, 2)

    def revenue_per_visitor(self):
        revenue = self.sales.get("total_revenue", 0)

        visitors = sum(
            1
            for e in self.events
            if e.get("event_type") == "entry"
        )

        if visitors == 0:
            return 0

        return round(revenue / visitors, 2)