#!/usr/bin/env python3
"""Accumulate GitHub profile repo traffic views into a shields.io endpoint gist."""
import json, os, requests

REPO = "areporeporepo/areporeporepo"
GIST_ID = os.environ["VIEWS_GIST_ID"]
TOKEN = os.environ["GH_GIST_TOKEN"]
headers = {"Authorization": f"token {TOKEN}", "Accept": "application/vnd.github+json"}

# Get current count from gist
gist = requests.get(f"https://api.github.com/gists/{GIST_ID}", headers=headers).json()
current = json.loads(gist["files"]["views.json"]["content"])
total = int(current["message"])

# Get 14-day traffic from GitHub
traffic = requests.get(f"https://api.github.com/repos/{REPO}/traffic/views", headers=headers).json()
new_views = traffic.get("count", 0)

# Accumulate (store last seen count to avoid double-counting)
last_seen = int(current.get("_last", 0))
delta = max(0, new_views - last_seen)
total += delta

# Update gist
payload = {
    "schemaVersion": 1,
    "label": "views",
    "message": str(total),
    "color": "grey",
    "style": "flat",
    "_last": new_views,
}
requests.patch(
    f"https://api.github.com/gists/{GIST_ID}",
    headers=headers,
    json={"files": {"views.json": {"content": json.dumps(payload)}}},
)
print(f"total={total} delta={delta} (traffic={new_views}, last_seen={last_seen})")
