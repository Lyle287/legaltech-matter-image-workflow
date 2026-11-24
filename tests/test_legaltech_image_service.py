from datetime import date

from src.legaltech_image_service import MatterIntake, decide_delivery


def test_signed_matter_due_today_is_sent_and_followed_up():
    matter = MatterIntake(
        matter_id="matter-7",
        practice_area="housing law",
        client_name="A Client",
        signed=True,
        delivery_due=date(2026, 10, 24),
    )

    decision = decide_delivery(matter, date(2026, 10, 24))

    assert decision.action == "send_signed_document_and_follow_up"
    assert decision.matter_id == "matter-7"
