#!/usr/bin/env bash
# Parallel render: WN capture workers (one Chromium each) split the frames by
# modulo, then a single ffmpeg encode pass. ~WN× faster than sequential.
# Env (inherited by render.js): MBLUR, SS, FMT, JQ, OUT, FPS, MAXT, FROMT, TOT…
#   WN=<workers> bash prender.sh
set -e
cd "$(dirname "$0")"
export WN="${WN:-4}"

echo "▶ parallel capture · $WN workers"
rm -rf frames && mkdir -p frames out
pids=()
for ((i=0; i<WN; i++)); do
  CAPTURE=1 WI="$i" node render.js >"/tmp/wrk$i.log" 2>&1 &
  pids+=($!)
done
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
if [ "$fail" != 0 ]; then echo "✗ a worker failed:"; tail -3 /tmp/wrk*.log; exit 1; fi

echo "▶ encode"
ENCODE=1 node render.js
