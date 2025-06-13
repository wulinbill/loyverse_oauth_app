# Loyverse OAuth Helper

This tiny Flask app runs on **Render** and helps you complete the Loyverse         OAuth 2.0 flow so you can generate a **refresh token** for API calls.

## 🛠️ Setup

1. **Fork / push** this repo to your own GitHub account.  
2. On **Render**, create a new **Web Service** and point it at your repo.  
3. Under **Environment → Secret Files / Variables**, add:
   - `LOYVERSE_CLIENT_ID`
   - `LOYVERSE_CLIENT_SECRET`
   - `LOYVERSE_REDIRECT_URI` (e.g. `https://<service>.onrender.com/oauth/callback`)
4. Render will auto‑detect `requirements.txt` and the `Procfile`.
5. Hit **Deploy**.

## 🚀 Usage

1. Visit your Render service root URL (e.g. `https://<service>.onrender.com/`).  
   Click **“Connect to Loyverse”**.  
2. Log in and approve access.  
3. After redirect, the page will display both the **access token**            (short‑lived) and the **refresh token** (long‑lived).  
4. **Copy the refresh token** immediately and save it securely (e.g.            add it to Render as `LOYVERSE_REFRESH_TOKEN`).

## 🔒 Security Notes

* In production, never render tokens in the browser—store them server‑side.  
* Rotate secrets regularly and restrict scopes only to what your app needs.

--  
Built with ❤️ for quick prototyping.
