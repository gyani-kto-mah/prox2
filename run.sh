#!/bin/bash

# TODO: Port customization for Proxy, and Web interface.

mitmdump -s prox.py --set block_global=false --set console_eventlog_verbosity=warn --set termlog_verbosity=warn &> ./.logs/mitm.out &

echo "[+] Started an HTTP Proxy on port: http://*:8080"
echo "[+] Starting web interface on http://localhost:8000"

cd ui/
PYTHONUNBUFFERED=TRUE uvicorn main:app --log-level warning &> ../.logs/uvicorn.out 

rm -rf __pycache__
rm -rf ui/__pycache__
