#!/bin/bash
curl -X POST http://localhost:8000/refactor \
  -H "Content-Type: application/json" \
  -d '{"code": "for i in range(len(arr)): print(arr[i])", "language": "python"}'
