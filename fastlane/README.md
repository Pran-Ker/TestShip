fastlane documentation
----

# Installation

Make sure you have the latest version of the Xcode command line tools installed:

```sh
xcode-select --install
```

For _fastlane_ installation instructions, see [Installing _fastlane_](https://docs.fastlane.tools/#installing-fastlane)

# Available Actions

## iOS

### ios register

```sh
[bundle exec] fastlane ios register
```

Create App Store Connect entry (App ID already registered in dev portal)

### ios setup_signing

```sh
[bundle exec] fastlane ios setup_signing
```

Generate & store App Store certificates/profiles (run once)

### ios beta

```sh
[bundle exec] fastlane ios beta
```

Build and ship to TestFlight

### ios add_device

```sh
[bundle exec] fastlane ios add_device
```

Register a new test device

----

This README.md is auto-generated and will be re-generated every time [_fastlane_](https://fastlane.tools) is run.

More information about _fastlane_ can be found on [fastlane.tools](https://fastlane.tools).

The documentation of _fastlane_ can be found on [docs.fastlane.tools](https://docs.fastlane.tools).
