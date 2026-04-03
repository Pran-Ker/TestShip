#!/usr/bin/env bash
# Run once after cloning to set up the development environment.
set -euo pipefail

echo "==> Checking prerequisites..."

# Xcode
if ! xcode-select -p &>/dev/null || [ "$(xcode-select -p)" = "/Library/Developer/CommandLineTools" ]; then
  echo "ERROR: Full Xcode required. Install from the Mac App Store, then:"
  echo "  sudo xcode-select -s /Applications/Xcode.app/Contents/Developer"
  exit 1
fi
echo "  Xcode: $(xcodebuild -version | head -1)"

# XcodeGen
if ! command -v xcodegen &>/dev/null; then
  echo "==> Installing XcodeGen..."
  brew install xcodegen
fi

# Bundler / Fastlane
if ! command -v bundle &>/dev/null; then
  echo "==> Installing Bundler..."
  gem install bundler
fi
echo "==> Installing Gems..."
bundle install

# Generate .xcodeproj from project.yml
echo "==> Generating Xcode project..."
xcodegen generate

# .env check
if [ ! -f .env ]; then
  cp .env.example .env
  echo ""
  echo "  IMPORTANT: Fill in .env before running 'bundle exec fastlane setup_signing'"
fi

echo ""
echo "Done! Next steps:"
echo "  1. Edit .env with your credentials"
echo "  2. bundle exec fastlane setup_signing   # first time only — creates certs + profiles"
echo "  3. bundle exec fastlane beta            # build + ship to TestFlight"
