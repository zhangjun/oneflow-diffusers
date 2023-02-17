import oneflow as flow

flow.mock_torch.enable()
from diffusers import DPMSolverMultistepScheduler
from onediff import OneFlowStableDiffusionPipeline as StableDiffusionPipeline

model_id = "CompVis/stable-diffusion-v1-4"

dpm_solver = DPMSolverMultistepScheduler.from_config(model_id, subfolder="scheduler")

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    use_auth_token=True,
    revision="fp16",
    torch_dtype=flow.float16,
    scheduler=dpm_solver,
    num_inference_steps=20,
)

pipe = pipe.to("cuda")

prompt = "a photo of an astronaut riding a horse on mars"
with flow.autocast("cuda"):
    images = pipe(prompt).images
    for i, image in enumerate(images):
        image.save(f"{prompt}-of-{i}.png")
