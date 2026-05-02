# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A reusable iOS app template for shipping to TestFlight via Fastlane. The `.xcodeproj` is generated from `project.yml` (XcodeGen) — never edit the `.xcodeproj` directly.

## Environment setup

Ruby is managed via rbenv (3.3.6). Always prefix Fastlane commands with the rbenv initialiser:

```bash
eval "$(rbenv init - zsh)" && bundle exec fastlane <lane>
```

Credentials come from `~/.local/secrets` — source it before running any lane:

```bash
source ~/.local/secrets
```

Required env vars: `ASC_KEY_ID`, `ASC_ISSUER_ID`, `ASC_KEY_PATH`, `MATCH_PASSWORD`.

## Common commands

```bash
# Regenerate .xcodeproj after changing project.yml
xcodegen generate

# Ship a new build to TestFlight (the only command you need day-to-day)
source ~/.local/secrets && eval "$(rbenv init - zsh)" && bundle exec fastlane beta

# First-time setup on a new machine
bundle exec fastlane setup_signing

# Register a new tester device
bundle exec fastlane add_device
```

## Architecture

- `project.yml` — single source of truth for the Xcode project (XcodeGen spec). Change bundle ID, deployment target, and build settings here.
- `Sources/TestShip/` — SwiftUI app source. `TestShipApp.swift` is the entry point, `ContentView.swift` is the root view.
- `Sources/TestShip/Info.plist` — manually maintained (not auto-generated). `CFBundleVersion` is bumped automatically by the `beta` lane via `agvtool`.
- `fastlane/Fastfile` — four lanes: `register` (once per new app), `setup_signing` (once per machine), `beta` (every ship), `add_device`.
- `fastlane/Appfile` — bundle ID, Apple ID, Team ID.
- Signing certs and profiles are stored encrypted in a private certs repo (managed by `match`). Never commit certs here.

## Signing approach

Manual signing with `match`. The `beta` lane pulls certs/profiles read-only from the certs repo, then passes explicit xcargs to xcodebuild (`CODE_SIGN_STYLE=Manual CODE_SIGN_IDENTITY="Apple Distribution"`). All Apple API calls use the ASC API key (no Apple ID password / 2FA required).

## When cloning this for a new app

1. Update `BUNDLE_ID`, `TEAM_ID` in `fastlane/Fastfile` and `fastlane/Appfile`
2. Update `PRODUCT_BUNDLE_IDENTIFIER`, `DEVELOPMENT_TEAM`, `PROVISIONING_PROFILE_SPECIFIER` in `project.yml`
3. Register the App ID at developer.apple.com (manual — API doesn't support creation)
4. Create the app in App Store Connect (manual)
5. Run `xcodegen generate` then `fastlane setup_signing` then `fastlane beta`

## TestFlight gotchas learned from first ship

- After upload, go to App Store Connect → TestFlight → build → **Manage** next to "Missing Compliance" → answer No to encryption question — required before build is testable.
- The `beta` lane tags each build as `beta/<build_number>` in git.
- Build number is auto-incremented from the latest TestFlight build number — never set it manually.
