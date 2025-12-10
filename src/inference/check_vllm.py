from vllm import LLM, SamplingParams
prompts = [
    "Mexico is famous for ",
    "The largest country in the world is ",
    "what's up anselm"
]

sampling_params = SamplingParams(temperature=0.8, top_p=0.95)
llm = LLM(model="anselmlong/almost-anselm")
responses = llm.generate(prompts, sampling_params)

for response in responses:
    print(response.outputs[0].text)
    