# CHANGELOG

<!-- version list -->

## v1.2.0 (2026-05-25)

### Bug Fixes

- **api**: Raise an exception when items exceed available chest slots
  ([`dc82836`](https://github.com/brufinus/rocket-request/commit/dc8283659a3934782ff92c42299854df16a4f613))

- **views**: Handle ChestIndexException and pass error to blueprint export
  ([`79ebb72`](https://github.com/brufinus/rocket-request/commit/79ebb72a133ab82dcea2f2072616ea66e0afca61))

- **views**: Validate int types
  ([`500edf0`](https://github.com/brufinus/rocket-request/commit/500edf02bfa1d499070052cc51f19dca11d18702))

### Chores

- **project**: Remove unused editable requirements
  ([`fa1f826`](https://github.com/brufinus/rocket-request/commit/fa1f8269bc6688765a2fa30e37317920e8d82182))

### Continuous Integration

- **cd**: Dynamically set displayed updated date
  ([`05e76e3`](https://github.com/brufinus/rocket-request/commit/05e76e313c5e65f40c8563954c87cba70107aaf0))

- **cd**: Get app id and set checkout token
  ([`a81565a`](https://github.com/brufinus/rocket-request/commit/a81565aa28f55cc9733966a201181875dc2827d9))

- **cd**: Use app to create deploy token
  ([`a81565a`](https://github.com/brufinus/rocket-request/commit/a81565aa28f55cc9733966a201181875dc2827d9))

### Documentation

- **project**: Add security policy
  ([`7454f91`](https://github.com/brufinus/rocket-request/commit/7454f9128a0ea2762205f50c9ad6083a53569b7b))

- **views**: Verbose docstrings
  ([`2347014`](https://github.com/brufinus/rocket-request/commit/234701467573bd2629ada60ff2c57947bd7a80ae))

### Features

- **static**: Implement paste functionality
  ([`6c6f418`](https://github.com/brufinus/rocket-request/commit/6c6f418a7aaadb83660a89090f1463096ff86ed2))

### Refactoring

- **views**: Remove unused code
  ([`2347014`](https://github.com/brufinus/rocket-request/commit/234701467573bd2629ada60ff2c57947bd7a80ae))


## v1.1.0 (2026-05-24)

### Bug Fixes

- **api**: Handle conversion exceptions
  ([`e2d8a18`](https://github.com/brufinus/rocket-request/commit/e2d8a18bf6b68936440b75cef13585777f8241ba))

- **css**: Set bottom padding for blueprint form
  ([`4f505fb`](https://github.com/brufinus/rocket-request/commit/4f505fbec7770eed36eca107feb4fbff205b23f8))

- **css**: Set font for text input and area
  ([`9c13ad8`](https://github.com/brufinus/rocket-request/commit/9c13ad877959311f963e1fa45d9a49cbf703ad0c))

- **data**: Give cryo plant a unique id and remove cheat items
  ([`fd089b9`](https://github.com/brufinus/rocket-request/commit/fd089b93d0049c7d90253b476fd672245f980322))

- **data**: Use in-game names
  ([`9d2fd52`](https://github.com/brufinus/rocket-request/commit/9d2fd524156246fb24d0758b9fdbe0932500d1f7))

- **views**: Handle blueprint import errors
  ([`3a0b2ae`](https://github.com/brufinus/rocket-request/commit/3a0b2ae8c72a9d1dae8ffc756deca61bd4f30e3b))

### Chores

- Add scripts for local development
  ([`3727830`](https://github.com/brufinus/rocket-request/commit/37278307a0552b92a26d2c8eb4879d526bb557f4))

- Add shebangs to dev scripts
  ([`3727830`](https://github.com/brufinus/rocket-request/commit/37278307a0552b92a26d2c8eb4879d526bb557f4))

- Enable parallel testing
  ([`c08617c`](https://github.com/brufinus/rocket-request/commit/c08617c8d63e12bd4d714191d19f98a66712878c))

- Settings docstring
  ([`c08617c`](https://github.com/brufinus/rocket-request/commit/c08617c8d63e12bd4d714191d19f98a66712878c))

### Continuous Integration

- **quality**: Run integration tests
  ([`684a7e9`](https://github.com/brufinus/rocket-request/commit/684a7e9a96f7edf07f1d6f828d77a0b1312bb981))

- **quality**: Set permissions
  ([`684a7e9`](https://github.com/brufinus/rocket-request/commit/684a7e9a96f7edf07f1d6f828d77a0b1312bb981))

### Documentation

- **api**: Add blueprint module header
  ([`f117124`](https://github.com/brufinus/rocket-request/commit/f1171244732615533e7cf2e4167d9b8e571c8b96))

- **project**: Add runtests usage
  ([`d5b20df`](https://github.com/brufinus/rocket-request/commit/d5b20df1fdb64ed3a05af1ee7b00345050cbe4a5))

- **project**: Run.sh usage
  ([`edb7f1f`](https://github.com/brufinus/rocket-request/commit/edb7f1f7ec7871ad11e7147278f9d6b304e11d8b))

### Features

- **api**: Add blueprint book metadata
  ([`f5c8530`](https://github.com/brufinus/rocket-request/commit/f5c8530cd6ab09a45e72dba66c5e0ca9691d6912))

- **api**: Add blueprint string converter
  ([`5e8c82c`](https://github.com/brufinus/rocket-request/commit/5e8c82c1a5f5a8f6b0d2db325352f302108bcec9))

- **api**: Add module for generating blueprint strings
  ([`6593730`](https://github.com/brufinus/rocket-request/commit/6593730ab04c644a30fe8dad6e5a330f418526b6))

- **api**: Build a full blueprint string and pass it to results
  ([`d204c67`](https://github.com/brufinus/rocket-request/commit/d204c67cf0877d56056c515b3250f15455c527f2))

- **api**: Implement blueprint import
  ([`2a0f409`](https://github.com/brufinus/rocket-request/commit/2a0f4099ab85a9eede9889841c9adb317b1d19b4))

- **exceptions**: Add exceptions module
  ([`a2d3b92`](https://github.com/brufinus/rocket-request/commit/a2d3b92b46bac3f39a2c4047d275baba933693a9))

- **templates**: Add blueprint viewer with copy button
  ([`e9af11f`](https://github.com/brufinus/rocket-request/commit/e9af11f16a915d1106c199f2acd88d0a348af238))

- **templates**: Create form for blueprint import
  ([`bc458e7`](https://github.com/brufinus/rocket-request/commit/bc458e7dd270963e68233c1c9a25be9233e45c05))


## v1.0.1 (2026-05-18)

### Bug Fixes

- **api**: Increment start index if new silo load is immediately capped
  ([`565de29`](https://github.com/brufinus/rocket-request/commit/565de29d69953b6811244a9bbbe67bb30b1016a6))

### Build System

- **dev**: Add various dev options to run script
  ([`0d82e5f`](https://github.com/brufinus/rocket-request/commit/0d82e5f5073d9541b49c58510d27e5fd344c2883))

- **dev**: Clean dist prior to build
  ([`3e676b4`](https://github.com/brufinus/rocket-request/commit/3e676b4e443d0781d50b76994d24d9934b027648))

### Chores

- **config**: Update ide config
  ([`98b9096`](https://github.com/brufinus/rocket-request/commit/98b90960c7e131184418217b83135344eca489d8))

### Continuous Integration

- **cd**: Add release workflow
  ([`2eff556`](https://github.com/brufinus/rocket-request/commit/2eff556dd33d254773ed50709a17b96edbfd56d0))

- **cd**: Install build
  ([`cc5aca0`](https://github.com/brufinus/rocket-request/commit/cc5aca09edd7b2450b702cd834266967f4ef8096))

- **quality**: Set working directory for run steps
  ([`9f8c6e0`](https://github.com/brufinus/rocket-request/commit/9f8c6e0cdbd7e4bff864fe28efa7dc95d5fab802))

### Documentation

- **api**: Fix return spec
  ([`76560e2`](https://github.com/brufinus/rocket-request/commit/76560e2139505f9e2863258e9dcba4b0c47160c6))

- **project**: Add commit specs
  ([`840e2bd`](https://github.com/brufinus/rocket-request/commit/840e2bd3f2b5235020bfc615d51f5810d8bab608))

- **project**: Fix run steps
  ([`75c25c3`](https://github.com/brufinus/rocket-request/commit/75c25c3e006d0fbc54ae75ac3687edc32cc4ac64))

### Performance Improvements

- **api**: Keep track of which index to start iterating over the list of silos
  ([`38b5ba6`](https://github.com/brufinus/rocket-request/commit/38b5ba6937b16354282c1963a193dae9b83051a4))

- **api**: Skip trying to add items to silos at max capacity
  ([`fc38f95`](https://github.com/brufinus/rocket-request/commit/fc38f95fed3bf555a81c255643d2d4a30ef3b67e))

### Refactoring

- **api**: Condense code by removing the intermediate find_open_silo function
  ([`76560e2`](https://github.com/brufinus/rocket-request/commit/76560e2139505f9e2863258e9dcba4b0c47160c6))

- **api**: Remove unused return value
  ([`76560e2`](https://github.com/brufinus/rocket-request/commit/76560e2139505f9e2863258e9dcba4b0c47160c6))


## v1.0.0 (2026-05-17)

- Initial Release
