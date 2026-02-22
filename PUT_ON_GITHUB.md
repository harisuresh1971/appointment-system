# Put this project on GitHub (then deploy to Render)

Your project is already a **git repo** with one commit. Follow these steps to get it on GitHub and then deploy.

---

## Step 1: Create a new repo on GitHub

1. Open **https://github.com/new**
2. **Repository name:** e.g. `appointment-system` (or any name you like)
3. Leave **Public** selected. Do **not** check "Add a README" (you already have one).
4. Click **Create repository**.

---

## Step 2: Push your code from your PC

GitHub will show you commands. Use these (replace `YOUR_USERNAME` and `REPO_NAME` with your GitHub username and repo name):

```bash
cd "c:\Users\harih\OneDrive\Desktop\project cursor"

git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

Example: if your username is `harih` and repo name is `appointment-system`:

```bash
git remote add origin https://github.com/harih/appointment-system.git
git branch -M main
git push -u origin main
```

When prompted, sign in to GitHub (browser or token).

---

## Step 3: Deploy on Render

1. Go to **https://dashboard.render.com** and sign in with GitHub.
2. Click **New** → **Blueprint**.
3. Select the repo you just pushed (e.g. `appointment-system`).
4. Click **Apply**. Render will create the database and web service from `render.yaml`.
5. When the deploy finishes, your app link will be:
   **https://appointment-system.onrender.com** (or the name you gave the service).

Done. Open the link, register, and use the app.
