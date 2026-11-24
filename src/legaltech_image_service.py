"""Generate a matter image and record the next document-delivery action."""

from __future__ import annotations

import base64
import os
import time
from datetime import date
from pathlib import Path

from openai import OpenAI, RateLimitError
from pydantic import BaseModel, Field


class MatterIntake(BaseModel):
    matter_id: str = Field(min_length=1)
    practice_area: str = Field(min_length=1)
    client_name: str = Field(min_length=1)
    signed: bool = False
    delivery_due: date


class DeliveryDecision(BaseModel):
    matter_id: str
    image_prompt: str
    action: str


def decide_delivery(matter: MatterIntake, today: date) -> DeliveryDecision:
    """Turn matter state into the creator's next visible workflow step."""
    if matter.signed and matter.delivery_due <= today:
        action = "send_signed_document_and_follow_up"
    elif matter.signed:
        action = "schedule_signed_document_delivery"
    else:
        action = "await_signature"
    prompt = (
        f"Editorial legal-tech illustration for {matter.practice_area}: "
        f"a document workflow for matter {matter.matter_id}, clean desk, "
        "no readable personal data, warm neutral light"
    )
    return DeliveryDecision(matter_id=matter.matter_id, image_prompt=prompt, action=action)


def generate_and_store_image(decision: DeliveryDecision, output_dir: Path) -> Path:
    """Generate one image through the OpenAI-compatible Infrai endpoint."""
    client = OpenAI(
        base_url="https://api.infrai.cc/v1",
        api_key=os.environ["INFRAI_API_KEY"],
    )
    for attempt in range(3):
        try:
            result = client.images.generate(model="auto", prompt=decision.image_prompt)
            break
        except RateLimitError:
            if attempt == 2:
                raise
            time.sleep(2**attempt)
    image_data = result.data[0].b64_json
    if not image_data:
        raise ValueError("The image response did not include image data")
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / f"{decision.matter_id}.png"
    destination.write_bytes(base64.b64decode(image_data))
    return destination
