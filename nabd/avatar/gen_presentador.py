"""Prueba (no forma parte del flujo diario): genera candidatos de imagen del presentador IA de Nabd Wall Street
con SDXL-Turbo en CPU. Uso: python gen_presentador.py <carpeta_salida>"""
import sys, time, os
import torch
from diffusers import AutoPipelineForText2Image

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
torch.set_num_threads(os.cpu_count())
t0 = time.time()
pipe = AutoPipelineForText2Image.from_pretrained("stabilityai/sdxl-turbo", torch_dtype=torch.float32)
print(f"modelo cargado en {time.time()-t0:.0f}s", flush=True)

BASE = ("professional photograph, head and shoulders portrait of a {who}, financial news anchor, "
        "facing the camera directly, looking straight into the lens, calm neutral expression, mouth closed, "
        "sitting in a modern TV news studio, dark navy blue background with soft golden bokeh lights, "
        "soft studio lighting, sharp focus, 85mm lens, photorealistic, high detail")
WHO = [
    "Gulf Arab man in his 40s wearing a white thobe and white ghutra headscarf with black agal, short neat beard",
    "Gulf Arab man in his 40s wearing a white thobe and red and white checkered shemagh with black agal, short trimmed beard",
    "Arab man in his 40s wearing a dark navy suit, white shirt and gold tie, short neat beard",
    "Gulf Arab man in his 30s wearing a white thobe and white ghutra with black agal, short neat beard, friendly",
]
i = 0
for w, who in enumerate(WHO):
    for seed in (11, 23):
        t = time.time()
        g = torch.Generator().manual_seed(seed)
        img = pipe(prompt=BASE.format(who=who), num_inference_steps=4, guidance_scale=0.0,
                   width=512, height=512, generator=g).images[0]
        i += 1
        img.save(f"{out}/candidato-{i:02d}-p{w+1}-s{seed}.png")
        print(f"candidato {i} en {time.time()-t:.0f}s", flush=True)
print(f"total {time.time()-t0:.0f}s")
