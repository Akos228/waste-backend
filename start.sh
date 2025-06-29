#!/bin/bash
uvicorn main:app --host 0.0.0.0 --port $PORT

chmod +x start.sh

# ces lignes de code permet de demarrer le service. ils sont appelés par le render.yaml

