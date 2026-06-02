# CHANGELOG

<!-- version list -->

## v1.8.0 (2026-06-02)

### Build System

- Ignore local env
  ([`85cea51`](https://github.com/brufinus/rocket-request/commit/85cea5187bf31e0951098e9b1a084dd6510ab527))

### Chores

- Fix local scripts to allow debug false
  ([`7f7f541`](https://github.com/brufinus/rocket-request/commit/7f7f54119286804d07198132366630f5e5be41ab))

### Features

- **settings**: Enable email backend and add email config
  ([`883f415`](https://github.com/brufinus/rocket-request/commit/883f41582c972d2839cd2b5127deb418d927d4c7))

- **templates**: Add error templates
  ([`023f352`](https://github.com/brufinus/rocket-request/commit/023f3525facd9d35bf27bf4c8254b11fc8dbfed6))

- **templates**: Add title block and unique titles
  ([`daed3d8`](https://github.com/brufinus/rocket-request/commit/daed3d8e394542d55778cfef6fa2e1fd7459e9e9))

### Refactoring

- **templates**: Update contact email
  ([`869200c`](https://github.com/brufinus/rocket-request/commit/869200c71c9b0cc7a1b2ecc49dfa1e2af06c1d19))

- **templates**: Update site description
  ([`cbdef20`](https://github.com/brufinus/rocket-request/commit/cbdef200e43aa0a8e93bc77ed3c508e531a847c2))


## v1.7.0 (2026-06-01)

### Bug Fixes

- **views**: Return redirect on num_silos value error
  ([`3cd1f79`](https://github.com/brufinus/rocket-request/commit/3cd1f7933a5ad4fc78cc713d1532422c514bb68c))

### Features

- **api**: Add function to validate item count
  ([`4c7c2aa`](https://github.com/brufinus/rocket-request/commit/4c7c2aafcf023eb6c3ab286acb712c669e75a73f))

- **js**: Show error on max count
  ([`4c7c2aa`](https://github.com/brufinus/rocket-request/commit/4c7c2aafcf023eb6c3ab286acb712c669e75a73f))

- **views**: Add server validation on blueprint string length
  ([`8edc5e5`](https://github.com/brufinus/rocket-request/commit/8edc5e50c152fcce139063633ece2a6b023629a0))

- **views**: Add server validation on max num_silos
  ([`4721455`](https://github.com/brufinus/rocket-request/commit/4721455b5dff3144d9465998641d9e32bc99d6d7))

- **views**: Track total item count for validation
  ([`4c7c2aa`](https://github.com/brufinus/rocket-request/commit/4c7c2aafcf023eb6c3ab286acb712c669e75a73f))

### Refactoring

- **templates**: Lower item count input form validation
  ([`49bd32b`](https://github.com/brufinus/rocket-request/commit/49bd32bdc5b814910739081d434bcdd67561c204))


## v1.6.1 (2026-05-31)

### Bug Fixes

- **settings**: Set name to persist cookie
  ([`9010146`](https://github.com/brufinus/rocket-request/commit/90101462da3f3c2c01b1b8e7a0aa43eadd1320dc))

### Build System

- Initialize firebase
  ([`326de5d`](https://github.com/brufinus/rocket-request/commit/326de5def69293b2349de7a2946c12133af33dd3))

### Continuous Integration

- **cd**: Build with service account
  ([`0d964ad`](https://github.com/brufinus/rocket-request/commit/0d964ad5f4fa406140334611340f212f1a6714c9))


## v1.6.0 (2026-05-31)

### Bug Fixes

- **templates**: Increase blueprint import maxlength
  ([`e1436e6`](https://github.com/brufinus/rocket-request/commit/e1436e6536079787f9c4025a9c7124dfcefc84da))

### Continuous Integration

- **cd**: Use auth service account
  ([`5ebc241`](https://github.com/brufinus/rocket-request/commit/5ebc241f6f924b3bd7a0a3676c7d60f3fc5479ab))

### Documentation

- **project**: Add web app info
  ([`43a8eb6`](https://github.com/brufinus/rocket-request/commit/43a8eb6dd2f64b4ccdce484f2a589281fcc291aa))

### Features

- **templates**: Add usage info to about page
  ([`88bfdfe`](https://github.com/brufinus/rocket-request/commit/88bfdfeb45c0be36f2d83a6c74816c35397e44ca))

### Refactoring

- **urls**: Move app to root url
  ([`a7750df`](https://github.com/brufinus/rocket-request/commit/a7750dfbd79ad2995b970708a061e2782902ac22))


## v1.5.0 (2026-05-30)

### Bug Fixes

- **js**: Render image using dynamic static path
  ([`d53849c`](https://github.com/brufinus/rocket-request/commit/d53849cc22e76ecccadd278151caaa297fb9b14a))

### Build System

- Add gcloud scripts and config
  ([`c365700`](https://github.com/brufinus/rocket-request/commit/c3657006b3c8ca2a1ea9f97fe0c2520306b3e3bd))

- Add gcloudignore and remove unused config
  ([`c365700`](https://github.com/brufinus/rocket-request/commit/c3657006b3c8ca2a1ea9f97fe0c2520306b3e3bd))

- Migrate with beta deploy
  ([`c365700`](https://github.com/brufinus/rocket-request/commit/c3657006b3c8ca2a1ea9f97fe0c2520306b3e3bd))

- **cd**: Remove build command
  ([`7e06ee1`](https://github.com/brufinus/rocket-request/commit/7e06ee1cdadad22c3f31e98cd2b672ed033a4e86))

### Continuous Integration

- **cd**: Add gcloud build and deploy job
  ([`c260d1d`](https://github.com/brufinus/rocket-request/commit/c260d1da4097d10008dafa15562df36ee89dd3b1))

- **quality**: Update setup for structure
  ([`34bb655`](https://github.com/brufinus/rocket-request/commit/34bb655b64baae6914cb25eeae1b84e5bb93a23e))

### Documentation

- **project**: Add issue templates
  ([`e3c3d86`](https://github.com/brufinus/rocket-request/commit/e3c3d860debe4ef10906668772e73f626b12423b))

- **project**: Update usage info
  ([`34bb655`](https://github.com/brufinus/rocket-request/commit/34bb655b64baae6914cb25eeae1b84e5bb93a23e))

### Features

- **templates**: Add context processor to inject build version
  ([`88503ca`](https://github.com/brufinus/rocket-request/commit/88503ca21f494f3a0684b21fa307f67ae29970e5))

### Refactoring

- Move js into sub dir
  ([`6bde8be`](https://github.com/brufinus/rocket-request/commit/6bde8be0c51c3c47f21ce81cf63ee59be4e5c910))

- **project**: Move app and project up to base dir
  ([`34bb655`](https://github.com/brufinus/rocket-request/commit/34bb655b64baae6914cb25eeae1b84e5bb93a23e))


## v1.4.0 (2026-05-26)

### Build System

- Include build date file
  ([`09e5c2c`](https://github.com/brufinus/rocket-request/commit/09e5c2c9202efdad374b3f89acfc3f569ecb309b))

### Continuous Integration

- **cd**: Warn on missing artifacts
  ([`273f717`](https://github.com/brufinus/rocket-request/commit/273f7178674ad9ac6357aabc78b2199995b51d98))

### Features

- **templates**: Add tooltip warning on import
  ([`f4bbd88`](https://github.com/brufinus/rocket-request/commit/f4bbd88b82a4d42e79311ae5953a4c2ecc7376a3))


## v1.3.0 (2026-05-26)

### Features

- Set updated date with custom context processor
  ([`acbe9bd`](https://github.com/brufinus/rocket-request/commit/acbe9bdccf8df148352b308485f121250db02049))


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
