"""
Qwen-FT-merged — Clinical Text Simplifier (Gradio demo)
Deployed on Hugging Face Spaces: https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier

This app loads the Qwen-FT-merged model (LoRA weights merged into Qwen3.5-0.8B)
and exposes a simple text-simplification interface.
"""

import re
import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Model loading ─────────────────────────────────────────────────────────────
MODEL = "pguerrero-igutierrez/qwen3.5-claramed"

tokenizer = AutoTokenizer.from_pretrained(MODEL)
model     = AutoModelForCausalLM.from_pretrained(
    MODEL,
    torch_dtype = torch.float32, 
    device_map  = "cpu",
)
model.eval()

# ── Prompt ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "Eres un asistente médico especializado en simplificar textos médicos complejos "
    "al español sencillo. Simplifica el texto manteniendo la información esencial "
    "pero usando un lenguaje claro y accesible para pacientes sin formación médica."
)

def make_inference_prompt(source: str) -> str:
    return (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\nSimplifica el siguiente texto médico:\n\n{source.strip()}<|im_end|>\n"
        "<|im_start|>assistant\n"
        "<think>\n</think>\n"  # suprime thinking mode
    )

# ── Inference ─────────────────────────────────────────────────────────────────
def simplify(text):
    if not text.strip():
        return ""

    prompt  = make_inference_prompt(text)
    stop_id = tokenizer.convert_tokens_to_ids("<|im_end|>")

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        padding=False,
        add_special_tokens=False,
    ).to("cpu")

    with torch.no_grad():
        outputs = model.generate(
            input_ids          = inputs.input_ids,
            attention_mask     = inputs.attention_mask,
            max_new_tokens     = 540,
            use_cache          = True,
            do_sample          = False,
            temperature        = None,
            top_p              = None,
            repetition_penalty = 1.0,
            eos_token_id       = stop_id,
            pad_token_id       = tokenizer.eos_token_id,
        )

    gen_tokens = outputs[0][inputs.input_ids.shape[-1]:]
    pred = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

    pred = re.sub(r"<think>.*?</think>", "", pred, flags=re.DOTALL).strip()

    if "En resumen:" in pred:
        pred = pred.split("En resumen:")[0].strip()

    return pred

def chat(text, history):
    if not text.strip():
        return history, ""
    pred = simplify(text)
    history.append({"role": "user",      "content": text})
    history.append({"role": "assistant", "content": pred})
    return history, ""

# ── UI ────────────────────────────────────────────────────────────────────────
css = """
footer { display: none !important; }
.built-with { display: none !important; }
"""

with gr.Blocks(title="CLARA-MeD Simplifier") as demo:
    gr.Markdown("## CLARA-MeD Clinical Text Simplifier")
    gr.Markdown("*Developed by Paula Guerrero & Iker Gutierrez. Fine-tuned on Qwen3.5-0.8B.*")

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
            ["Se realizará un PGT-A para descartar la presencia de embriones aneuploides."],
            ["Mujeres de más de 18 años y menores de 42 programadas para la realización de un ciclo de fecundación in vitro con transferencia diferida de un blastocisto tras screening genético preimplantacional (PGT-A)."],
        ],
        inputs=input_box,
    )

    state = gr.State([])
    btn.click(fn=chat, inputs=[input_box, state], outputs=[chatbot, input_box])
    input_box.submit(fn=chat, inputs=[input_box, state], outputs=[chatbot, input_box])

demo.launch(
    css=css,
)
