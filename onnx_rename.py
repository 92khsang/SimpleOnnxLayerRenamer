#!/usr/bin/python
import sys
from arguments.parse import Parser
from arguments.split import Splitter

import os
import onnx

def help():
   print("[Usage]")
   print("  onnx_convert.py -t <target_node_name_list> -d <desire_node_name_list>\n")
   print("[Example]")
   print("1. Rename single node (input.1 -> input)")

   print("  onnx_convert.py -t input.1 -d input")
   print("2. Rename multi nodes (300 -> score, 301 -> box)")
   print("  onnx_convert.py -t 300,301 -d score,box")
   print("")

class Converter():
   def __init__(self, args : dict):
      if not isinstance(args, dict):
        raise TypeError("Invalid Input arguments")

      self.__model = onnx.load(args['file'])
      self.__old_names = args['target']
      self.__new_names = args['dest']
      self.__number_of_target = len(self.__old_names)

      self.__model_input_layers = self.__model.graph.input
      self.__model_output_layers = self.__model.graph.output
      self.__model_node_layers = self.__model.graph.node
      

   def __find_in_input_layer(self, layer_name : str) -> int:
      for i in range(0, len(self.__model_input_layers)):
         if self.__model_input_layers[i].name == layer_name:
            return i
      return -1
               

   def __find_in_output_layer(self, layer_name : str):
      for i in range(0, len(self.__model_output_layers)):
         if self.__model_output_layers[i].name == layer_name:
            return i
      return -1

   def __find_in_node_layer(self, layer_name : str):
      for i in range(0, len(self.__model_node_layers)):
         if self.__model_node_layers[i].name == layer_name:
            return i
      return -1

   def __convert_input_layer(self, target_index : int, new_name : str):
      old_name = self.__model_input_layers[target_index].name
      self.__model_input_layers[target_index].name = new_name
      for linked_node_layer in self.__model_node_layers:
         for i in range(0, len(linked_node_layer.input)):
            if linked_node_layer.input[i] == old_name:
               linked_node_layer.input[i] = new_name
               break

   def __convert_output_layer(self, target_index : int, new_name : str):
      old_name = self.__model_output_layers[target_index].name
      self.__model_output_layers[target_index].name = new_name
      for linked_node_layer in self.__model_node_layers:
         for i in range(0, len(linked_node_layer.output)):
            if linked_node_layer.output[i] == old_name:
               linked_node_layer.output[i] = new_name
               break

   def __convert_node_layer(self, target_index : int, new_name : str):
      old_name = self.__model_node_layers[target_index].name
      self.__model_node_layers[target_index].name = new_name
      for linked_node_layer in self.__model_node_layers:
         for i in range(0, len(linked_node_layer.input)):
            if linked_node_layer.input[i] == old_name:
               linked_node_layer.input[i] = new_name
               break
         for i in range(0, len(linked_node_layer.output)):
            if linked_node_layer.output[i] == old_name:
               linked_node_layer.output[i] = new_name
               break

   def convert(self) -> onnx.ModelProto:
      if self.__model is None:
         raise NameError("No model file")

      print("Start converting...")
      for i in range(0, self.__number_of_target):
         index = self.__find_in_input_layer(self.__old_names[i])
         if index != -1:
            self.__convert_input_layer(index, self.__new_names[i])
            continue

         index = self.__find_in_output_layer(self.__old_names[i])
         if index != -1:
            self.__convert_output_layer(index, self.__new_names[i])
            continue

         index = self.__find_in_node_layer(self.__old_names[i])
         if index != -1:
            self.__convert_node_layer(index, self.__new_names[i])
            continue

         print("[Warning] Cannot find ", self.__old_names[i], " layer")
      print("Finisih converting...")
      return self.__model



def main(argv):
   parser = Parser(argv)
   parsed_arguments = parser.parse()
   if len(parsed_arguments) != 3:
      help()
      sys.exit(-1)

   splitter = Splitter(parsed_arguments)
   splited_arguments = splitter.split()
   if len(splited_arguments['target']) != len(splited_arguments['dest']):
      print("The size of target list and dest list must be the same.")
      sys.exit(-1)

   if len(splited_arguments['target']) == 0:
      print("At least one input value is required.\n")
      help()
      sys.exit(-1)

   converter = Converter(splited_arguments)
   converted_model = converter.convert()

   old_base_fiile_name = os.path.splitext(splited_arguments['file'])[0]
   new_file_name = old_base_fiile_name + "-fixed.onnx"
   
   onnx.save(converted_model, new_file_name)
   print("Done")

   
if __name__ == "__main__":
   main(sys.argv[1:])