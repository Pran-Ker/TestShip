#!/usr/bin/env python3
"""Creates an app in App Store Connect via the REST API using the ASC API key."""

import time, json, sys, os
import urllib.request, urllib.error

try:
    import jwt
except ImportError:
    os.system("pip install PyJWT cryptography -q")
    import jwt

KEY_ID    = os.environ["ASC_KEY_ID"]
ISSUER_ID = os.environ["ASC_ISSUER_ID"]
KEY_PATH  = os.path.expanduser(os.environ["ASC_KEY_PATH"])

BUNDLE_ID = "com.hebbarpran.testship"
APP_NAME  = "TestShip"
SKU       = "testship-001"

def make_token():
    with open(KEY_PATH) as f:
        private_key = f.read()
    now = int(time.time())
    payload = {"iss": ISSUER_ID, "iat": now, "exp": now + 1200, "aud": "appstoreconnect-v1"}
    return jwt.encode(payload, private_key, algorithm="ES256", headers={"kid": KEY_ID})

def asc_request(method, path, body=None):
    token = make_token()
    url = f"https://api.appstoreconnect.apple.com/v1/{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        err = json.loads(e.read())
        print(f"HTTP {e.code}: {json.dumps(err, indent=2)}")
        sys.exit(1)

# 1. Find the bundle ID resource
print(f"Looking up bundle ID {BUNDLE_ID}...")
result = asc_request("GET", f"bundleIds?filter[identifier]={BUNDLE_ID}&filter[platform]=IOS")
if not result["data"]:
    print("Bundle ID not found in dev portal. Register it first at developer.apple.com.")
    sys.exit(1)
bundle_id_resource = result["data"][0]["id"]
print(f"  Found: {bundle_id_resource}")

# 2. Create the app
print(f"Creating '{APP_NAME}' in App Store Connect...")
body = {
    "data": {
        "type": "apps",
        "attributes": {
            "bundleId":        BUNDLE_ID,
            "name":            APP_NAME,
            "primaryLocale":   "en-US",
            "sku":             SKU,
        },
        "relationships": {
            "bundleId": {"data": {"type": "bundleIds", "id": bundle_id_resource}}
        }
    }
}
app = asc_request("POST", "apps", body)
app_id = app["data"]["id"]
print(f"  Created app, ID: {app_id}")
print("Done — app is now in App Store Connect.")
