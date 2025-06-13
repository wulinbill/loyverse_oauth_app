import os
import requests
from flask import Flask, request, redirect, render_template_string

# === Config ===
CLIENT_ID = os.environ.get("LOYVERSE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LOYVERSE_CLIENT_SECRET")
REDIRECT_URI = os.environ.get("LOYVERSE_REDIRECT_URI")  # 记得与 Loyverse 后台保持一致
LOYVERSE_TOKEN_URL = "https://api.loyverse.com/oauth/token"

app = Flask(__name__)

# ---------- 首页 ----------
@app.route("/")
def index():
    if not (CLIENT_ID and REDIRECT_URI):
        return "<h3>环境变量未配置：LOYVERSE_CLIENT_ID / LOYVERSE_REDIRECT_URI</h3>"

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
        "<p>点击下方链接授权并生成新的 access/refresh token：</p>"
        f"<p><a href='{auth_link}'>🔗 Connect to Loyverse</a></p>"
    )

# ---------- 回调统一处理函数 ----------
def handle_callback():
    """共用的回调逻辑：用授权码换取 token"""
    code = request.args.get("code")
    if not code:
        return "Missing ?code= parameter in redirect.", 400

    token_payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
    }
    resp = requests.post(LOYVERSE_TOKEN_URL, data=token_payload, timeout=15)
    if resp.status_code != 200:
        return f"Failed to exchange token: {resp.status_code} - {resp.text}", resp.status_code

    token = resp.json()
    # 正式项目请把 token 持久化到数据库 / Secrets
    return render_template_string(
        """
        <h2>✅ Authorization successful!</h2>
        <p><strong>Access&nbsp;Token:</strong> {{ access }}</p>
        <p><strong>Refresh&nbsp;Token:</strong> {{ refresh }}</p>
        <hr>
        <p style='color:red;'>⚠️ 请立即复制并妥善保存 refresh token，此页面不会再次显示。</p>
        """,
        access=token["access_token"],
        refresh=token["refresh_token"],
    )

# ---------- 两条路由指向同一处理 ----------
@app.route("/oauth/callback")
@app.route("/callback")
def oauth_callback():
    return handle_callback()

# ---------- 本地运行 ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
