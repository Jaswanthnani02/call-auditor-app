# Deploying to Streamlit Cloud

Follow these steps to deploy your Call Auditor App to the web.

## 1. Prepare for GitHub
I have already generated the `requirements.txt` and updated `.gitignore` for you.

1.  **Initialize Git** (if not done):
    ```bash
    git init
    git add .
    git commit -m "Initial commit of Call Auditor App"
    ```

2.  **Create a Repository on GitHub**:
    - Go to [GitHub.com](https://github.com/new).
    - Crate a new repository (e.g., `call-auditor-app`).
    - **Do not** initialize with README or .gitignore (we have them).

3.  **Push Code**:
    Follow the commands shown by GitHub, typically:
    ```bash
    git branch -M main
    git remote add origin https://github.com/YOUR_USERNAME/call-auditor-app.git
    git push -u origin main
    ```

## 2. Deploy on Streamlit Cloud

1.  Go to [share.streamlit.io](https://share.streamlit.io/).
2.  Click **"New app"**.
3.  Select your GitHub repository (`call-auditor-app`).
4.  Set the **Main file path** to `app.py`.
5.  Click **"Deploy!"**.

## 3. Configure Secrets (Important!)

Your app needs the `API_KEY` to work.

1.  On your app dashboard in Streamlit Cloud, click the **Settings** (three dots) > **Settings**.
2.  Go to the **Secrets** tab.
3.  Paste your API key in TOML format:
    ```toml
    API_KEY = "your_actual_api_key_here"
    ```
4.  Click **Save**.

Your app should now be live and working!
