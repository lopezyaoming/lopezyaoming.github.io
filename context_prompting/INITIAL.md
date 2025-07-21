## FEATURE:

Lafufu (viral doll) ComfyUI SDXL prompting automatizer:
You should write a precise python code  (lafufuGeneration.py) that automatically sends a new worflow prompt to my comfyUI running in the background (Initializing upload queue system...
Upload queue system initialized with max_concurrent=3
Starting server

To see the GUI go to: http://127.0.0.1:8188). It's encoded in a JSON called Lafufu.wf.json. i will have an instance of ComfyUI running on my machine, you just need to change three variables. first:  "image": "pasted/image (7).png" to assets\lafufu\reference_Image.jpg. this doesn't change. Second, in   ,
  "35": {
    "inputs": {
      "file_path": "",
      "dictionary_name": "[filename]"
    },
    "class_type": "Load Text File",
    "_meta": {
      "title": "LOAD TEXT FILE"
    }
  }, you will need to load a new .txt, and this .txt will update everytime the worflow resets. this corresponds to the contents of labubu_prompts_AVD.json., as the string that is written in "" after the name of the prompt. an example string "A plush creature with a round cartoon face, oversized eyes, and sharp teeth. It wears a bunny costume made from faux fur, styled with a retro water goggles. Ultra-detailed character concept render, soft toy design, photographed in a professional studio, sharp focus, high-resolution 4K, clean white background, volumetric lighting, cinematic depth of field."" there are 216 possible images. lastly, you will have to dynamically update   ,
  "34": {
    "inputs": {
      "output_path": "[time(%Y-%m-%d)]",
      "filename_prefix": "ComfyUI",
      "filename_delimiter": "",
      "filename_number_padding": 4,
      "filename_number_start": "false",
      "extension": "png",
      "dpi": 300,
      "quality": 100,
      "optimize_image": "true",
      "lossless_webp": "false",
      "overwrite_mode": "false",
      "show_history": "false",
      "show_history_by_prefix": "true",
      "embed_workflow": "true",
      "show_previews": "true",
      "images": [
        "32",
        0
      ]
    },
    "class_type": "Image Save",
    "_meta": {
      "title": "Image Save"
    }
  }, with a the corresponding title of the prompt. for example: "A0.0V0.6D0.0.png". this will be saved here: assets\lafufu . is extremely important that the title corresponds with the appropiate string that is using as prompt. be sure everytime the workflow resets, the corresponding text is also refreshed, as comfyUI sometimes doesn't double check for a refreshing in text. 


