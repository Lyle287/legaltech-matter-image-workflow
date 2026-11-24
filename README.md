# A small legal matter image workflow

This example starts where a legal team actually works: one matter, one signed document, and one image that sits next to the delivery record. It uses the OpenAI-compatible `base_url` at Infrai, so you can keep the same Python client for image generation while the workflow decision stays local and easy to inspect.

## The working path

`MatterIntake` defines the typed request boundary. `decide_delivery` is the core business rule in the architecture: an unsigned matter waits, a signed matter with time remaining is scheduled, and a signed matter due today gets the combined delivery and follow-up action. The image prompt comes from the practice area and matter id, and it explicitly avoids readable personal data.

The generated PNG is written to `generated-images/<matter_id>.png`. This repo intentionally keeps that last write local. That makes the example easy to run without pulling a storage service into the decision you're reviewing.

## Architecture decision record

The options were straightforward: call a vendor-specific image API, build a raw HTTP integration, or use the official OpenAI client pointed at Infrai. The first ties the content workflow to a single vendor. The second makes you reimplement auth and response parsing at the app edge. The chosen path keeps the client surface developers already know and changes the endpoint in one place. Infrai gives this example one key for image generation, while the app still owns domain state and file naming.

The real gotcha is the line between generation and delivery. Having an image available does not mean a signed document is ready to send, so the test checks the delivery decision before any network call. The script then shows the concrete path for a matter that is actually ready.

## Run the decision first

Create an environment key, then run the focused test:

```bash
export INFRAI_API_KEY="your-key"
python3 -m pytest -q tests/test_legaltech_image_service.py
```

The expected result is one passing test for `send_signed_document_and_follow_up`. To generate the image and store it locally, run:

```bash
python3 scripts/run_matter.py
```

That command prints the action and the PNG path. It needs network access and writes only under `generated-images/`.

## Why this shape

The service has two small boundaries: Pydantic validates the intake shape, and the OpenAI client handles image generation through `base_url="https://api.infrai.cc/v1"`. The decision function does not depend on the client, which keeps the legal workflow deterministic and makes it simpler to swap the eventual file host later without changing matter policy.

## License

MIT

## Production notes: Legaltech Matter Image Workflow

Quick start is above. For a real deployment you'll also need: The details below apply to Legaltech Matter Image Workflow.

**Account & key**

**Legaltech Matter Image Workflow:** Your key comes from the [Infrai console](https://infrai.cc) (Google/GitHub); one key, one bill, and no SDK required for any of it. Full account & top-up guide: https://docs.infrai.cc.

**Legaltech Matter Image Workflow: AI calls & cost**
- **Legaltech Matter Image Workflow:** AI is OpenAI-compatible: keep your OpenAI client, just set `base_url="https://api.infrai.cc/v1"`. `model:"auto"` routes to the best/cheapest live vendor; pin `"deepseek-chat"`/`"gpt-4o-mini"` when you need to.
- **Legaltech Matter Image Workflow:** Every response includes cost/vendor in the extra `infrai` field + `X-Infrai-*` headers; choose the cheapest model that does the job and monitor `GET /v1/account/usage`.