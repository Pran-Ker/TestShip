# TestFlight Ship Checklist

A reusable checklist for going from zero → app on your iPhone via TestFlight.
Do the **one-time** steps once ever, the **per-app** steps for every new app.

---

## One-Time (account setup)

- [ ] **Enroll in Apple Developer Program** — $99/yr  
  https://developer.apple.com/programs/enroll/
- [ ] **Create a private GitHub repo for certs** (used by Fastlane `match`)  
  Name it something like `{yourname}-certs` — keep it private
- [ ] **Generate an App-Specific Password**  
  appleid.apple.com → Sign-In and Security → App-Specific Passwords  
  → paste into `.env` as `FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD`
- [ ] **Find your Team ID**  
  developer.apple.com → Account → Membership → Team ID (10 chars)

---

## Per-App Steps

### 1. Configure this repo
- [ ] Replace every `YOURNAME` in `project.yml`, `fastlane/Appfile`, `fastlane/Fastfile`
- [ ] Replace `XXXXXXXXXX` with your Team ID in the same files
- [ ] Set `MATCH_REPO` in `Fastfile` to your private certs repo URL
- [ ] Fill in `.env` (copy from `.env.example`)

### 2. Register the App ID
- [ ] Go to developer.apple.com → Certificates, IDs & Profiles → Identifiers → +  
  Type: App ID | Bundle ID: `com.YOURNAME.testship` (Explicit)

### 3. Create app in App Store Connect
- [ ] apps.apple.com/apps → + → New App  
  Platform: iOS | Bundle ID: select the one you just registered  
  Name: TestShip | Primary Language: English | SKU: testship-001

### 4. Run local setup
```bash
./scripts/setup.sh
bundle exec fastlane setup_signing   # generates + stores certs in your cert repo
```

### 5. Ship to TestFlight
```bash
bundle exec fastlane beta
```
- Build appears in App Store Connect → TestFlight in ~5 min
- Add yourself as internal tester → Apple sends TestFlight invite email
- Open TestFlight on your iPhone → Install

### 6. For each new ship
```bash
bundle exec fastlane beta   # auto-increments build number, uploads
```

---

## For future new apps — what to reuse

| Asset | Reusable? | Action |
|-------|-----------|--------|
| Apple Developer account | ✅ | Nothing |
| Cert repo (`match`) | ✅ | Point new app's Fastfile at same repo |
| App-Specific Password | ✅ | Copy to new app's `.env` |
| `Fastfile` template | ✅ | Copy, change `BUNDLE_ID` |
| `project.yml` template | ✅ | Copy, change bundle ID + app name |
| App ID | ❌ | Register new one per app |
| App Store Connect entry | ❌ | Create new one per app |

**Estimated time for second+ app: ~10 minutes end-to-end.**
