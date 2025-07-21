# Lafufu ComfyUI Generator

Automated ComfyUI workflow generator for creating 216 unique Lafufu doll variations.

## Prerequisites

1. **ComfyUI**: Must be running on `http://127.0.0.1:8188`
2. **Python 3.7+**: Required for the automation script
3. **Reference Image**: Place `reference_Image.jpg` in `assets/lafufu/` directory

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure ComfyUI is running:
   - Start ComfyUI
   - Verify it's accessible at `http://127.0.0.1:8188`

3. Place your reference image:
   - Copy your reference image to `assets/lafufu/reference_Image.jpg`

## Usage

Run the automation script:
```bash
python lafufuGeneration.py
```

### Generation Modes

1. **Generate ALL images (216 total)**: Creates all prompt variations
2. **Generate specific prompts**: Choose specific variations like `A0.0V0.6D0.6`
3. **Test with first 3 prompts**: Quick test mode
4. **Resume from specific prompt**: Continue from where you left off

### Features

- ✅ Automatically modifies ComfyUI workflow for each prompt
- ✅ Creates temporary text files for each prompt
- ✅ Manages image output with proper filenames
- ✅ Batched processing to avoid overwhelming ComfyUI
- ✅ Progress tracking and error handling
- ✅ Resume capability for interrupted sessions
- ✅ Automatic cleanup of temporary files

### File Structure

```
Labubu-Generator/
├── lafufuGeneration.py          # Main automation script
├── requirements.txt             # Python dependencies
├── assets/lafufu/              # Input/Output images
│   ├── reference_Image.jpg     # Reference image (you provide this)
│   └── [generated_images].png  # Generated output images
├── imageGen/
│   ├── Lafufu_wf.json          # ComfyUI workflow template
│   └── labubu_prompts_AVD.json # 216 prompt variations
└── README.md                   # This file
```

### Example Output Files

Generated images will be named according to their prompt keys:
- `A0.0V0.0D0.0.png` - Bunny + denim + crystal necklace
- `A0.0V0.6D0.6.png` - Bunny + faux fur + retro water goggles
- `A1.0V1.0D1.0.png` - Dragon + faux leather + plush Jordan sneakers
- And 213 more variations...

### Troubleshooting

**ComfyUI Connection Failed**:
- Ensure ComfyUI is running
- Check the URL `http://127.0.0.1:8188` in your browser
- Verify no firewall is blocking the connection

**Missing Reference Image**:
- Place your image at `assets/lafufu/reference_Image.jpg`
- Ensure the file format is supported by ComfyUI

**Generation Errors**:
- Check ComfyUI console for workflow errors
- Ensure all required ComfyUI nodes/models are installed
- Try the test mode first (option 3)

## Prompt Variations

The generator creates images with these variations:
- **Animals (A)**: Bunny (0.0), Rooster (0.2), Dog (0.4), Monkey (0.6), Tiger (0.8), Dragon (1.0)
- **Accessories (V)**: Crystal necklace (0.0), Macrame bracelet (0.2), Chunky scarf (0.4), Water goggles (0.6), Gold chain (0.8), Jordan sneakers (1.0)
- **Materials (D)**: Denim (0.0), Mesh knit (0.2), Puffer fabric (0.4), Faux fur (0.6), Satin (0.8), Faux leather (1.0)

Total combinations: 6 × 6 × 6 = 216 unique variations 