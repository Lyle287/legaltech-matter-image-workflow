from datetime import date
from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.legaltech_image_service import MatterIntake, decide_delivery, generate_and_store_image


matter = MatterIntake(
    matter_id="matter-104",
    practice_area="employment law",
    client_name="Example Client",
    signed=True,
    delivery_due=date(2026, 10, 20),
)
decision = decide_delivery(matter, date(2026, 10, 24))
path = generate_and_store_image(decision, Path("generated-images"))
print(decision.action)
print(path)
