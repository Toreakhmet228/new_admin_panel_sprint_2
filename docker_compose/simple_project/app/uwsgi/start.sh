#!/bin/bash

function foo() {
  echo "$1"
}

read -p "hell wordl: " name
foo "$name"


for file in *; do
  echo $file

done