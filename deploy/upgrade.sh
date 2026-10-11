#!/usr/bin/env bash

# Upgrades the server checkout to the latest version and restarts the service.

set -euo pipefail

cd "$(dirname "$0")/.."

git pull
git fetch --tags
uv pip install -e .
uv sync --all-extras --locked

# Throttle the index build so it does not starve other workloads on the host.
systemd-run --scope --quiet \
    -p CPUQuota=50% -p CPUWeight=10 \
    -p IOWeight=10 \
    -p MemoryHigh=256M \
    uv run pyrefdev-indexer build-index

systemctl restart pyrefdev.service
