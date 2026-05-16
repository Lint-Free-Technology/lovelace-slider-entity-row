## [19.0.0-beta.2](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/compare/v19.0.0-beta.1...v19.0.0-beta.2) (2026-05-16)

### ⭐ New Features

* Add CSS var for slider padding ([eb29bcf](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/eb29bcf190598cef8740c549be09f62bda161199))

## [19.0.0-beta.1](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/compare/v18.1.0...v19.0.0-beta.1) (2026-05-16)

### ⚠ BREAKING CHANGES

* `--slider-entity-row-box-shadow` renamed to `--slider-entity-row-thumb-box-shadow`
* `grow` option now defaults to `true` to better align rows when `hide_state` is `true`. Set `grow: false` to not grow slider.

### ⭐ New Features

* Adjust left right padding of slider so thumb lines up with state / switch ([f21e8c5](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/f21e8c5dc1e6117f5da2f54e4b51cc20bc0291db))
* Adapt to changes in entity toggle with 2026.5.2. Add state min-width CSS var ([2bd2338](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/2bd23389d701087c0e6efce94d2fe7a90815c088))
* Add CSS slider vars for track/indicator/thumb theme colors ([#33](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/33)) ([862190c](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/862190c8e0acbcf032e44b3b4ca9dd877a427057)), closes [#29](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/29)
* Allow for setting slider tooltip distance in config (default 20). Allow for styling of slider tooltip with CSS variables. ([31cc252](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/31cc25261bc09f616dff5bb4dc6540f379269e6b)), closes [#37](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/37)
* Slider thumb hover/pressed effect with opacity being able to be set by theme CSS vars. ([191fe0b](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/191fe0b65be4e66995e91da6d53be75270dcf432)), closes [#30](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/30)

### 🐞 Bug Fixes

* Add missing `grow` option to the row editor ([#32](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/32)) ([a1d46a3](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/a1d46a34629d6dd136fe288d2bf8629017bc9ec0))

### 📔 Documentation

* Add README theme example and screenshot scenario for slider CSS variables ([#35](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/35)) ([341b914](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/341b91448042a1ead45e7ee2d18bcc45d336c111))

### ⚙️ Miscellaneous

* Default `grow` to `true` for slider rows ([#28](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/28)) ([b401fdc](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/b401fdcc0a6dc7bf06089b8a35e5a23365710cdc)), closes [#27](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/27)
* Migrate from legacy devcontainer/docker tests to ha-testcontainer scenario-based visual pipeline ([#26](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/26)) ([4cca881](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/4cca881ba07315a3f290ae72038108f89dbc8428))
* Rename CSS var `--slider-entity-row-box-shadow` to `--slider-entity-row-thumb-box-shadow` ([22524f3](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/22524f3288082738facbfc05b25e600d89d348c5))

## [18.1.0](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/compare/v18.0.1...v18.1.0) (2026-05-07)

### ⭐ New Features

* add single thumb size to CSS vars to simplify for circular thumb ([9a667a1](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/9a667a1b1104637ba3559669dc9feda47d8a1899)), closes [#19](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/19)
* Add theme vars for slider thumb size, track thickness, and thumb shadow ([#22](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/22)) ([3c5ef93](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/3c5ef93ac4ca24d578b7cadb32a351aef4caaf99))

### 🐞 Bug Fixes

* Restore state min-width: 45px to realign toggle after 2026.5.0 ([3bfeecb](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/3bfeecb49d01c6226413f652a2aed49f761e74da))

### ⚙️ Miscellaneous

* Support `color_temp_kelvin` as a first-class light attribute keeping `color_temp` as legacy alias ([[#21](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/21)](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/issues/21)) ([e2836d4](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/e2836d4aaf02f5192099776e10a43aaf60e1076a))

## [18.0.1](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/compare/v18.0.0...v18.0.1) (2026-05-04)

### 📦 Dependency Upgrades

* Update typescript to v6 and various security and build dependency updates ([b56fa75](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/b56fa753a4f4cad349c4014427b708f183abd247))

## [18.0.0](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/compare/v17.9.9...v18.0.0) (2026-05-04)

### ⭐ New Features

* **major:** Implement semantic release for build release ([b0645bf](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/b0645bfa5cf94122b948c096f05fa70b7190c7de))

### 🐞 Bug Fixes

* Toggle broken in Home Assistant 2026.5.0b0 ([d27b751](https://github.com/Lint-Free-Technology/lovelace-slider-entity-row/commit/d27b7519a1673485779817ec18b676f77d9e6838))
