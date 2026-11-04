# Login setup checklist (to be done by Yawar)

The login page (`/login/`) is live in the code, but Google and phone
sign-in need accounts that only you can create. **Until you finish the
steps below, the Google and phone buttons on the login page will show
"not configured yet" and email + password sign-in works regardless.**

---

## A. Google sign-in (one-time, about 10 minutes)

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
   and create (or open) a project, for example "birds-of-paradise".
2. Open **APIs & Services > Credentials** and click
   **Create Credentials > OAuth client ID**.
3. Choose application type **Web application**.
4. Under **Authorized redirect URIs**, add BOTH of these exactly
   (the login code builds the callback URL from the site's address,
   and Google only accepts URIs you have registered here):

   - `https://www.birdsofparadise.in/auth/google/callback/`
   - `https://kashmir-birds-ai.onrender.com/auth/google/callback/`

5. Google will show you a **Client ID** and a **Client secret**.
6. In the [Render dashboard](https://dashboard.render.com/), open your
   `kashmir-birds-ai` web service, go to **Environment**, and add two
   environment variables:

   - `GOOGLE_OAUTH_CLIENT_ID` = your Client ID
   - `GOOGLE_OAUTH_CLIENT_SECRET` = your Client secret

7. Save. Render redeploys automatically. After the deploy, the
   "Continue with Google" button on `/login/` will be active.

---

## B. Phone OTP sign-in via Firebase (one-time, about 15 minutes)

1. Go to the [Firebase Console](https://console.firebase.google.com/)
   and create a project, for example "birds-of-paradise".
2. Open **Build > Authentication**, click **Get started**, and under
   **Sign-in method** enable **Phone**.
3. In the Firebase Console go to **Project settings** and add a
   **Web app** (the `</>` icon). Firebase will show you a config
   containing `apiKey`, `authDomain`, `projectId` and `appId`.
4. Still in **Project settings > Service accounts**, click
   **Generate new private key** and download the JSON file. Keep this
   file private; it lets the server verify phone tokens.
5. In the Render dashboard (**Environment** for the
   `kashmir-birds-ai` service), add these variables:

   - `FIREBASE_API_KEY` = the `apiKey` from step 3
   - `FIREBASE_AUTH_DOMAIN` = the `authDomain` from step 3
   - `FIREBASE_PROJECT_ID` = the `projectId` from step 3
   - `FIREBASE_APP_ID` = the `appId` from step 3
   - `FIREBASE_SERVICE_ACCOUNT_JSON` = the entire contents of the
     JSON file from step 4 (paste it as one line)

6. Save. Render redeploys automatically. After the deploy, the
   "Continue with Phone number" button on `/login/` will be active.

Note: Firebase phone sign-in may ask you to upgrade the Firebase
project to the Blaze (pay-as-you-go) plan for SMS; the free tier
includes a monthly SMS allowance, and the console will show your
usage.

---

## What works before you do any of this

- The home page (`/`) stays public, with no login needed.
- Every other page redirects visitors to `/login/`.
- Anyone can create an account on `/login/` with an email and a
  password and sign in immediately.
- The Google and phone buttons stay visible but greyed out with a
  "not configured yet" note until you finish the matching section
  above.
