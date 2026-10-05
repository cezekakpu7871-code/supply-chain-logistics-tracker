import hashlib
import json
from datetime import datetime


class ShipmentPackage:
    """Represents a parcel moving through a supply chain network."""

    def __init__(self, package_id: str, origin: str, destination: str):
        self.package_id = package_id
        self.origin = origin
        self.destination = destination
        self.status = "CREATED"
        self.location_history = []
        self._add_checkpoint(origin, "Package created at facility")

    def _add_checkpoint(self, location: str, status_message: str):
        """Appends an immutable tracking event to the history log."""
        checkpoint = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "location": location,
            "status": status_message,
            "hash": self._generate_event_hash(location, status_message)
        }
        self.location_history.append(checkpoint)

    def _generate_event_hash(self, location: str, status: str) -> str:
        """Generates a cryptographic hash to ensure log integrity."""
        payload = f"{self.package_id}:{location}:{status}:{datetime.utcnow().timestamp()}"
        return hashlib.sha256(payload.encode()).hexdigest()

    def update_location(self, new_location: str, status_description: str):
        """Updates package transit status."""
        self.status = "IN_TRANSIT"
        self._add_checkpoint(new_location, status_description)
        print(f"[TRACKING UPDATE] Package {self.package_id} reached {new_location}.")

    def mark_delivered(self, final_location: str):
        """Finalizes package delivery status."""
        self.status = "DELIVERED"
        self._add_checkpoint(final_location, "Package delivered to recipient")
        print(f"[DELIVERY COMPLETE] Package {self.package_id} delivered at {final_location}.")


# Demonstration Run
if __name__ == "__main__":
    print("=== LOGISTICS TRACKER DEMO ===")
    shipment = ShipmentPackage("PKG-9921", "Lagos Hub", "Abuja Delivery Station")
    shipment.update_location("Lokoja Transit Center", "In transit through highway checkpoint")
    shipment.mark_delivered("Abuja Delivery Station")
    print("\nAudit Log:")
    print(json.dumps(shipment.location_history, indent=2))
