from gliner import GLiNER
from typing import List, Dict
import gc
import torch
import os

global_model = None
device = 'cuda' if torch.cuda.is_available() else 'cpu'

def get_entities(text: str, model: str = 'EmergentMethods/gliner_large_news-v2.1', labels: List[str] = ['PERSON', 'ORGANIZATION', 'LOCATION', 'DATE'], threshold: float = 0.4) -> List[Dict[str, str]]:
    if global_model is None:
        load_model(model)
    entities = global_model.predict_entities(text, labels, threshold)
    print(entities)
    return entities

def unload_model():
    global global_model
    if global_model is not None:
        del global_model
        global_model = None
        gc.collect()

def load_model(model: str = 'EmergentMethods/gliner_large_news-v2.1'):
    global global_model
    if global_model is None:
        # Extract model name without organization prefix
        model_name = model.split('/')[-1] if '/' in model else model
        local_path = os.path.join('./models', model_name)
        
        # Try loading from local path first, fall back to remote
        if os.path.exists(local_path):
            print(f"Loading model from local path: {local_path}")
            global_model = GLiNER.from_pretrained(local_path)
        else:
            print(f"Loading model from remote: {model}")
            global_model = GLiNER.from_pretrained(model)
    
    global_model.to(device)
    global_model.eval()
