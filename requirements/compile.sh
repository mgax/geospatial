#!/bin/bash

set -euo pipefail
cd "$(dirname "$0")"/..

pip-compile requirements/base.in "$@"
pip-compile requirements/dev.in "$@"
