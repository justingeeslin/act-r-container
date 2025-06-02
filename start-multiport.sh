#!/bin/bash
set -e
set -m

# Multi-port startup script for ACT-R container
# Supports environment variables to run specific services

if [ "$JUPYTER_ONLY" = "true" ]; then
    echo "Starting Jupyter-only mode on port $PORT"
    exec /start-it.sh run-jupyter.sh
elif [ "$REMOTE_ONLY" = "true" ]; then
    echo "Starting ACT-R remote interface only on port $PORT"
    # Start ACT-R with remote interface
    cp -n -r -t actr7.x/tutorial actr7.x/original-tutorial/*
    export PYTHONPATH=${PYTHONPATH}:${HOME}/actr7.x/tutorial/python
    exec sbcl --load "quicklisp/setup.lisp" --load "actr7.x/load-act-r.lisp" --eval "(progn (init-des) (echo-act-r-output) (mp-print-versions) (start-environment-server \"0.0.0.0\" $PORT) (loop))"
else
    echo "Starting full ACT-R environment on port $PORT"
    exec /start-it.sh
fi