"""
Qwen-FT-merged — Clinical Text Simplifier (Gradio demo)
Deployed on Hugging Face Spaces: https://huggingface.co/spaces/pguerrero-igutierrez/qwen-text-simplifier

This app loads the Qwen-FT-merged model (LoRA weights merged into Qwen3.5-0.8B)
and exposes a simple text-simplification interface.
No conversational history is maintained between inputs.
"""

import torch
import gradio as gr
from transformers import AutoTokenizer, AutoModelForCausalLM

# ── Model configuration ────────────────────────────────────────────────────────
MODEL_ID = "pguerrero-igutierrez/qwen-clinical-merged"
DEVICE   = "cuda" if torch.cuda.is_available() else "cpu"
DTYPE    = torch.float16 if DEVICE == "cuda" else torch.float32

SYSTEM_PROMPT = (
    "Eres un asistente médico especializado en simplificar textos médicos complejos "
    "al español sencillo. Simplifica el texto manteniendo la información esencial "
    "pero usando un lenguaje claro y accesible para pacientes sin formación médica."
)

# ── Load model & tokenizer ─────────────────────────────────────────────────────
print(f"Loading {MODEL_ID} on {DEVICE} …")
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=DTYPE,
    device_map="auto",
)
model.eval()
print("Model loaded.")


# ── Inference ──────────────────────────────────────────────────────────────────
def make_prompt(source: str) -> str:
    return (
        f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
        f"<|im_start|>user\nSimplifica el siguiente texto médico:\n\n{source.strip()}<|im_end|>\n"
        "<|im_start|>assistant\n"
    )


def simplify(source: str) -> str:
    if not source.strip():
        return "⚠️ Por favor, introduce un texto médico para simplificar."

    prompt = make_prompt(source)
    inputs = tokenizer(prompt, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=128,
            do_sample=False,          # greedy decoding
            eos_token_id=tokenizer.convert_tokens_to_ids("<|im_end|>"),
        )

    # Decode only the newly generated tokens
    new_tokens = output_ids[0][inputs["input_ids"].shape[-1]:]
    result = tokenizer.decode(new_tokens, skip_special_tokens=True)
    return result.strip()


# ── Gradio interface ───────────────────────────────────────────────────────────
EXAMPLES = [
    ["Se recomienda profilaxis tromboembólica durante el postoperatorio."],
    ["Diagnóstico de cáncer de vejiga con invasión muscular (MIBC) confirmado histológicamente "
     "(estadio T2-4a N0/N1 M0) mediante resección transuretral del tumor vesical (TURBT) "
     "realizada no más de 3 meses antes de la visita de selección."],
    ["Se incluirán aquellos pacientes con cambios degenerativos espondiloartrósicos "
     "(hernia discal, estenosis de canal, estenosis de recesos laterales, estenosis de foramen "
     "de conjunción, espondilolistesis) que no verifiquen los criterios de exclusión."],
]

with gr.Blocks(title="Clinical Text Simplifier — Qwen") as demo:
    gr.Markdown(
        """
        # 🏥 Clinical Text Simplifier — Qwen-FT-merged
        Simplificación automática de textos clínicos en español.  
        Modelo: **Qwen3.5-0.8B** fine-tuned with LoRA on [CLARA-MeD](https://github.com/lcampillos/CLARA-MeD).
        > This demo is **not** a conversational chatbot. Each input is processed independently.
        """
    )
    with gr.Row():
        with gr.Column():
            input_box = gr.Textbox(
                label="Texto médico complejo (español)",
                placeholder="Introduce aquí el texto clínico a simplificar…",
                lines=6,
            )
            submit_btn = gr.Button("Simplificar", variant="primary")
        with gr.Column():
            output_box = gr.Textbox(
                label="Texto simplificado",
                lines=6,
                interactive=False,
            )
    gr.Examples(examples=EXAMPLES, inputs=input_box)
    submit_btn.click(fn=simplify, inputs=input_box, outputs=output_box)

if __name__ == "__main__":
    demo.launch()
