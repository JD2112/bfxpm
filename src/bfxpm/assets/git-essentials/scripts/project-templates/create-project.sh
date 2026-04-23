#!/bin/bash
MAKEFILE="$HOME/.makefiles/project-templates.mk"
read -p "Enter your full name: " AUTHOR
read -p "Enter the project directory name: " DIR
make -f "$MAKEFILE" project AUTHOR="$AUTHOR" DIR="$DIR"