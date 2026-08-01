#!/usr/bin/env bash
# Idle-resource guard for the TaskFlow lab node.
# Cloud spend is an engineering concern, not an accounting one.
set -euo pipefail
LIMIT_MINUTES="${1:-240}"
sudo shutdown -h "+${LIMIT_MINUTES}" "auto-stop: taskflow lab session limit" || true
echo "Instance will halt in ${LIMIT_MINUTES} minutes. Cancel with: sudo shutdown -c"
