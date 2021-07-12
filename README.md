# SimpleOnnxLayerRenamer

## Brief
Code to simply change the layer name of the onnx model


## Env
- Python 3
- Onnx


## Usage
```
python3 onnx_rename.py - <onnx_file_name> -t <target_node_name_list> -d <desire_node_name_list>
```
## Example
1. Rename single node (input.1 -> input)
```
python3 onnx_rename.py -f test.onnx -t input.1 -d input
```
2. Rename multi nodes (300 -> score, 301 -> box)
```
python3 onnx_rename.py  -f test.onnx -t 300,301 -d score,box
```
