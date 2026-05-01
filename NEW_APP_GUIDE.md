# Shipping a New iOS App to TestFlight

Everything needed to go from zero to an app on your iPhone. Steps marked **once ever** only need doing once across all apps.

---

## Prerequisites (once ever)

| What | Where | Notes |
|------|-------|-------|
| Apple Developer Program | developer.apple.com/enroll | $99/yr, takes 24–48h to activate |
| ASC API Key | appstoreconnect.apple.com → Users & Access → Integrations → API | Role: Admin. Save `.p8` to `~/.local/`, add Key ID + Issuer ID to `~/.local/secrets` |
| Private certs repo | github.com/new | Name it `certs`, keep private. One repo shared across all apps |
| App-specific password | appleid.apple.com → Security | Only needed if using Fastlane session auth (not needed with API key setup) |

---

## Per-app checklist (~10 min)

### 1. Register the App ID
developer.apple.com → Certificates, IDs & Profiles → Identifiers → **+**
- Type: App IDs → App
- Bundle ID: Explicit → `com.hebbarpran.APPNAME`
- Capabilities: leave everything unchecked unless the app needs them

### 2. Create the app in App Store Connect
appstoreconnect.apple.com → Apps → **+** → New App
- Platform: iOS
- Name: your app name
- Bundle ID: select the one just registered
- SKU: anything unique (e.g. `appname-001`)

### 3. Clone this template
```bash
cp -r ~/Developer/mobile-dev/TestShip ~/Developer/mobile-dev/APPNAME
cd ~/Developer/mobile-dev/APPNAME
rm -rf .git && git init && git add -A && git commit -m "Initial"
gh repo create Pran-Ker/APPNAME --private --source=. --remote=origin --push
```

### 4. Update identifiers
In `project.yml`:
```yaml
PRODUCT_BUNDLE_IDENTIFIER: com.hebbarpran.APPNAME
PROVISIONING_PROFILE_SPECIFIER: match AppStore com.hebbarpran.APPNAME
```

In `fastlane/Fastfile`:
```ruby
BUNDLE_ID = "com.hebbarpran.APPNAME"
```

In `fastlane/Appfile`:
```ruby
app_identifier("com.hebbarpran.APPNAME")
```

### 5. Update the app source
- Rename the app in `Sources/TestShip/` or create new source files
- Replace `TestShipApp` and `ContentView` with your app's content
- Update the app name in `project.yml` (`name:` field)

### 6. Regenerate the project
```bash
xcodegen generate
```

### 7. Set up signing (first time on this machine only)
```bash
source ~/.local/secrets && eval "$(rbenv init - zsh)"
bundle exec fastlane setup_signing
```

### 8. Ship
```bash
bundle exec fastlane beta
```

---

## After upload — two manual steps in App Store Connect

1. **Missing Compliance** — TestFlight → your build → Manage → "Does your app use encryption?" → **No**
2. **Add to group** — TestFlight → Internal Testing → Main → Builds → add the new build

Once added you'll get an email invite. Open it on your iPhone → install via TestFlight.

---

## Every subsequent ship
```bash
source ~/.local/secrets && eval "$(rbenv init - zsh)" && bundle exec fastlane beta
```
Build number increments automatically. The update appears in TestFlight on your phone within ~5 min.

---

## Credentials reference

All stored in `~/.local/secrets`:

| Variable | What it is |
|----------|-----------|
| `APPLE_ID` | hebbarpran@gmail.com |
| `APPLE_TEAM_ID` | 7M3BLC8QM2 |
| `ASC_KEY_ID` | 36756XHHXT |
| `ASC_ISSUER_ID` | 5f3b3fe4-9116-474b-a0c8-9b98c6e63c70 |
| `ASC_KEY_PATH` | ~/.local/AuthKey_36756XHHXT.p8 |
| `MATCH_PASSWORD` | passphrase for the encrypted certs repo |
| `MATCH_REPO` | https://github.com/Pran-Ker/certs.git |
