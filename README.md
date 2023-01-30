# Diffusion Frame 🖼️    
A Stable Diffusion powered e-Paper picture frame

## Getting Started

1. Install the pre-requisites (run pre.sh)
2. Create a virtual environment and install the requirements
   
   2.1. `virtualenv venv`

   2.2 `source venv/bin/activate`

   2.3 `pip install -r requirements.txt`
3. Update app.py

    3.1. Update the `display_type` to match your e-Paper display type
    
    3.2. Update the `gradio_inference_url` to match your gradio inference url
3. Run the script `python3 app.py`
4. Access the gradio app at `http://localhost:7860`