import json
import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

logger = logging.getLogger(__name__)

class MalformedLayerException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

def parse_layer(layer_def):
    """
    Given a dictionary describing a layer, return the corresponding PyTorch layer.
    
    Example of layer_def:
    {
      "type": "Linear",
      "in_features": 4,
      "out_features": 8
    }
    
    Supported types in this demo:
    - Linear
    - ReLU
    - Conv2d
    - MaxPool2d
    (Add more as needed.)
    """
    # print(layer_def)
    layer_type = layer_def["type"]
    if layer_type == "Linear":
        # required fields: in_features, out_features
        return nn.Linear(
            in_features=layer_def["in_features"],
            out_features=layer_def["out_features"],
            bias = layer_def.get('bias',True)
        )
    
    elif layer_type == "ReLU":
        # No arguments needed
        return nn.ReLU()
    
    elif layer_type == "Conv2d":
        # minimal fields: in_channels, out_channels, kernel_size
        # optional: stride, padding, dilation, etc.
        return nn.Conv2d(
            in_channels=layer_def["in_channels"],
            out_channels=layer_def["out_channels"],
            kernel_size=layer_def["kernel_size"],
            stride=layer_def.get("stride", 1),
            padding=layer_def.get("padding", 0),
            dilation=layer_def.get("dilation", 1)
        )
    
    elif layer_type == "MaxPool2d":
        # minimal fields: kernel_size
        return nn.MaxPool2d(
            kernel_size=layer_def["kernel_size"],
            stride=layer_def.get("stride", None),
            padding=layer_def.get("padding", 0)
        )
    
    else:
        raise ValueError(f"Unsupported layer type: {layer_type}")

def parse_model(model_definition: dict, input_dim:int = None, output_dim:int = None):
    """
    Given a dictionary describing an entire model,
    return a PyTorch nn.Sequential model.
    
    Example of model_def:
    {
      "name": "MyModel",
      "layers": [
        { "type": "Linear", "in_features": 4, "out_features": 8 },
        { "type": "ReLU" },
        { "type": "Linear", "in_features": 8, "out_features": 2 }
      ]
    }

    raises 
    MalformedLayerException for errors in layer definition
    """
    # print(input_dim, output_dim)
    layers = []
    for idx, layer_info in enumerate(model_definition["layers"]):
        try:
            if idx == 0:
                layer_info['in_features'] = input_dim
            if idx == len(model_definition['layers']) - 1:
                layer_info['out_features'] = output_dim
            layer = parse_layer(layer_info)
        except KeyError:
            raise MalformedLayerException(f'Error while parsing layer {layer_info}. Please check definition')
        layers.append(layer)
    # build an nn.Sequential with these layers
    return nn.Sequential(*layers)

def convert_model_to_json(pytorch_model: torch.nn.Sequential, model_name="ExportedModel"):
    """
    Given a PyTorch model (nn.Sequential), convert it to a JSON-like dict.
    This is a simple demo: it only handles a few layer types.
    """
    layers_def = []
    for layer in pytorch_model:
        layer_type = layer.__class__.__name__
        
        if layer_type == "Linear":
            layer_dict = {
                "type": "Linear",
                "in_features": layer.in_features,
                "out_features": layer.out_features,
                "bias":  (False if layer.bias is None else True)
            }
        elif layer_type == "ReLU":
            layer_dict = {
                "type": "ReLU"
            }
        elif layer_type == "Conv2d":
            layer_dict = {
                "type": "Conv2d",
                "in_channels": layer.in_channels,
                "out_channels": layer.out_channels,
                "kernel_size": layer.kernel_size[0],
                "stride": layer.stride[0],
                "padding": layer.padding[0],
                "dilation": layer.dilation[0]
            }
        elif layer_type == "MaxPool2d":
            layer_dict = {
                "type": "MaxPool2d",
                "kernel_size": layer.kernel_size,
                "stride": layer.stride,
                "padding": layer.padding
            }
        else:
            raise ValueError(f"convert_model_to_json: Unsupported layer type: {layer_type}")
        
        layers_def.append(layer_dict)
    
    model_def = {
        "layers": layers_def
    }
    return model_def

def write_model(model_name, model, filename:str = 'models.json'):
    '''
    Writes the given model to a JSON file. If the file already exists, it updates the model definition;
    otherwise, it creates a new file with the model definition.
    
    Parameters:
    model_name (str): The name of the model to be written.
    model (Any): The model object to be converted and written to the file.
    filename (str, optional): The name of the JSON file to write the model to. Defaults to 'models.json'.
    
    Returns:
    None
    '''
    # Convert the model to a JSON-like dictionary
    model_def = convert_model_to_json(model, model_name)
    # Read the existing models from the file, if it exists
    try:
        with open(filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    # Add or update the model definition
    data[model_name] = model_def
    # Write the updated models back to the file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def get_model(model_name: str, models_file:str = 'models.json', input_dim:int = None, output_dim:int = None):
    # Read JSON from file
    json_file = models_file  # Replace with your actual filename
    with open(json_file, "r") as f:
        data = json.load(f)
    
    # Find the model definition by name
    try:
        mdef = data[model_name]
    except KeyError as e:
        logger.info(f'Model definition for {model_name} Not found. Please check {models_file}')
        raise e
    else: 
        return parse_model(mdef, 
                           input_dim=input_dim, 
                           output_dim=output_dim)


if __name__ == "__main__":
    model = get_model("SimpleModel", models_file='models/models.json', input_dim=42, output_dim=2)
    print(model)

    write_model(model_name='SimpleModel2', model=model, filename='models/models.json')