# AiManager

- [Send AI Ask request](#send-ai-ask-request)
- [Send AI Text Gen request](#send-ai-text-gen-request)

## Send AI Ask request

Sends an AI request to supported LLMs and returns an answer specifically focused on the user's question given the provided context.

This operation is performed by calling function `create_ai_ask`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-ask/).

_Currently we don't have an example for calling `create_ai_ask` in integration tests_

### Arguments

- mode `CreateAiAskMode`
  - The mode specifies if this request is for a single or multiple items.
- prompt `str`
  - The prompt provided by the client to be answered by the LLM.
- items `List[CreateAiAskItems]`
  - The items to be processed by the LLM, often files.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiResponse`.

A successful response including the answer from the LLM.

## Send AI Text Gen request

Sends an AI request to supported LLMs and returns an answer specifically focused on the creation of new text.

This operation is performed by calling function `create_ai_text_gen`.

See the endpoint docs at
[API Reference](https://developer.box.com/reference/post-ai-text-gen/).

_Currently we don't have an example for calling `create_ai_text_gen` in integration tests_

### Arguments

- prompt `str`
  - The prompt provided by the client to be answered by the LLM.
- items `List[CreateAiTextGenItems]`
  - The items to be processed by the LLM, often files.
- dialogue_history `Optional[List[CreateAiTextGenDialogueHistory]]`
  - The history of prompts and answers previously passed to the LLM. This provides additional context to the LLM in generating the response.
- extra_headers `Optional[Dict[str, Optional[str]]]`
  - Extra headers that will be included in the HTTP request.

### Returns

This function returns a value of type `AiResponse`.

A successful response including the answer from the LLM.