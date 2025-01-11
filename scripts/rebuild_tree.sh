#!/bin/bash
set -e

rm -rf build/
rm -rf tree-sitter-jftt/src/*.o
cd tree-sitter-jftt/
tree-sitter generate
cd ..
pip install -e tree-sitter-jftt


echo "Rebuild completed successfully."


