FROM vllm/vllm-openai:latest

# Set environment variables
ENV MODEL_NAME=anselmlong/almost-anselm

# Expose the default OpenAI-compatible API port
EXPOSE 8000

# Start the OpenAI-compatible server
CMD python3 -m vllm.entrypoints.openai.api_server \
  --model $MODEL_NAME \
  --tokenizer $MODEL_NAME \
  --dtype float16 \
  --max-model-len 768 \
  --host 0.0.0.0 \
  --port 8000 \
  --trust-remote-code


