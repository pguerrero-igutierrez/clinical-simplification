"""
Llama-FT-merged — Clinical Text Simplifier (Gradio demo)
Deployed on Hugging Face Spaces: https://huggingface.co/spaces/pguerrero-igutierrez/llama-text-simplifier

This app loads the Llama-FT-merged model (LoRA weights merged into Llama-3.2-1B-Instruct)
and exposes a simple text-simplification interface.
"""

import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Model loading ──────────────────────────────────────────────────────────────
MODEL = "pguerrero-igutierrez/llama-3.2-claramed"
DEVICE = "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(
    MODEL,
    dtype=torch.float32,       
    device_map="cpu",
)
model.eval()

# ── Inference ──────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "Eres un asistente médico especializado en simplificar textos médicos "
    "al español sencillo. Simplifica el texto manteniendo la información esencial "
    "pero usando un lenguaje claro y accesible para pacientes sin formación médica."
)

def make_inference_prompt(source):
    return (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\nSimplifica el siguiente texto médico:\n\n{source.strip()}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )

def simplify(text):
    if not text.strip():
        return ""
    prompt = make_inference_prompt(text)
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)
    with torch.no_grad():
        outputs = model.generate(
            input_ids=inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_new_tokens=512,
            do_sample=False,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.convert_tokens_to_ids("<|im_end|>"),
        )
    gen_tokens = outputs[0][inputs.input_ids.shape[-1]:]
    pred = tokenizer.decode(gen_tokens, skip_special_tokens=False).strip()
    for special_tok in ["<|eot_id|>", "<|start_header_id|>", "<|end_header_id|>"]:
        pred = pred.replace(special_tok, "")
    if "<|im_end|>" in pred:
        pred = pred.split("<|im_end|>")[0].strip()
    return pred

def chat(user_message, history):
    if not user_message.strip():
        return history, ""
    response = simplify(user_message)
    history.append({"role": "user",      "content": user_message})
    history.append({"role": "assistant", "content": response})
    return history, ""

# ── UI ─────────────────────────────────────────────────────────────────────────
css = """
footer { display: none !important; }
.built-with { display: none !important; }
"""

with gr.Blocks(title="CLARA-MeD Simplifier") as demo:   
    gr.Markdown("## CLARA-MeD Clinical Text Simplifier")
    gr.Markdown("*Developed by Paula Guerrero & Iker Gutierrez. Fine-tuned on Llama-3.2-1B-Instruct.* ")

    chatbot = gr.Chatbot(value=[], height=460, show_label=False)  

    with gr.Row():
        input_box = gr.Textbox(
            lines=2,
            placeholder="Type your text here...",
            label="",
            scale=5,
            container=False,
        )
        btn = gr.Button("Simplify", variant="primary", scale=1, min_width=70)

    gr.Examples(
        label="Examples",
        examples=[
            ["Se objetiva derrame pleural bilateral."],
            ["El diagnóstico diferencial incluye tromboembolismo pulmonar."],
            ["Mujeres de más de 18 años y menores de 42 programadas para la realización de un ciclo de fecundación in vitro con transferencia diferida de un blastocisto tras screening genético preimplantacional (PGT-A)."],
        ],
        inputs=input_box,
    )

    state = gr.State([])
    btn.click(fn=chat, inputs=[input_box, state], outputs=[chatbot, input_box])
    input_box.submit(fn=chat, inputs=[input_box, state], outputs=[chatbot, input_box])

demo.launch(css=css)   
