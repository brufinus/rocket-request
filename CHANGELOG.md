# CHANGELOG

<!-- version list -->

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
