import os
import requests
from flask import Flask, request, redirect, render_template_string

# === Config ===
CLIENT_ID = os.environ.get("LOYVERSE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOYVERSE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LOYVERSE_REDIRECT_URI")
LOYVERSE_TOKEN_URL = "https://api.loyverse.com/oauth/token"

app = Flask(__name__)


@app.route("/")
def index():
    if not (CLIENT_ID and REDIRECT_URI):
        return "<h3>Environment variables not set. Please configure LOYVERSE_CLIENT_ID and LOYVERSE_REDIRECT_URI.</h3>"

    scopes = [
        "stores.read",
        "customers.read",
        "customers.write",
        "items.read",
        "receipts.read",
        "receipts.write",
    ]
    scope_param = "%20".join(scopes)
    auth_link = (
        "https://api.loyverse.com/oauth/authorize"
        f"?response_type=code&client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope={scope_param}"
    )
    return (
        "<h2>Loyverse OAuth Demo</h2>"
        "<p>This minimal app runs on Render and helps you generate a new "
        "access token & refresh token pair for the Loyverse API.</p>"
        f"<p><a href='{auth_link}'>⭕ Click here to connect your Loyverse account</a></p>"
    )


@app.route("/oauth/callback")
def oauth_callback():
    code = request.args.get("code")
    if not code:
        return "Missing ?code= parameter from Loyverse redirect.", 400

    token_payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    resp = requests.post(LOYVERSE_TOKEN_URL, data=token_payload, timeout=15)
    if resp.status_code != 200:
        return f"Failed to fetch token: {resp.status_code} - {resp.text}", resp.status_code

    token = resp.json()
    # NOTE: Persist token['refresh_token'] securely in your DB or Render Secret.
    return render_template_string(
        """
        <h2>✅ Authorization successful!</h2>
        <p><strong>Access&nbsp;Token:</strong> {{ access }}</p>
        <p><strong>Refresh&nbsp;Token:</strong> {{ refresh }}</p>
        <hr>
        <p style='color:red;'>Copy & store the refresh token somewhere safe—this page will never show it again.</p>
        """,
        access=token["access_token"],
        refresh=token["refresh_token"],
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
