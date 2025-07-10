#!/bin/bash

while true; do
  POD=$(kubectl get pods -l app=demo-app --field-selector=status.phase=Running -o jsonpath='{.items[*].metadata.name}' | tr ' ' '\n' | shuf -n 1)
  echo "Deleting pod: $POD"
  kubectl delete pod "$POD"
  sleep 20
done
