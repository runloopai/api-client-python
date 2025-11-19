# Changelog

## 0.68.0 (2025-11-19)

Full Changelog: [v0.67.0...v0.68.0](https://github.com/runloopai/api-client-python/compare/v0.67.0...v0.68.0)

### Features

* **blueprints:** Cleanup the BuildContext API ([#6407](https://github.com/runloopai/api-client-python/issues/6407))\n\nTest ([c87b986](https://github.com/runloopai/api-client-python/commit/c87b986e558ad3a0cca2ad1609b9833baf86fef8))
* **blueprints:** prevent deletion of blueprints with dependent snapshots ([ce55350](https://github.com/runloopai/api-client-python/commit/ce55350d81f7f5ba3a3aff8faea88c0e1366cea9))
* **object:** Added ability to give objects a Time To Live, after which they are automatically deleted.\nfeat(blueprints): Added the ability to attach objects as build contexts that can be referenced in your Dockerfile. ([f2bc83c](https://github.com/runloopai/api-client-python/commit/f2bc83c126696aea224bb5978294fc3362a94eeb))


### Bug Fixes

* compat with Python 3.14 ([a52802a](https://github.com/runloopai/api-client-python/commit/a52802a6d12d96c3bf4bd670e77c9ec50d08b459))
* **compat:** update signatures of `model_dump` and `model_dump_json` for Pydantic v1 ([50340b2](https://github.com/runloopai/api-client-python/commit/50340b20148f72cb645bba0bafde6f902e063425))
* **snapshot:** added "deleted" status to DevboxSnapshotStatus enum \n fix(storage-object): added ObjectState enum, fixed createObject() to appropriately type content_type and state as the respective enums ([7c26593](https://github.com/runloopai/api-client-python/commit/7c265936088c074d00bd3c65b52dde5dcde3ccfb))


### Chores

* **package:** drop Python 3.8 support ([07a0b8c](https://github.com/runloopai/api-client-python/commit/07a0b8c1825c78b0a6c30c2d374b82aced2f97d5))
* **package:** drop Python 3.8 support ([d67abf1](https://github.com/runloopai/api-client-python/commit/d67abf1c52a089e192987a261e69219d60514bc3))

## 0.67.0 (2025-11-14)

Full Changelog: [v0.66.1...v0.67.0](https://github.com/runloopai/api-client-python/compare/v0.66.1...v0.67.0)

### Features

* **api:** api update ([516c20b](https://github.com/runloopai/api-client-python/commit/516c20b3095d7e75b0e15647621bf92e0d79f5f4))
* **blueprint:** adds queued state ([5893559](https://github.com/runloopai/api-client-python/commit/5893559e8839260876947d31f1090dd343f1cf43))


### Bug Fixes

* **client:** close streams without requiring full consumption ([30f9ee5](https://github.com/runloopai/api-client-python/commit/30f9ee5b6cc5f42ce642b918c4e0194a4ab8bc7a))


### Chores

* **internal/tests:** avoid race condition with implicit client cleanup ([7152280](https://github.com/runloopai/api-client-python/commit/71522809d211f5bbad89be807559ca2de591729f))
* **internal:** grammar fix (it's -&gt; its) ([fd6963f](https://github.com/runloopai/api-client-python/commit/fd6963f1777dedc2db5b86dc222a5e70521134ba))
* **package:** drop Python 3.8 support ([5026669](https://github.com/runloopai/api-client-python/commit/50266693caae9b3c6e6506cb58f096f1d439dcd0))

## 0.66.1 (2025-10-23)

Full Changelog: [v0.66.0...v0.66.1](https://github.com/runloopai/api-client-python/compare/v0.66.0...v0.66.1)

## 0.66.0 (2025-10-23)

Full Changelog: [v0.65.0...v0.66.0](https://github.com/runloopai/api-client-python/compare/v0.65.0...v0.66.0)

### Features

* **api:** api update ([a0f1f40](https://github.com/runloopai/api-client-python/commit/a0f1f402b1f403fbe439bdebd9f96d5069c5fdf9))


### Chores

* bump `httpx-aiohttp` version to 0.1.9 ([8d29288](https://github.com/runloopai/api-client-python/commit/8d29288a957e7a8d14dfb4e4cfaf4d6345dbaf41))

## 0.65.0 (2025-10-15)

Full Changelog: [v0.64.0...v0.65.0](https://github.com/runloopai/api-client-python/compare/v0.64.0...v0.65.0)

### Features

* **api:** api update ([e6de5c0](https://github.com/runloopai/api-client-python/commit/e6de5c068a75512dd89a9240c281f46c69f14f07))


### Chores

* **internal:** detect missing future annotations with ruff ([e8914e3](https://github.com/runloopai/api-client-python/commit/e8914e3d40f6bbed2175d39f25e3b1da1c350225))

## 0.64.0 (2025-10-06)

Full Changelog: [v0.63.0...v0.64.0](https://github.com/runloopai/api-client-python/compare/v0.63.0...v0.64.0)

### Features

* **api:** api update ([b13e49f](https://github.com/runloopai/api-client-python/commit/b13e49f006c45d3e10c0383825fbe2054b31b351))
* **api:** api update ([736c122](https://github.com/runloopai/api-client-python/commit/736c122c5a350ba081eb495786e94ad6b999b121))
* **api:** api update ([c4dbcf3](https://github.com/runloopai/api-client-python/commit/c4dbcf33822da8045def9617948e7b30f617fe51))

## 0.63.0 (2025-10-02)

Full Changelog: [v0.62.0...v0.63.0](https://github.com/runloopai/api-client-python/compare/v0.62.0...v0.63.0)

### Features

* **api:** api update ([dbf7a2e](https://github.com/runloopai/api-client-python/commit/dbf7a2ea929d3832faec4241f8b8831c97c1755a))
* **api:** api update ([fff1e21](https://github.com/runloopai/api-client-python/commit/fff1e210bf02f2a8be0cb7fc6d2fe0b04e28bf03))

## 0.62.0 (2025-10-01)

Full Changelog: [v0.61.0...v0.62.0](https://github.com/runloopai/api-client-python/compare/v0.61.0...v0.62.0)

### Features

* **api:** api update ([a2ed6d7](https://github.com/runloopai/api-client-python/commit/a2ed6d7530f8ea05f600713163ac646989426a65))
* **api:** api update ([59b9486](https://github.com/runloopai/api-client-python/commit/59b9486f94c15ec76021ec98db3dad93225be663))
* **api:** api update ([8d62f4b](https://github.com/runloopai/api-client-python/commit/8d62f4b5018b52f3d813b8f6a1f3e5460b80e368))

## 0.61.0 (2025-09-29)

Full Changelog: [v0.60.1...v0.61.0](https://github.com/runloopai/api-client-python/compare/v0.60.1...v0.61.0)

### Features

* **api:** api update ([6c66922](https://github.com/runloopai/api-client-python/commit/6c669226f72692500161d8cef6e9220fb474d748))
* **api:** api update ([249f9d2](https://github.com/runloopai/api-client-python/commit/249f9d264e0f376bacdc2dc5625eb58f9ecd1adf))
* **api:** api update ([6c9ba20](https://github.com/runloopai/api-client-python/commit/6c9ba20394ae5d5db138048cc95d6106fa6aeca3))


### Chores

* do not install brew dependencies in ./scripts/bootstrap by default ([d5ba1be](https://github.com/runloopai/api-client-python/commit/d5ba1beccdfc925274d91c225ff1141177978bdc))
* **internal:** update pydantic dependency ([baecb39](https://github.com/runloopai/api-client-python/commit/baecb39b0f1d647a42dc40338215ddfabdcc2bbf))
* **types:** change optional parameter type from NotGiven to Omit ([783fea5](https://github.com/runloopai/api-client-python/commit/783fea55e782d391c0f4332908e86b16ec318bd4))

## 0.60.1 (2025-09-11)

Full Changelog: [v0.60.0...v0.60.1](https://github.com/runloopai/api-client-python/compare/v0.60.0...v0.60.1)

## 0.60.0 (2025-09-10)

Full Changelog: [v0.59.0...v0.60.0](https://github.com/runloopai/api-client-python/compare/v0.59.0...v0.60.0)

### Features

* **api:** api update ([82b7001](https://github.com/runloopai/api-client-python/commit/82b700156bc034cb486225ef2889b7f3b7575c9e))
* **api:** api update ([5d1797b](https://github.com/runloopai/api-client-python/commit/5d1797b1e193ffd5b17c664fdf3894a568039c14))
* **api:** api update ([f9e63d9](https://github.com/runloopai/api-client-python/commit/f9e63d96beac3fcdfda3b1038683ebf514b421d7))

## 0.59.0 (2025-09-08)

Full Changelog: [v0.58.0...v0.59.0](https://github.com/runloopai/api-client-python/compare/v0.58.0...v0.59.0)

### Features

* **api:** api update ([d28f600](https://github.com/runloopai/api-client-python/commit/d28f60090e9c8c3c508812bfaf4bacbdd0b64330))
* **api:** api update ([a7b44bc](https://github.com/runloopai/api-client-python/commit/a7b44bc091060518d507dbd806694de9ba09c1f8))
* **api:** api update ([39c93bd](https://github.com/runloopai/api-client-python/commit/39c93bd7061e77c01fbb1cd913ede94ce90664c4))


### Chores

* **internal:** codegen related update ([4ed8b7a](https://github.com/runloopai/api-client-python/commit/4ed8b7a3ab98378214f74e79202051260f8488da))
* **tests:** simplify `get_platform` test ([6b38a37](https://github.com/runloopai/api-client-python/commit/6b38a37e0e3630b360090fd4ab91b4ffc431c46c))

## 0.58.0 (2025-09-04)

Full Changelog: [v0.57.0...v0.58.0](https://github.com/runloopai/api-client-python/compare/v0.57.0...v0.58.0)

### Features

* **api:** api update ([59e649d](https://github.com/runloopai/api-client-python/commit/59e649db1632c06c7c6b7cdabaf7e42e003daa09))
* improve future compat with pydantic v3 ([adb9765](https://github.com/runloopai/api-client-python/commit/adb97652aea509e832ab50f25d7e04e80d8fd09e))
* **types:** replace List[str] with SequenceNotStr in params ([9c3bbcd](https://github.com/runloopai/api-client-python/commit/9c3bbcdfdaedcf60d9829bc3cad83f89c9add98a))


### Chores

* **internal:** add Sequence related utils ([dec07b5](https://github.com/runloopai/api-client-python/commit/dec07b5258bc057375c8412c76f0a7f29f12b723))

## 0.57.0 (2025-08-27)

Full Changelog: [v0.56.2...v0.57.0](https://github.com/runloopai/api-client-python/compare/v0.56.2...v0.57.0)

### Features

* **api:** api update ([3a5d31a](https://github.com/runloopai/api-client-python/commit/3a5d31a6eafb76cf8013355ba22676945509681f))
* **api:** api update ([104af9f](https://github.com/runloopai/api-client-python/commit/104af9fd5482701947186669748098b060715748))


### Bug Fixes

* avoid newer type syntax ([3412f2b](https://github.com/runloopai/api-client-python/commit/3412f2b11594e35ef48e4b283a9306eb645af6b3))


### Chores

* **internal:** change ci workflow machines ([b01847c](https://github.com/runloopai/api-client-python/commit/b01847caa9adcebfc4447c10c3723451dcb140a1))
* **internal:** update pyright exclude list ([0da3132](https://github.com/runloopai/api-client-python/commit/0da3132fb19d9e1aac3770415b72fb1b413f3175))

## 0.56.2 (2025-08-25)

Full Changelog: [v0.56.1-beta...v0.56.2](https://github.com/runloopai/api-client-python/compare/v0.56.1-beta...v0.56.2)

### Chores

* update github action ([d0a51b8](https://github.com/runloopai/api-client-python/commit/d0a51b81c7cda9e63bc4c6a314effbdfadacd7b2))

## 0.56.1-beta (2025-08-21)

Full Changelog: [v0.55.2...v0.56.1-beta](https://github.com/runloopai/api-client-python/compare/v0.55.2...v0.56.1-beta)

### Features

* **api:** api update ([9ad6951](https://github.com/runloopai/api-client-python/commit/9ad69513705ef867763ef306c15af777de542437))

## 0.55.2 (2025-08-19)

Full Changelog: [v0.55.1...v0.55.2](https://github.com/runloopai/api-client-python/compare/v0.55.1...v0.55.2)

## 0.55.1 (2025-08-19)

Full Changelog: [v0.55.0...v0.55.1](https://github.com/runloopai/api-client-python/compare/v0.55.0...v0.55.1)

## 0.55.0 (2025-08-19)

Full Changelog: [v0.54.0...v0.55.0](https://github.com/runloopai/api-client-python/compare/v0.54.0...v0.55.0)

### Features

* **api:** api update ([b861c73](https://github.com/runloopai/api-client-python/commit/b861c73595eb0d0744a7a3d81bb46cc2cc397486))
* **api:** api update ([06ec7b9](https://github.com/runloopai/api-client-python/commit/06ec7b9b9b47b96c1876427f74a063640a4f6fb7))


### Chores

* **internal:** fix ruff target version ([91fb064](https://github.com/runloopai/api-client-python/commit/91fb0649d64f4982c292330ade9f61b26ff4841c))
* **internal:** update comment in script ([4b8d5ba](https://github.com/runloopai/api-client-python/commit/4b8d5ba0dd2553ca32f56876bd6a20ec04991778))
* update @stainless-api/prism-cli to v5.15.0 ([3119d91](https://github.com/runloopai/api-client-python/commit/3119d91af94985c86961db8b137753f70ef13748))

## 0.54.0 (2025-08-05)

Full Changelog: [v0.53.0...v0.54.0](https://github.com/runloopai/api-client-python/compare/v0.53.0...v0.54.0)

### Features

* **api:** api update ([9d40ca4](https://github.com/runloopai/api-client-python/commit/9d40ca48745596ae2fa29ea3ad7fba93961eb801))
* **client:** support file upload requests ([5742a4b](https://github.com/runloopai/api-client-python/commit/5742a4ba701938607996b278531234121f81776d))

## 0.53.0 (2025-07-30)

Full Changelog: [v0.52.0...v0.53.0](https://github.com/runloopai/api-client-python/compare/v0.52.0...v0.53.0)

### Features

* **api:** api update ([1854faf](https://github.com/runloopai/api-client-python/commit/1854faf3e7a0a63b136d7fceaf03352afe9181a7))

## 0.52.0 (2025-07-30)

Full Changelog: [v0.51.0...v0.52.0](https://github.com/runloopai/api-client-python/compare/v0.51.0...v0.52.0)

### Features

* **api:** api update ([49a39e1](https://github.com/runloopai/api-client-python/commit/49a39e15cdb131567da55c689033b94affba85f2))

## 0.51.0 (2025-07-29)

Full Changelog: [v0.50.0...v0.51.0](https://github.com/runloopai/api-client-python/compare/v0.50.0...v0.51.0)

### Features

* **api:** api update ([5d42629](https://github.com/runloopai/api-client-python/commit/5d426295ac258ede767c131a209b1deab4d746a6))


### Bug Fixes

* **parsing:** ignore empty metadata ([10c81bd](https://github.com/runloopai/api-client-python/commit/10c81bd7e10ee82e1414aede07c6889630322f6b))
* **parsing:** parse extra field types ([9d2a5f0](https://github.com/runloopai/api-client-python/commit/9d2a5f01e3646d127dec75dca085c2168c35f48a))


### Chores

* **project:** add settings file for vscode ([7a11210](https://github.com/runloopai/api-client-python/commit/7a1121066a7eeb7ca3acb9185834154556d52894))
* **types:** rebuild Pydantic models after all types are defined ([b1839c6](https://github.com/runloopai/api-client-python/commit/b1839c61f42496896ed58b90a983771902f2c26e))

## 0.50.0 (2025-07-15)

Full Changelog: [v0.49.0...v0.50.0](https://github.com/runloopai/api-client-python/compare/v0.49.0...v0.50.0)

### Features

* **api:** api update ([3ebaf54](https://github.com/runloopai/api-client-python/commit/3ebaf5400d977cf4eed3c254235aecb44e5b6836))

## 0.49.0 (2025-07-15)

Full Changelog: [v0.48.2...v0.49.0](https://github.com/runloopai/api-client-python/compare/v0.48.2...v0.49.0)

### Features

* **api:** api update ([6022768](https://github.com/runloopai/api-client-python/commit/60227681f91e9eabc2b8da030fc6ef61834ce761))
* **api:** api update ([27c4579](https://github.com/runloopai/api-client-python/commit/27c4579ac003a2e211c5b421a1cc4714f86c6e57))
* clean up environment call outs ([e3a125d](https://github.com/runloopai/api-client-python/commit/e3a125d0bde927ff142d1817ce4c40489a3217c0))


### Bug Fixes

* **client:** don't send Content-Type header on GET requests ([5d9b833](https://github.com/runloopai/api-client-python/commit/5d9b8330d37d53bb5c1e8393c5d9798323a0a2ca))

## 0.48.2 (2025-07-11)

Full Changelog: [v0.48.1...v0.48.2](https://github.com/runloopai/api-client-python/compare/v0.48.1...v0.48.2)

### Chores

* **readme:** fix version rendering on pypi ([73af53e](https://github.com/runloopai/api-client-python/commit/73af53e19889262ac445fc0789999873c411c35a))

## 0.48.1 (2025-07-10)

Full Changelog: [v0.48.0...v0.48.1](https://github.com/runloopai/api-client-python/compare/v0.48.0...v0.48.1)

### Bug Fixes

* **parsing:** correctly handle nested discriminated unions ([3312be9](https://github.com/runloopai/api-client-python/commit/3312be9e751dd58396884644be4ceabbaba11014))


### Chores

* **internal:** bump pinned h11 dep ([80ff87c](https://github.com/runloopai/api-client-python/commit/80ff87cde91eedd2169bd3b3e563545291928cbd))
* **package:** mark python 3.13 as supported ([7043864](https://github.com/runloopai/api-client-python/commit/70438649e40206746ea1543fc6c29b3c9fb47bd3))

## 0.48.0 (2025-07-09)

Full Changelog: [v0.47.1...v0.48.0](https://github.com/runloopai/api-client-python/compare/v0.47.1...v0.48.0)

## 0.47.1 (2025-07-08)

Full Changelog: [v0.47.0...v0.47.1](https://github.com/runloopai/api-client-python/compare/v0.47.0...v0.47.1)

### Chores

* **ci:** change upload type ([e8af7c3](https://github.com/runloopai/api-client-python/commit/e8af7c350cf848f0255ffc3ebcaeb339ebcb8ba9))
* **internal:** codegen related update ([402126e](https://github.com/runloopai/api-client-python/commit/402126e45fbb32556f59b1504ded9581910ee7dd))

## 0.47.0 (2025-07-01)

Full Changelog: [v0.46.0...v0.47.0](https://github.com/runloopai/api-client-python/compare/v0.46.0...v0.47.0)

### Features

* **api:** api update ([01b01d4](https://github.com/runloopai/api-client-python/commit/01b01d43edfeb15a3f4b56cab6577a4bdd4f75ed))

## 0.46.0 (2025-07-01)

Full Changelog: [v0.45.0...v0.46.0](https://github.com/runloopai/api-client-python/compare/v0.45.0...v0.46.0)

### Features

* **api:** api update ([f8b3493](https://github.com/runloopai/api-client-python/commit/f8b3493a584b10a91fe1e7d543fe4c0de406cf7d))


### Bug Fixes

* **ci:** correct conditional ([2005e4f](https://github.com/runloopai/api-client-python/commit/2005e4ff9ca9bcb569ef4798bd490e036ad1afd5))
* **ci:** release-doctor — report correct token name ([41a600a](https://github.com/runloopai/api-client-python/commit/41a600aeceb84b5c32a7d771acc6acd1cca97b8e))


### Chores

* **ci:** only run for pushes and fork pull requests ([c914e94](https://github.com/runloopai/api-client-python/commit/c914e94ea65e9d4180810cc3b816f4ab4a2a8e22))

## 0.45.0 (2025-06-24)

Full Changelog: [v0.44.0...v0.45.0](https://github.com/runloopai/api-client-python/compare/v0.44.0...v0.45.0)

### Features

* **api:** api update ([382b901](https://github.com/runloopai/api-client-python/commit/382b9018d26ce11e12d7143a84b80147be63ac2e))
* **api:** api update ([3f896cf](https://github.com/runloopai/api-client-python/commit/3f896cf907ef15fc2f0d01f681844eef0bca9479))
* **api:** api update ([9bb3abf](https://github.com/runloopai/api-client-python/commit/9bb3abf4b274d9e75940cc859eafd0f4f37027b8))


### Chores

* **tests:** skip some failing tests on the latest python versions ([27007c0](https://github.com/runloopai/api-client-python/commit/27007c0a1500e80cc9ac93cb634021a7cfb569e6))

## 0.44.0 (2025-06-21)

Full Changelog: [v0.43.0...v0.44.0](https://github.com/runloopai/api-client-python/compare/v0.43.0...v0.44.0)

### Features

* **api:** api update ([8bd0a39](https://github.com/runloopai/api-client-python/commit/8bd0a3937ff3d5b3e03a34ab2fc291377bbc4203))
* **api:** api update ([8ebd055](https://github.com/runloopai/api-client-python/commit/8ebd055bb3760c7a01193df890ca7e56d7ff9c01))
* **client:** add support for aiohttp ([4237321](https://github.com/runloopai/api-client-python/commit/4237321688934fcc89a17588800ce33fb47d9633))


### Bug Fixes

* **tests:** fix: tests which call HTTP endpoints directly with the example parameters ([038fe71](https://github.com/runloopai/api-client-python/commit/038fe71f5d0bee93bdcad12af69a8f5b09b6664f))


### Chores

* **ci:** enable for pull requests ([f64b8a2](https://github.com/runloopai/api-client-python/commit/f64b8a2a52a28a86f25d8b8ad1998e9ce4dda542))
* **internal:** update conftest.py ([d840c86](https://github.com/runloopai/api-client-python/commit/d840c863eb3b080202874080e44b8ab0baa379c4))
* **readme:** update badges ([4b5af3f](https://github.com/runloopai/api-client-python/commit/4b5af3faf2f3cfbcee8474b864335eb0a4c0a78b))
* **tests:** add tests for httpx client instantiation & proxies ([938b9aa](https://github.com/runloopai/api-client-python/commit/938b9aa33ef7ae52809ca6e9111fc3265d70263d))


### Documentation

* **client:** fix httpx.Timeout documentation reference ([b8df915](https://github.com/runloopai/api-client-python/commit/b8df91557df34f77ce5a6f85769305628d9f2a1d))

## 0.43.0 (2025-06-14)

Full Changelog: [v0.42.0...v0.43.0](https://github.com/runloopai/api-client-python/compare/v0.42.0...v0.43.0)

### Features

* **api:** api update ([695b29a](https://github.com/runloopai/api-client-python/commit/695b29a97bd2dcad3f90ee377ed0475a84ed1a2b))


### Bug Fixes

* **client:** correctly parse binary response | stream ([1d815d4](https://github.com/runloopai/api-client-python/commit/1d815d468db24142174fe536c05dcd3ec49ee03f))


### Chores

* **tests:** run tests in parallel ([fdeee42](https://github.com/runloopai/api-client-python/commit/fdeee42440c5df55af77cbad2423c7faab473dcd))

## 0.42.0 (2025-06-11)

Full Changelog: [v0.41.0...v0.42.0](https://github.com/runloopai/api-client-python/compare/v0.41.0...v0.42.0)

### Features

* **api:** api update ([6cdcab7](https://github.com/runloopai/api-client-python/commit/6cdcab70311f7344b28867e1bc0310370618dac8))

## 0.41.0 (2025-06-10)

Full Changelog: [v0.40.0...v0.41.0](https://github.com/runloopai/api-client-python/compare/v0.40.0...v0.41.0)

### Features

* **api:** api update ([31d12f7](https://github.com/runloopai/api-client-python/commit/31d12f76e35504238eadc7ff85a04557c3851a2a))

## 0.40.0 (2025-06-10)

Full Changelog: [v0.39.0...v0.40.0](https://github.com/runloopai/api-client-python/compare/v0.39.0...v0.40.0)

### Features

* **api:** api update ([8e066c3](https://github.com/runloopai/api-client-python/commit/8e066c3dde50f92a16054323b867f94bc6ba0f8e))
* **api:** api update ([4a9a9e3](https://github.com/runloopai/api-client-python/commit/4a9a9e3c2d5b307df4205f16cc8a6eca38f51721))

## 0.39.0 (2025-06-04)

Full Changelog: [v0.38.0...v0.39.0](https://github.com/runloopai/api-client-python/compare/v0.38.0...v0.39.0)

### Features

* **api:** api update ([fbabb53](https://github.com/runloopai/api-client-python/commit/fbabb538a0dc6662841cb4cb4e489dae3f4f4e4c))
* **api:** api update ([7fa8636](https://github.com/runloopai/api-client-python/commit/7fa8636459ea96553b9d65a4475fce3815c1b2e7))

## 0.38.0 (2025-06-04)

Full Changelog: [v0.37.0...v0.38.0](https://github.com/runloopai/api-client-python/compare/v0.37.0...v0.38.0)

### Features

* **api:** api update ([ecb87bd](https://github.com/runloopai/api-client-python/commit/ecb87bdf471fffd90e742ff3021859eb3e94db8c))

## 0.37.0 (2025-06-04)

Full Changelog: [v0.36.0...v0.37.0](https://github.com/runloopai/api-client-python/compare/v0.36.0...v0.37.0)

### Features

* **api:** api update ([a167d0b](https://github.com/runloopai/api-client-python/commit/a167d0b2dbab59cb4ffbb029ea6dae22d0d7c2f4))
* **client:** add follow_redirects request option ([c29d24c](https://github.com/runloopai/api-client-python/commit/c29d24c5483ee2ca7e4d53dfdf8d40278f04f1fe))


### Chores

* **docs:** remove reference to rye shell ([af51a95](https://github.com/runloopai/api-client-python/commit/af51a958afb08cc728959b154c52d0ca31f4206c))
* **docs:** remove unnecessary param examples ([a29553d](https://github.com/runloopai/api-client-python/commit/a29553d048fa85207e28e5b3dbc4ad9ea326ad86))

## 0.36.0 (2025-06-02)

Full Changelog: [v0.35.0...v0.36.0](https://github.com/runloopai/api-client-python/compare/v0.35.0...v0.36.0)

### Features

* **api:** api update ([43e693c](https://github.com/runloopai/api-client-python/commit/43e693ce72c8000ee98ae50925a05b8163e04c15))

## 0.35.0 (2025-05-30)

Full Changelog: [v0.34.1...v0.35.0](https://github.com/runloopai/api-client-python/compare/v0.34.1...v0.35.0)

### Features

* **api:** api update ([c303a71](https://github.com/runloopai/api-client-python/commit/c303a710e21d6da73de907638905b08027acf64a))

## 0.34.1 (2025-05-28)

Full Changelog: [v0.34.0...v0.34.1](https://github.com/runloopai/api-client-python/compare/v0.34.0...v0.34.1)

### Bug Fixes

* **docs/api:** remove references to nonexistent types ([2462ba5](https://github.com/runloopai/api-client-python/commit/2462ba56d0f0735cf9995eebd18818ea94b3fb10))

## 0.34.0 (2025-05-27)

Full Changelog: [v0.33.0...v0.34.0](https://github.com/runloopai/api-client-python/compare/v0.33.0...v0.34.0)

### Features

* **api:** api update ([997a8ff](https://github.com/runloopai/api-client-python/commit/997a8ffab12ffc3f3a305058456af2bebeae8482))

## 0.33.0 (2025-05-22)

Full Changelog: [v0.32.0...v0.33.0](https://github.com/runloopai/api-client-python/compare/v0.32.0...v0.33.0)

### Features

* **api:** api update ([cb65028](https://github.com/runloopai/api-client-python/commit/cb65028a6402068015249344ae28bccc73f06a44))
* **api:** api update ([d86368b](https://github.com/runloopai/api-client-python/commit/d86368b9d942d4eada396ad864f2f75dfeec3f1a))
* **api:** api update ([a08fe0e](https://github.com/runloopai/api-client-python/commit/a08fe0e64744f7edb832574c8ed66ecb181cdeba))
* **api:** api update ([597df88](https://github.com/runloopai/api-client-python/commit/597df884cf33c10fadb2148393bef626aaf23c53))


### Bug Fixes

* **package:** support direct resource imports ([44f30d6](https://github.com/runloopai/api-client-python/commit/44f30d62901a439f835e7ea9367d2691de8844a8))


### Chores

* **ci:** fix installation instructions ([5fed44a](https://github.com/runloopai/api-client-python/commit/5fed44abc7323ac5360c60a3c2472b24c3a7359a))
* **ci:** upload sdks to package manager ([25dbae1](https://github.com/runloopai/api-client-python/commit/25dbae18d04f12b9a19dac7cea76546b6be0acab))
* **docs:** grammar improvements ([a0c74a5](https://github.com/runloopai/api-client-python/commit/a0c74a50c8209448b1eaaf29416fc30a25c5eecc))
* **internal:** avoid errors for isinstance checks on proxies ([e825829](https://github.com/runloopai/api-client-python/commit/e825829b51d90c2d2b18b0f6d0864ee8fc1b0419))

## 0.32.0 (2025-04-25)

Full Changelog: [v0.31.0...v0.32.0](https://github.com/runloopai/api-client-python/compare/v0.31.0...v0.32.0)

### Features

* **api:** api update ([cf2ad50](https://github.com/runloopai/api-client-python/commit/cf2ad505284d70de40503c417b3a1183294b7174))


### Bug Fixes

* **pydantic v1:** more robust ModelField.annotation check ([6ac21f3](https://github.com/runloopai/api-client-python/commit/6ac21f3a0ceb614011e1359b7c8d68c85a47b840))


### Chores

* broadly detect json family of content-type headers ([0a09a72](https://github.com/runloopai/api-client-python/commit/0a09a72c20fdf74d044bf074a68629da159d16b7))
* **ci:** add timeout thresholds for CI jobs ([a10bca8](https://github.com/runloopai/api-client-python/commit/a10bca8067d5fdbd5095a7bdc81ff744e5bc1314))
* **ci:** only use depot for staging repos ([84dd6ba](https://github.com/runloopai/api-client-python/commit/84dd6ba5bd4279e8dacad56c04b4aebb20023463))
* **internal:** codegen related update ([fdaff81](https://github.com/runloopai/api-client-python/commit/fdaff81cc4ef7a4ee0455c07a7655868705599c0))
* **internal:** fix list file params ([d74de2f](https://github.com/runloopai/api-client-python/commit/d74de2fab676075f4e46972dbba8f413b1e1160e))
* **internal:** import reformatting ([97a122c](https://github.com/runloopai/api-client-python/commit/97a122c50265888b92b41d6f078209c054a1fb79))
* **internal:** minor formatting changes ([6557c6c](https://github.com/runloopai/api-client-python/commit/6557c6ccf7bb6f6e93b6e29c3c8bbe49ef57d44d))
* **internal:** refactor retries to not use recursion ([88cd023](https://github.com/runloopai/api-client-python/commit/88cd02300c4e5eb6bb763341a71aca3eccbeebae))

## 0.31.0 (2025-04-21)

Full Changelog: [v0.30.0...v0.31.0](https://github.com/runloopai/api-client-python/compare/v0.30.0...v0.31.0)

### Features

* **api:** api update ([4c348b6](https://github.com/runloopai/api-client-python/commit/4c348b65cf8e0c59b1cc04122a2a53bc863e053b))


### Chores

* **internal:** base client updates ([71a0a00](https://github.com/runloopai/api-client-python/commit/71a0a00703668b365cce28979bf052d2c1ce78a9))
* **internal:** bump pyright version ([950fe0d](https://github.com/runloopai/api-client-python/commit/950fe0d00ec77063e2a8b7dedba256e2878c41bb))
* **internal:** update models test ([def3490](https://github.com/runloopai/api-client-python/commit/def3490573a3b1b304287b54e30cd26fd86dc1ac))

## 0.30.0 (2025-04-16)

Full Changelog: [v0.29.0...v0.30.0](https://github.com/runloopai/api-client-python/compare/v0.29.0...v0.30.0)

### Features

* **api:** api update ([380287d](https://github.com/runloopai/api-client-python/commit/380287d31238c9cc1cf99a3c394f03141be6174d))
* **api:** api update ([e9857e8](https://github.com/runloopai/api-client-python/commit/e9857e86999295ef3a8507f69c61ea6ee2861908))
* **api:** api update ([#586](https://github.com/runloopai/api-client-python/issues/586)) ([eb6d1ba](https://github.com/runloopai/api-client-python/commit/eb6d1ba0b6420f256c8b40dbae75f8a51854d32d))


### Bug Fixes

* **client:** correctly reuse idempotency key ([a6ba920](https://github.com/runloopai/api-client-python/commit/a6ba9201bf5012822ba97fdfdc48e96668a2d22e))
* **perf:** optimize some hot paths ([edf120c](https://github.com/runloopai/api-client-python/commit/edf120c4cfc3d0104c3735c6882787a039b21bce))
* **perf:** skip traversing types for NotGiven values ([bcb8823](https://github.com/runloopai/api-client-python/commit/bcb8823c114d7171745010f41442932657fc0b76))


### Chores

* fix typos ([#582](https://github.com/runloopai/api-client-python/issues/582)) ([66d248c](https://github.com/runloopai/api-client-python/commit/66d248cf691f776d04df6aeb3273734bbf914a3b))
* **internal:** expand CI branch coverage ([0b68591](https://github.com/runloopai/api-client-python/commit/0b68591b8977c6863d75a464045a958809cca096))
* **internal:** reduce CI branch coverage ([58821a3](https://github.com/runloopai/api-client-python/commit/58821a3fc73f47ed0601a8fdbeaad79778765719))
* **internal:** remove trailing character ([#584](https://github.com/runloopai/api-client-python/issues/584)) ([65bacb7](https://github.com/runloopai/api-client-python/commit/65bacb71b584b8b1a3f998efb2d28102ffa98d74))
* **internal:** slight transform perf improvement ([#587](https://github.com/runloopai/api-client-python/issues/587)) ([ec630c4](https://github.com/runloopai/api-client-python/commit/ec630c44eefc52b89ce69277c9040fc93dd9241f))
* **internal:** update pyright settings ([487213d](https://github.com/runloopai/api-client-python/commit/487213dcc570b7d538fbff04b0a942cdbc6e97c6))
* slight wording improvement in README ([#588](https://github.com/runloopai/api-client-python/issues/588)) ([2eb6437](https://github.com/runloopai/api-client-python/commit/2eb643793ea4ce03000b5b4eae6f39843a74543b))


### Documentation

* swap examples used in readme ([#585](https://github.com/runloopai/api-client-python/issues/585)) ([adf9a26](https://github.com/runloopai/api-client-python/commit/adf9a26a3890b7bd5899d191927ed97a9402c864))

## 0.29.0 (2025-03-25)

Full Changelog: [v0.28.0...v0.29.0](https://github.com/runloopai/api-client-python/compare/v0.28.0...v0.29.0)

### Features

* **api:** api update ([#578](https://github.com/runloopai/api-client-python/issues/578)) ([73a814f](https://github.com/runloopai/api-client-python/commit/73a814fa135eb768ca5d6f7e73c9720d32c5be93))
* **api:** api update ([#580](https://github.com/runloopai/api-client-python/issues/580)) ([c8389b1](https://github.com/runloopai/api-client-python/commit/c8389b1d1c521226ccca8665c79c1b1a5349e457))

## 0.28.0 (2025-03-21)

Full Changelog: [v0.27.0...v0.28.0](https://github.com/runloopai/api-client-python/compare/v0.27.0...v0.28.0)

### Features

* **api:** api update ([#575](https://github.com/runloopai/api-client-python/issues/575)) ([c6f1ca5](https://github.com/runloopai/api-client-python/commit/c6f1ca5d4101b6c1b62326a1bf4d7bd090461595))

## 0.27.0 (2025-03-21)

Full Changelog: [v0.26.0...v0.27.0](https://github.com/runloopai/api-client-python/compare/v0.26.0...v0.27.0)

### Features

* **api:** api update ([#573](https://github.com/runloopai/api-client-python/issues/573)) ([091f833](https://github.com/runloopai/api-client-python/commit/091f833d80096bb0470d505c0a0145648e52819b))


### Bug Fixes

* **ci:** ensure pip is always available ([#571](https://github.com/runloopai/api-client-python/issues/571)) ([ddb9362](https://github.com/runloopai/api-client-python/commit/ddb93629704f116cafb2123dc8b302ddff883bb8))
* **ci:** remove publishing patch ([#572](https://github.com/runloopai/api-client-python/issues/572)) ([c71815a](https://github.com/runloopai/api-client-python/commit/c71815aaaf47e404e1bf3d44c6b26b5ed0b05054))
* **types:** handle more discriminated union shapes ([#570](https://github.com/runloopai/api-client-python/issues/570)) ([297cfbe](https://github.com/runloopai/api-client-python/commit/297cfbe93bfdcbbafd44a4501d5a81a7fb1651bd))


### Chores

* **internal:** bump rye to 0.44.0 ([#569](https://github.com/runloopai/api-client-python/issues/569)) ([dd5b79a](https://github.com/runloopai/api-client-python/commit/dd5b79a221fff5b38fdbd655d78254fe7140fd73))
* **internal:** remove extra empty newlines ([#567](https://github.com/runloopai/api-client-python/issues/567)) ([49f34bd](https://github.com/runloopai/api-client-python/commit/49f34bd0b733f2a10592fff098d379501df3ac86))


### Documentation

* revise readme docs about nested params ([#564](https://github.com/runloopai/api-client-python/issues/564)) ([a2df5d3](https://github.com/runloopai/api-client-python/commit/a2df5d3c9b32ab941ee83d3f5cac8b874b7bbe28))

## 0.26.0 (2025-03-04)

Full Changelog: [v0.25.0...v0.26.0](https://github.com/runloopai/api-client-python/compare/v0.25.0...v0.26.0)

### Features

* cp ([4675ff3](https://github.com/runloopai/api-client-python/commit/4675ff37c7bfbce34db1a2b1a2b95bfc90407c57))
* cp ([a0e7c26](https://github.com/runloopai/api-client-python/commit/a0e7c26d92b1f846e8e27ad80b4bcc3eec9a6b4c))
* cp ([2ed5f7a](https://github.com/runloopai/api-client-python/commit/2ed5f7a944582d29a5284ddc7ff455832dede033))


### Chores

* **docs:** update client docstring ([#559](https://github.com/runloopai/api-client-python/issues/559)) ([aae64ef](https://github.com/runloopai/api-client-python/commit/aae64ef8fa7a03db23695b7dae48dba6d7b1d1e3))
* **internal:** remove unused http client options forwarding ([#561](https://github.com/runloopai/api-client-python/issues/561)) ([39fcd59](https://github.com/runloopai/api-client-python/commit/39fcd59664517ad7a088a087011cb38f1d9a58ae))


### Documentation

* update URLs from stainlessapi.com to stainless.com ([#558](https://github.com/runloopai/api-client-python/issues/558)) ([cc0b37d](https://github.com/runloopai/api-client-python/commit/cc0b37d74d46c7796ae72a8d496ee733e50b70c0))

## 0.25.0 (2025-02-26)

Full Changelog: [v0.24.0...v0.25.0](https://github.com/runloopai/api-client-python/compare/v0.24.0...v0.25.0)

### Features

* **api:** api update ([#555](https://github.com/runloopai/api-client-python/issues/555)) ([7c1d55d](https://github.com/runloopai/api-client-python/commit/7c1d55de7fe3f157a30080ddc7e7f0ea5053304a))
* **client:** allow passing `NotGiven` for body ([#553](https://github.com/runloopai/api-client-python/issues/553)) ([dc21cae](https://github.com/runloopai/api-client-python/commit/dc21caec97e15ccde2c396c6a2f0fce0f2bad313))


### Bug Fixes

* **client:** mark some request bodies as optional ([dc21cae](https://github.com/runloopai/api-client-python/commit/dc21caec97e15ccde2c396c6a2f0fce0f2bad313))


### Chores

* **internal:** codegen related update ([#551](https://github.com/runloopai/api-client-python/issues/551)) ([8dd01a1](https://github.com/runloopai/api-client-python/commit/8dd01a1e69d82ccbc4f05b72bd980d16cb93e5e5))
* **internal:** fix devcontainers setup ([#554](https://github.com/runloopai/api-client-python/issues/554)) ([9260eb4](https://github.com/runloopai/api-client-python/commit/9260eb4443fc50ecb07e99af2307896e32027158))
* **internal:** properly set __pydantic_private__ ([#556](https://github.com/runloopai/api-client-python/issues/556)) ([4496830](https://github.com/runloopai/api-client-python/commit/449683002d1fb31b01c4d167973058684b7ee654))

## 0.24.0 (2025-02-19)

Full Changelog: [v0.23.0...v0.24.0](https://github.com/runloopai/api-client-python/compare/v0.23.0...v0.24.0)

### Features

* **api:** api update ([#549](https://github.com/runloopai/api-client-python/issues/549)) ([3e19f41](https://github.com/runloopai/api-client-python/commit/3e19f41cf8e2b9cd225439d9df90f80b34d89660))


### Bug Fixes

* asyncify on non-asyncio runtimes ([#547](https://github.com/runloopai/api-client-python/issues/547)) ([8ce7003](https://github.com/runloopai/api-client-python/commit/8ce700397fc5d6755f0a95b637efad74d6dc3fe4))


### Chores

* **internal:** codegen related update ([#543](https://github.com/runloopai/api-client-python/issues/543)) ([5c44e84](https://github.com/runloopai/api-client-python/commit/5c44e84a8a029b22461df339c280885dc972fa96))
* **internal:** codegen related update ([#546](https://github.com/runloopai/api-client-python/issues/546)) ([d8b620d](https://github.com/runloopai/api-client-python/commit/d8b620d93c687d37a843262d5ac60fd4a9b815e8))
* **internal:** update client tests ([#545](https://github.com/runloopai/api-client-python/issues/545)) ([30307f4](https://github.com/runloopai/api-client-python/commit/30307f4b78ba76240793b851dd735a0beb835b75))
* **internal:** update client tests ([#548](https://github.com/runloopai/api-client-python/issues/548)) ([4e782f1](https://github.com/runloopai/api-client-python/commit/4e782f19bfa7e08ae318eca6f00fb4d5ffe5c9af))

## 0.23.0 (2025-02-11)

Full Changelog: [v0.22.0...v0.23.0](https://github.com/runloopai/api-client-python/compare/v0.22.0...v0.23.0)

### Features

* **api:** api update ([#540](https://github.com/runloopai/api-client-python/issues/540)) ([0f1ce28](https://github.com/runloopai/api-client-python/commit/0f1ce28e9137b52265666131ee0c7561e92cefd9))
* **client:** send `X-Stainless-Read-Timeout` header ([#536](https://github.com/runloopai/api-client-python/issues/536)) ([996da95](https://github.com/runloopai/api-client-python/commit/996da9596984be3962a3f1f81753c0617676988b))


### Bug Fixes

* **api:** remove recursive model for now ([#534](https://github.com/runloopai/api-client-python/issues/534)) ([748bd3d](https://github.com/runloopai/api-client-python/commit/748bd3d1c63587094c0c7ead108d670740052a0b))


### Chores

* **internal:** codegen related update ([#538](https://github.com/runloopai/api-client-python/issues/538)) ([b538d7c](https://github.com/runloopai/api-client-python/commit/b538d7c842fa8f2ebf5bcb61b9184d9171283c36))
* **internal:** fix type traversing dictionary params ([#537](https://github.com/runloopai/api-client-python/issues/537)) ([d6afc80](https://github.com/runloopai/api-client-python/commit/d6afc8051e30d19b2f011f3bcad85676d96c4a48))
* **internal:** minor type handling changes ([#539](https://github.com/runloopai/api-client-python/issues/539)) ([ecd4acd](https://github.com/runloopai/api-client-python/commit/ecd4acd4ac7e950ad5757a4f6adc08971135f7d3))

## 0.22.0 (2025-02-04)

Full Changelog: [v0.21.0...v0.22.0](https://github.com/runloopai/api-client-python/compare/v0.21.0...v0.22.0)

### Features

* **api:** api update ([#531](https://github.com/runloopai/api-client-python/issues/531)) ([2952d8d](https://github.com/runloopai/api-client-python/commit/2952d8d3b2653fd02f1bf99ac3cb6e76739a282a))

## 0.21.0 (2025-02-04)

Full Changelog: [v0.20.0...v0.21.0](https://github.com/runloopai/api-client-python/compare/v0.20.0...v0.21.0)

### Features

* **api:** api update ([#528](https://github.com/runloopai/api-client-python/issues/528)) ([d731dad](https://github.com/runloopai/api-client-python/commit/d731dadc4b7095967be1184bf2f490f4405e8237))

## 0.20.0 (2025-02-04)

Full Changelog: [v0.19.0...v0.20.0](https://github.com/runloopai/api-client-python/compare/v0.19.0...v0.20.0)

### Features

* add helpers for blueprint and scenario run creation ([b00a7c1](https://github.com/runloopai/api-client-python/commit/b00a7c1b935db7c919d79ed10c135bf5ed2a9b4f))
* **api:** api update ([#526](https://github.com/runloopai/api-client-python/issues/526)) ([be26ed7](https://github.com/runloopai/api-client-python/commit/be26ed7c82017d9bff67c9920c078808f8a675e3))


### Chores

* **internal:** bummp ruff dependency ([#525](https://github.com/runloopai/api-client-python/issues/525)) ([84051db](https://github.com/runloopai/api-client-python/commit/84051db83a6347f28ee4891be52f5eee7fa9d02a))
* **internal:** change default timeout to an int ([#524](https://github.com/runloopai/api-client-python/issues/524)) ([a15ccaa](https://github.com/runloopai/api-client-python/commit/a15ccaa45f69331d57be0144a16ba3b1df387245))

## 0.19.0 (2025-02-03)

Full Changelog: [v0.18.0...v0.19.0](https://github.com/runloopai/api-client-python/compare/v0.18.0...v0.19.0)

### Features

* add helper methods for scenarios ([551fcfc](https://github.com/runloopai/api-client-python/commit/551fcfc1dc5b8b67c0c6179d49c3eef2c0a38676))
* **api:** api update ([#520](https://github.com/runloopai/api-client-python/issues/520)) ([750b4ba](https://github.com/runloopai/api-client-python/commit/750b4ba51cc0c848258113af8bf882ceb679bf9e))

## 0.18.0 (2025-02-01)

Full Changelog: [v0.17.0...v0.18.0](https://github.com/runloopai/api-client-python/compare/v0.17.0...v0.18.0)

### Features

* **api:** api update ([#515](https://github.com/runloopai/api-client-python/issues/515)) ([1c68520](https://github.com/runloopai/api-client-python/commit/1c68520b90822af7d035acbf8b366a0c6492ec87))

## 0.17.0 (2025-01-31)

Full Changelog: [v0.16.0...v0.17.0](https://github.com/runloopai/api-client-python/compare/v0.16.0...v0.17.0)

### Features

* **api:** api update ([#512](https://github.com/runloopai/api-client-python/issues/512)) ([7664372](https://github.com/runloopai/api-client-python/commit/7664372659f1b7c63ee4e93ca4e2873402030733))

## 0.16.0 (2025-01-31)

Full Changelog: [v0.15.0...v0.16.0](https://github.com/runloopai/api-client-python/compare/v0.15.0...v0.16.0)

### Features

* **api:** api update ([#510](https://github.com/runloopai/api-client-python/issues/510)) ([914ee46](https://github.com/runloopai/api-client-python/commit/914ee460ccdc6bbd58a7a263d5566716b4bbf9df))


### Chores

* **internal:** codegen related update ([#508](https://github.com/runloopai/api-client-python/issues/508)) ([278e736](https://github.com/runloopai/api-client-python/commit/278e736787b66e0d0a5fbc64743a386cfefd1994))

## 0.15.0 (2025-01-29)

Full Changelog: [v0.14.0...v0.15.0](https://github.com/runloopai/api-client-python/compare/v0.14.0...v0.15.0)

### Features

* **api:** api update ([#504](https://github.com/runloopai/api-client-python/issues/504)) ([d73a1ef](https://github.com/runloopai/api-client-python/commit/d73a1efcec6e24fc92a0504746d0da186fd3d20a))
* **api:** api update ([#506](https://github.com/runloopai/api-client-python/issues/506)) ([a122cdc](https://github.com/runloopai/api-client-python/commit/a122cdc3b592860ce08cbd02b434ecf343bb3081))

## 0.14.0 (2025-01-29)

Full Changelog: [v0.13.0...v0.14.0](https://github.com/runloopai/api-client-python/compare/v0.13.0...v0.14.0)

### Features

* **api:** api update ([#501](https://github.com/runloopai/api-client-python/issues/501)) ([cb1f8ac](https://github.com/runloopai/api-client-python/commit/cb1f8ac9e6ea44e33db8a4739cbb325a982840f4))
* **api:** api update ([#502](https://github.com/runloopai/api-client-python/issues/502)) ([22d84a8](https://github.com/runloopai/api-client-python/commit/22d84a8727e147d26d4bfd82ca26a1ac8d32365f))


### Bug Fixes

* **tests:** make test_get_platform less flaky ([#500](https://github.com/runloopai/api-client-python/issues/500)) ([394d017](https://github.com/runloopai/api-client-python/commit/394d0172530ea1284173d3fd04a3a8a1f1dd78f9))


### Chores

* **internal:** codegen related update ([#497](https://github.com/runloopai/api-client-python/issues/497)) ([207a88e](https://github.com/runloopai/api-client-python/commit/207a88ed4bed2b87e10d15c49002661f1cf84f1c))


### Documentation

* **raw responses:** fix duplicate `the` ([#499](https://github.com/runloopai/api-client-python/issues/499)) ([80e393c](https://github.com/runloopai/api-client-python/commit/80e393c1c87319b6886cef1c2806c2ce8e467a54))

## 0.13.0 (2025-01-15)

Full Changelog: [v0.12.0...v0.13.0](https://github.com/runloopai/api-client-python/compare/v0.12.0...v0.13.0)

### Features

* add helpers for common polling operations ([97891c7](https://github.com/runloopai/api-client-python/commit/97891c7cf8be7b9192c5dbcfc35fc93cb3490d04))
* **api:** api update ([#481](https://github.com/runloopai/api-client-python/issues/481)) ([7a8d8a8](https://github.com/runloopai/api-client-python/commit/7a8d8a8ba1119fd43ee4d40127fc486f0c626cb8))
* **api:** manual updates ([#490](https://github.com/runloopai/api-client-python/issues/490)) ([bcc441e](https://github.com/runloopai/api-client-python/commit/bcc441ed2706379994b7ef27b6104d2cb47a9095))
* **api:** manual updates ([#492](https://github.com/runloopai/api-client-python/issues/492)) ([96e2419](https://github.com/runloopai/api-client-python/commit/96e2419332dbd2c65367730d0d4186c31e76ed32))


### Bug Fixes

* **client:** only call .close() when needed ([#484](https://github.com/runloopai/api-client-python/issues/484)) ([55bf004](https://github.com/runloopai/api-client-python/commit/55bf004101e86ebdb01db4b9ad8661d619a777bb))
* correctly handle deserialising `cls` fields ([#489](https://github.com/runloopai/api-client-python/issues/489)) ([2b2a573](https://github.com/runloopai/api-client-python/commit/2b2a5736c16a985e4b8e33313b4dcde8fc10dbca))


### Chores

* **internal:** bump httpx dependency ([#483](https://github.com/runloopai/api-client-python/issues/483)) ([dcd5be5](https://github.com/runloopai/api-client-python/commit/dcd5be5065ed52f1172d2fa813d6a5ff64767de6))
* **internal:** codegen related update ([#488](https://github.com/runloopai/api-client-python/issues/488)) ([af72728](https://github.com/runloopai/api-client-python/commit/af727286ef5018e27be7d564078d1c0305f7d9e1))


### Documentation

* fix typos ([#487](https://github.com/runloopai/api-client-python/issues/487)) ([440e80b](https://github.com/runloopai/api-client-python/commit/440e80b9e28a64edec079bf72d27c3b188997574))

## 0.12.0 (2025-01-07)

Full Changelog: [v0.11.0...v0.12.0](https://github.com/runloopai/api-client-python/compare/v0.11.0...v0.12.0)

### Features

* **api:** api update ([#362](https://github.com/runloopai/api-client-python/issues/362)) ([3dfc4eb](https://github.com/runloopai/api-client-python/commit/3dfc4eb21b5f4096b33b42e6017a4f536767fe39))
* **api:** api update ([#364](https://github.com/runloopai/api-client-python/issues/364)) ([206a693](https://github.com/runloopai/api-client-python/commit/206a6934f207d0d5006156da6c18a5e2987bece5))
* **api:** api update ([#365](https://github.com/runloopai/api-client-python/issues/365)) ([ffb41c8](https://github.com/runloopai/api-client-python/commit/ffb41c8bd150b2697bba5881f4b65a939dbc5628))
* **api:** api update ([#366](https://github.com/runloopai/api-client-python/issues/366)) ([d3acab8](https://github.com/runloopai/api-client-python/commit/d3acab8f273b3c5a9bbba5f8ed1b2fb6fc95d62e))
* **api:** api update ([#367](https://github.com/runloopai/api-client-python/issues/367)) ([32362b4](https://github.com/runloopai/api-client-python/commit/32362b43f302c837f9becba35d5f582e66111318))
* **api:** api update ([#369](https://github.com/runloopai/api-client-python/issues/369)) ([7f4ac29](https://github.com/runloopai/api-client-python/commit/7f4ac29899d9dd9f22ac440f84b1bbd26e8e4bf4))
* **api:** api update ([#370](https://github.com/runloopai/api-client-python/issues/370)) ([b401ea0](https://github.com/runloopai/api-client-python/commit/b401ea0640d58c4425524bdec3bfb754fd3c7b34))
* **api:** api update ([#371](https://github.com/runloopai/api-client-python/issues/371)) ([7199c10](https://github.com/runloopai/api-client-python/commit/7199c10e22a071d5e80ac429b8ad137afc91ad14))
* **api:** api update ([#372](https://github.com/runloopai/api-client-python/issues/372)) ([3d054e8](https://github.com/runloopai/api-client-python/commit/3d054e81f40836ec07447339be74e26eb499ea5b))
* **api:** api update ([#374](https://github.com/runloopai/api-client-python/issues/374)) ([e1df606](https://github.com/runloopai/api-client-python/commit/e1df606d6726f3c2cd3840f86861c2992f946f57))
* **api:** api update ([#375](https://github.com/runloopai/api-client-python/issues/375)) ([4d377b5](https://github.com/runloopai/api-client-python/commit/4d377b5aabb9d73b01847c04a37e2a13c3228d30))
* **api:** api update ([#376](https://github.com/runloopai/api-client-python/issues/376)) ([ae3516e](https://github.com/runloopai/api-client-python/commit/ae3516e8b99310ba7cc4da431d1cdbbdaa7e8063))
* **api:** api update ([#377](https://github.com/runloopai/api-client-python/issues/377)) ([aba9fd4](https://github.com/runloopai/api-client-python/commit/aba9fd4fde4e4f08396ed8b4d3b523c4d3d4020a))
* **api:** api update ([#378](https://github.com/runloopai/api-client-python/issues/378)) ([b8f2463](https://github.com/runloopai/api-client-python/commit/b8f2463dc08ab85915fe9fc660cd9c11a557649d))
* **api:** api update ([#379](https://github.com/runloopai/api-client-python/issues/379)) ([e9cf060](https://github.com/runloopai/api-client-python/commit/e9cf06068c0dd56af8b1ce2942045c31ba4fe478))
* **api:** api update ([#380](https://github.com/runloopai/api-client-python/issues/380)) ([d20ea3b](https://github.com/runloopai/api-client-python/commit/d20ea3b326fe580a288cac749ec0d4e55177e92c))
* **api:** api update ([#381](https://github.com/runloopai/api-client-python/issues/381)) ([74b87c3](https://github.com/runloopai/api-client-python/commit/74b87c3f41f310d746aacff56e928b1eae6dd9de))
* **api:** api update ([#382](https://github.com/runloopai/api-client-python/issues/382)) ([233e0dd](https://github.com/runloopai/api-client-python/commit/233e0dd203d32cbc3567a177a1c8e443b2d14cfa))
* **api:** api update ([#383](https://github.com/runloopai/api-client-python/issues/383)) ([e235409](https://github.com/runloopai/api-client-python/commit/e2354092bbff99c5314d492bc9213c5dad874c68))
* **api:** api update ([#384](https://github.com/runloopai/api-client-python/issues/384)) ([1b0e2c4](https://github.com/runloopai/api-client-python/commit/1b0e2c4a84f50f07e3c7b034325e7984ee2cc2a9))
* **api:** api update ([#385](https://github.com/runloopai/api-client-python/issues/385)) ([8343ecc](https://github.com/runloopai/api-client-python/commit/8343ecc1094be1a920af87f7887b4d7601552ce9))
* **api:** api update ([#386](https://github.com/runloopai/api-client-python/issues/386)) ([70f46f2](https://github.com/runloopai/api-client-python/commit/70f46f205f8fe8d480107973dacb4590ec1b211e))
* **api:** api update ([#387](https://github.com/runloopai/api-client-python/issues/387)) ([389cf90](https://github.com/runloopai/api-client-python/commit/389cf905ddd1859b72a210ba53274e951c2b1b34))
* **api:** api update ([#388](https://github.com/runloopai/api-client-python/issues/388)) ([bf43a05](https://github.com/runloopai/api-client-python/commit/bf43a05a9c2a3a78fa26454db7188d5e353a1411))
* **api:** api update ([#389](https://github.com/runloopai/api-client-python/issues/389)) ([af17aed](https://github.com/runloopai/api-client-python/commit/af17aed21c4221762ae1111b6df7ee51d49742e2))
* **api:** api update ([#390](https://github.com/runloopai/api-client-python/issues/390)) ([012f542](https://github.com/runloopai/api-client-python/commit/012f542bad6a0c4d1c1f272d4bb0cddeaeecdb48))
* **api:** api update ([#391](https://github.com/runloopai/api-client-python/issues/391)) ([9f52531](https://github.com/runloopai/api-client-python/commit/9f5253195ec5f9c9c782565f64499e64e3f4f016))
* **api:** api update ([#392](https://github.com/runloopai/api-client-python/issues/392)) ([b65b5a4](https://github.com/runloopai/api-client-python/commit/b65b5a4c42f488690f91bed57d427a2fa323b3cd))
* **api:** api update ([#393](https://github.com/runloopai/api-client-python/issues/393)) ([40016f9](https://github.com/runloopai/api-client-python/commit/40016f944bdb366f82d4d02c8ad4e6dd3d35ee6b))
* **api:** api update ([#394](https://github.com/runloopai/api-client-python/issues/394)) ([d8b3c3f](https://github.com/runloopai/api-client-python/commit/d8b3c3f6668ff9a898c6e87b19d78cb1ef978a61))
* **api:** api update ([#395](https://github.com/runloopai/api-client-python/issues/395)) ([4d1c78a](https://github.com/runloopai/api-client-python/commit/4d1c78a27459c170fa613d864bdd0ac902ba1bbc))
* **api:** api update ([#396](https://github.com/runloopai/api-client-python/issues/396)) ([cff50a1](https://github.com/runloopai/api-client-python/commit/cff50a16266e8cc27d69670f0494ba3c914e12bd))
* **api:** api update ([#397](https://github.com/runloopai/api-client-python/issues/397)) ([7b1cbec](https://github.com/runloopai/api-client-python/commit/7b1cbecd0d3806ca2f204181e40e30eb21748b00))
* **api:** api update ([#398](https://github.com/runloopai/api-client-python/issues/398)) ([48cda68](https://github.com/runloopai/api-client-python/commit/48cda680cf76d77861697f361cfcbc835270c608))
* **api:** api update ([#399](https://github.com/runloopai/api-client-python/issues/399)) ([c9473fb](https://github.com/runloopai/api-client-python/commit/c9473fba9e6bafd8cabea5f1cbf3ca4a038ce90c))
* **api:** api update ([#400](https://github.com/runloopai/api-client-python/issues/400)) ([e17628d](https://github.com/runloopai/api-client-python/commit/e17628dbdf515ec49ae87e82bf0d37218cb27233))
* **api:** api update ([#401](https://github.com/runloopai/api-client-python/issues/401)) ([80a1564](https://github.com/runloopai/api-client-python/commit/80a1564e73f434233f8e0a3fa01c826a9009ba0f))
* **api:** api update ([#402](https://github.com/runloopai/api-client-python/issues/402)) ([fffe4ca](https://github.com/runloopai/api-client-python/commit/fffe4ca8e799aad4a38bd18a4ebf96c0276dfa6c))
* **api:** api update ([#403](https://github.com/runloopai/api-client-python/issues/403)) ([e055c7e](https://github.com/runloopai/api-client-python/commit/e055c7e2940b599060c1a425f0ccec2ded38da38))
* **api:** api update ([#404](https://github.com/runloopai/api-client-python/issues/404)) ([1afe6bb](https://github.com/runloopai/api-client-python/commit/1afe6bb15cfadc417e4d10155ad77ac14b03aa48))
* **api:** api update ([#405](https://github.com/runloopai/api-client-python/issues/405)) ([6621921](https://github.com/runloopai/api-client-python/commit/66219217f21dc75bc55842c65b887cab45e3b5ad))
* **api:** api update ([#406](https://github.com/runloopai/api-client-python/issues/406)) ([633bf17](https://github.com/runloopai/api-client-python/commit/633bf17df71d3d28a0c291414b85e9a201483d94))
* **api:** api update ([#407](https://github.com/runloopai/api-client-python/issues/407)) ([964cb03](https://github.com/runloopai/api-client-python/commit/964cb03acb9ed236cc2daea4ddc01d575ecc4a2e))
* **api:** api update ([#408](https://github.com/runloopai/api-client-python/issues/408)) ([f414a30](https://github.com/runloopai/api-client-python/commit/f414a301829cfcf6cb0e09947531882f8b43794e))
* **api:** api update ([#409](https://github.com/runloopai/api-client-python/issues/409)) ([8eb1ea3](https://github.com/runloopai/api-client-python/commit/8eb1ea3ba5d4f09376b4ae0de5d939692796f34e))
* **api:** api update ([#410](https://github.com/runloopai/api-client-python/issues/410)) ([cf5cb65](https://github.com/runloopai/api-client-python/commit/cf5cb651fb5e6ac897099d83a91436582e617e18))
* **api:** api update ([#411](https://github.com/runloopai/api-client-python/issues/411)) ([c4958ef](https://github.com/runloopai/api-client-python/commit/c4958ef61cd2e8ff009574a664357268ebb27d91))
* **api:** api update ([#412](https://github.com/runloopai/api-client-python/issues/412)) ([f0bdc85](https://github.com/runloopai/api-client-python/commit/f0bdc85aea591110a9e081e28fe33f1910c9d9ca))
* **api:** api update ([#413](https://github.com/runloopai/api-client-python/issues/413)) ([d621c18](https://github.com/runloopai/api-client-python/commit/d621c18330cc7ddbbdfbb29570a182a3e038a50e))
* **api:** api update ([#414](https://github.com/runloopai/api-client-python/issues/414)) ([33f66ee](https://github.com/runloopai/api-client-python/commit/33f66eea0d34928bd7245d97b2b7cee539bc7762))
* **api:** api update ([#415](https://github.com/runloopai/api-client-python/issues/415)) ([dc4dee7](https://github.com/runloopai/api-client-python/commit/dc4dee7d331821048fd29105ca6acc2b79a8cadf))
* **api:** api update ([#416](https://github.com/runloopai/api-client-python/issues/416)) ([18ade84](https://github.com/runloopai/api-client-python/commit/18ade84c7eddc115f561b938539db9154de3c962))
* **api:** api update ([#417](https://github.com/runloopai/api-client-python/issues/417)) ([02a1fe8](https://github.com/runloopai/api-client-python/commit/02a1fe8c81a05ff7001ec524fe4207bf14ba31af))
* **api:** api update ([#418](https://github.com/runloopai/api-client-python/issues/418)) ([ba31602](https://github.com/runloopai/api-client-python/commit/ba31602d7be4ce823fa5d15d834c7a8adea58bcc))
* **api:** api update ([#419](https://github.com/runloopai/api-client-python/issues/419)) ([ed84a54](https://github.com/runloopai/api-client-python/commit/ed84a544005c0283199b8cff95f26534fbbbe200))
* **api:** api update ([#420](https://github.com/runloopai/api-client-python/issues/420)) ([a189508](https://github.com/runloopai/api-client-python/commit/a189508858735228872fad813c60a8999a20b008))
* **api:** api update ([#421](https://github.com/runloopai/api-client-python/issues/421)) ([ee6083b](https://github.com/runloopai/api-client-python/commit/ee6083bb8faca2542ba8c739a12dbac4c1e2cae3))
* **api:** api update ([#422](https://github.com/runloopai/api-client-python/issues/422)) ([7415fb9](https://github.com/runloopai/api-client-python/commit/7415fb9c452505d21df8aa23cd26c9073c6b5088))
* **api:** api update ([#423](https://github.com/runloopai/api-client-python/issues/423)) ([cdb793d](https://github.com/runloopai/api-client-python/commit/cdb793d025ce636693933f0e6df405f2b8f6ffd4))
* **api:** api update ([#424](https://github.com/runloopai/api-client-python/issues/424)) ([5b5c0c1](https://github.com/runloopai/api-client-python/commit/5b5c0c1eac9f9511b46794af11619cfd5efecac7))
* **api:** api update ([#425](https://github.com/runloopai/api-client-python/issues/425)) ([673d5ba](https://github.com/runloopai/api-client-python/commit/673d5baba9981f28582dab9619b752c8619feae9))
* **api:** api update ([#426](https://github.com/runloopai/api-client-python/issues/426)) ([0b11b80](https://github.com/runloopai/api-client-python/commit/0b11b80e261da59a644579ec38c15be7ec68d0df))
* **api:** api update ([#427](https://github.com/runloopai/api-client-python/issues/427)) ([875a3bb](https://github.com/runloopai/api-client-python/commit/875a3bb143bdee17bc534935c57fd6566164b33b))
* **api:** api update ([#428](https://github.com/runloopai/api-client-python/issues/428)) ([fc11810](https://github.com/runloopai/api-client-python/commit/fc11810c6c5c908813857532a92e50419e9d0494))
* **api:** api update ([#431](https://github.com/runloopai/api-client-python/issues/431)) ([c4990b0](https://github.com/runloopai/api-client-python/commit/c4990b039821244b15e58a9e0ad61ebc1d4fb4bb))
* **api:** api update ([#432](https://github.com/runloopai/api-client-python/issues/432)) ([d0684d0](https://github.com/runloopai/api-client-python/commit/d0684d07d452f4e9dd7b1eb8614f15d70f386da2))
* **api:** api update ([#433](https://github.com/runloopai/api-client-python/issues/433)) ([bbe8d92](https://github.com/runloopai/api-client-python/commit/bbe8d9289c202f89844cc4a5d219f14ad41232de))
* **api:** api update ([#434](https://github.com/runloopai/api-client-python/issues/434)) ([f81e740](https://github.com/runloopai/api-client-python/commit/f81e740464585f4a4331adba38a834486e63f8ba))
* **api:** api update ([#435](https://github.com/runloopai/api-client-python/issues/435)) ([531fcc0](https://github.com/runloopai/api-client-python/commit/531fcc0008697eba0ca9dec0437753a7e0d6802b))
* **api:** api update ([#436](https://github.com/runloopai/api-client-python/issues/436)) ([f4e0343](https://github.com/runloopai/api-client-python/commit/f4e0343c3229501b22d1ab8373d0045e71a02287))
* **api:** api update ([#437](https://github.com/runloopai/api-client-python/issues/437)) ([e7e5cde](https://github.com/runloopai/api-client-python/commit/e7e5cde5f5e27ed153e10a30dfb512d36a6ffde1))
* **api:** api update ([#438](https://github.com/runloopai/api-client-python/issues/438)) ([8f3b91f](https://github.com/runloopai/api-client-python/commit/8f3b91f39fefb8e98e1f1bc60e2b3fe7d0cdbeaa))
* **api:** api update ([#440](https://github.com/runloopai/api-client-python/issues/440)) ([5a89907](https://github.com/runloopai/api-client-python/commit/5a89907c8812c221193bab0493eba36c0d0ca04f))
* **api:** api update ([#441](https://github.com/runloopai/api-client-python/issues/441)) ([b59c6e8](https://github.com/runloopai/api-client-python/commit/b59c6e8693d5411b9afdb4a8d2bbf881c7edab4a))
* **api:** api update ([#442](https://github.com/runloopai/api-client-python/issues/442)) ([4b12c1a](https://github.com/runloopai/api-client-python/commit/4b12c1a233c729ca55dcf10bb290fc3d0dd48916))
* **api:** api update ([#443](https://github.com/runloopai/api-client-python/issues/443)) ([0847342](https://github.com/runloopai/api-client-python/commit/08473429deb4f10c6b405c931f86dc603154f08f))
* **api:** api update ([#444](https://github.com/runloopai/api-client-python/issues/444)) ([a268c66](https://github.com/runloopai/api-client-python/commit/a268c66d3a01017b273e3f9ac1ff9462aa368143))
* **api:** api update ([#445](https://github.com/runloopai/api-client-python/issues/445)) ([c81a340](https://github.com/runloopai/api-client-python/commit/c81a340c849869bb84b014b8fcde50bf5151a18c))
* **api:** api update ([#446](https://github.com/runloopai/api-client-python/issues/446)) ([890dd15](https://github.com/runloopai/api-client-python/commit/890dd154d289a7b108078cf98675e29d897a78b7))
* **api:** api update ([#447](https://github.com/runloopai/api-client-python/issues/447)) ([5c15205](https://github.com/runloopai/api-client-python/commit/5c152052cbd78738224e49e572f07a7e985e8d72))
* **api:** api update ([#448](https://github.com/runloopai/api-client-python/issues/448)) ([0a4281c](https://github.com/runloopai/api-client-python/commit/0a4281ca32cc84aff988c7ac74550801d2659dff))
* **api:** api update ([#450](https://github.com/runloopai/api-client-python/issues/450)) ([f146e9e](https://github.com/runloopai/api-client-python/commit/f146e9e6579b87cd123ab5b40688276caac09b40))
* **api:** api update ([#451](https://github.com/runloopai/api-client-python/issues/451)) ([3aa8890](https://github.com/runloopai/api-client-python/commit/3aa88905b80e5436c2f679c9fcb7bceaaeb63a1c))
* **api:** api update ([#452](https://github.com/runloopai/api-client-python/issues/452)) ([f34e6a0](https://github.com/runloopai/api-client-python/commit/f34e6a04169ca59f11d8f460ac4fc5b8fc1670c6))
* **api:** api update ([#456](https://github.com/runloopai/api-client-python/issues/456)) ([1c4457e](https://github.com/runloopai/api-client-python/commit/1c4457e187d1da307c4c64b2f64163ca39701c6b))
* **api:** api update ([#457](https://github.com/runloopai/api-client-python/issues/457)) ([3944caf](https://github.com/runloopai/api-client-python/commit/3944cafae35ed8dfd25cdf81cfb11bb63030ab10))
* **api:** api update ([#458](https://github.com/runloopai/api-client-python/issues/458)) ([2051057](https://github.com/runloopai/api-client-python/commit/205105792548c8474155710cef59c767d85dc5ff))
* **api:** api update ([#459](https://github.com/runloopai/api-client-python/issues/459)) ([f994f2b](https://github.com/runloopai/api-client-python/commit/f994f2b220959c64f2e2e0b3a7a5376626cd9f46))
* **api:** api update ([#461](https://github.com/runloopai/api-client-python/issues/461)) ([9916c69](https://github.com/runloopai/api-client-python/commit/9916c699871deb17032a42c2206b6b7eaef2422a))
* **api:** api update ([#462](https://github.com/runloopai/api-client-python/issues/462)) ([12db42c](https://github.com/runloopai/api-client-python/commit/12db42c33402d6dbb3ed6f58275e81f9fec7df6d))
* **api:** api update ([#463](https://github.com/runloopai/api-client-python/issues/463)) ([2b96a69](https://github.com/runloopai/api-client-python/commit/2b96a691a4316974fb0189fea7bcb4a5e83b7100))
* **api:** api update ([#464](https://github.com/runloopai/api-client-python/issues/464)) ([8befd9c](https://github.com/runloopai/api-client-python/commit/8befd9ca3ded2c1612ce6c0afe45ea5ca19abf60))
* **api:** api update ([#465](https://github.com/runloopai/api-client-python/issues/465)) ([13a2b7c](https://github.com/runloopai/api-client-python/commit/13a2b7c97f790b84f2d0c17d661deaea1d2c385d))
* **api:** api update ([#466](https://github.com/runloopai/api-client-python/issues/466)) ([32022e6](https://github.com/runloopai/api-client-python/commit/32022e691ffaf8ff4f329ba11ca442e034702deb))
* **api:** api update ([#467](https://github.com/runloopai/api-client-python/issues/467)) ([b54bcda](https://github.com/runloopai/api-client-python/commit/b54bcda08049b79fb6119883de75bd7b7577b178))
* **api:** api update ([#468](https://github.com/runloopai/api-client-python/issues/468)) ([c63ccbb](https://github.com/runloopai/api-client-python/commit/c63ccbb10bec2469147480608a1f8b85884c0a84))
* **api:** api update ([#469](https://github.com/runloopai/api-client-python/issues/469)) ([e360b33](https://github.com/runloopai/api-client-python/commit/e360b330e21ff2d5f40245fec4abbcc9c855984b))
* **api:** api update ([#470](https://github.com/runloopai/api-client-python/issues/470)) ([4d451be](https://github.com/runloopai/api-client-python/commit/4d451be9763d647a65e3b808a5df2c4bb558c2e4))
* **api:** api update ([#471](https://github.com/runloopai/api-client-python/issues/471)) ([00b4736](https://github.com/runloopai/api-client-python/commit/00b4736f593efd87110ce4f281e44b9573b6e88d))
* **api:** api update ([#472](https://github.com/runloopai/api-client-python/issues/472)) ([b3bb5a3](https://github.com/runloopai/api-client-python/commit/b3bb5a3a006b40c066ba7288b9f9f5d7ad650ed0))
* **api:** api update ([#473](https://github.com/runloopai/api-client-python/issues/473)) ([0ddbcd9](https://github.com/runloopai/api-client-python/commit/0ddbcd9f332326c4210302d457445eef85ad337c))
* **api:** api update ([#474](https://github.com/runloopai/api-client-python/issues/474)) ([bebafe7](https://github.com/runloopai/api-client-python/commit/bebafe76afd82928ba0b9b9904598ecf5664d698))
* **api:** api update ([#475](https://github.com/runloopai/api-client-python/issues/475)) ([493d9a5](https://github.com/runloopai/api-client-python/commit/493d9a5bc8c2116e7a028c7dd39b178a2c51640b))
* **api:** api update ([#476](https://github.com/runloopai/api-client-python/issues/476)) ([8a8c550](https://github.com/runloopai/api-client-python/commit/8a8c550238f0ecc3ab93773abfd37d28c631b9c3))


### Chores

* add missing isclass check ([#478](https://github.com/runloopai/api-client-python/issues/478)) ([1b477a3](https://github.com/runloopai/api-client-python/commit/1b477a378a9ea74c52c97c5e4741dc67ee96d409))
* **internal:** add support for TypeAliasType ([#430](https://github.com/runloopai/api-client-python/issues/430)) ([7c4be68](https://github.com/runloopai/api-client-python/commit/7c4be683074bf86d8caca25190508de59b855362))
* **internal:** bump pyright ([#429](https://github.com/runloopai/api-client-python/issues/429)) ([5546e05](https://github.com/runloopai/api-client-python/commit/5546e05bcb6a1f9b14a611dac0c954303429ad4a))
* **internal:** codegen related update ([#368](https://github.com/runloopai/api-client-python/issues/368)) ([6bbac9d](https://github.com/runloopai/api-client-python/commit/6bbac9dcd9cace70ade900d5e3261b2c4608cb31))
* **internal:** codegen related update ([#439](https://github.com/runloopai/api-client-python/issues/439)) ([0ea26b1](https://github.com/runloopai/api-client-python/commit/0ea26b1244c4b857b479acda101661981fac0d46))
* **internal:** codegen related update ([#453](https://github.com/runloopai/api-client-python/issues/453)) ([947ffa2](https://github.com/runloopai/api-client-python/commit/947ffa210c0d28bb2c2a900054043ede50a51afb))
* **internal:** codegen related update ([#454](https://github.com/runloopai/api-client-python/issues/454)) ([72127cd](https://github.com/runloopai/api-client-python/commit/72127cdedf2ad79beb513d2d5d0b9aeec6d60c39))
* **internal:** codegen related update ([#477](https://github.com/runloopai/api-client-python/issues/477)) ([648039b](https://github.com/runloopai/api-client-python/commit/648039bc42b0c39867408c204fd9e78b2bb3e1a9))
* **internal:** fix some typos ([#460](https://github.com/runloopai/api-client-python/issues/460)) ([1c17f0c](https://github.com/runloopai/api-client-python/commit/1c17f0c3f1fe28ec92c942ef1356c7a28a54a545))
* make the `Omit` type public ([#373](https://github.com/runloopai/api-client-python/issues/373)) ([1ec1400](https://github.com/runloopai/api-client-python/commit/1ec1400baa00a62d2e3cbe616423653be3d28f22))
* updates ([#479](https://github.com/runloopai/api-client-python/issues/479)) ([55b7d1d](https://github.com/runloopai/api-client-python/commit/55b7d1dd63c9e363328528a6412bd15d68d39885))


### Documentation

* **readme:** example snippet for client context manager ([#455](https://github.com/runloopai/api-client-python/issues/455)) ([8f57943](https://github.com/runloopai/api-client-python/commit/8f579438f9a3648049c29b264fa1afe0659f274b))

## 0.11.0 (2024-11-28)

Full Changelog: [v0.10.0...v0.11.0](https://github.com/runloopai/api-client-python/compare/v0.10.0...v0.11.0)

### Features

* **api:** api update ([#267](https://github.com/runloopai/api-client-python/issues/267)) ([27a2611](https://github.com/runloopai/api-client-python/commit/27a26112b3e3ba949ec93d51ba1c94886faa0d5a))
* **api:** api update ([#269](https://github.com/runloopai/api-client-python/issues/269)) ([398d7b7](https://github.com/runloopai/api-client-python/commit/398d7b722c7753f9fd739807d2102c5c5b193da2))
* **api:** api update ([#270](https://github.com/runloopai/api-client-python/issues/270)) ([79cdab5](https://github.com/runloopai/api-client-python/commit/79cdab53adf57783d0ec2c8d0034540805475e5d))
* **api:** api update ([#271](https://github.com/runloopai/api-client-python/issues/271)) ([b98e2c3](https://github.com/runloopai/api-client-python/commit/b98e2c39daa921abe3bbd420b0b4177e33254eff))
* **api:** api update ([#272](https://github.com/runloopai/api-client-python/issues/272)) ([cd352c7](https://github.com/runloopai/api-client-python/commit/cd352c7334be2b6f30a761f605075481f5f1c7fc))
* **api:** api update ([#273](https://github.com/runloopai/api-client-python/issues/273)) ([e98fc62](https://github.com/runloopai/api-client-python/commit/e98fc627b8d2e66c23c03d82625f4ae0cc74ce21))
* **api:** api update ([#274](https://github.com/runloopai/api-client-python/issues/274)) ([333d0bb](https://github.com/runloopai/api-client-python/commit/333d0bb20efe17979d3ea63b5288459b9a3c47e6))
* **api:** api update ([#275](https://github.com/runloopai/api-client-python/issues/275)) ([cccf52e](https://github.com/runloopai/api-client-python/commit/cccf52e723676a4814630b8fd4a19766d94cf185))
* **api:** api update ([#276](https://github.com/runloopai/api-client-python/issues/276)) ([1833bda](https://github.com/runloopai/api-client-python/commit/1833bda457c662c70d0630ef5eb12c97c609b0e2))
* **api:** api update ([#277](https://github.com/runloopai/api-client-python/issues/277)) ([a2e551d](https://github.com/runloopai/api-client-python/commit/a2e551d9380ee37b23ab0a58044d6cc94a020791))
* **api:** api update ([#278](https://github.com/runloopai/api-client-python/issues/278)) ([5f6bc45](https://github.com/runloopai/api-client-python/commit/5f6bc45e385d6b23613fcadc8f7bc4a74cef1583))
* **api:** api update ([#279](https://github.com/runloopai/api-client-python/issues/279)) ([93892e2](https://github.com/runloopai/api-client-python/commit/93892e2ae8db9503d99ec95676b233e9d08abc97))
* **api:** api update ([#280](https://github.com/runloopai/api-client-python/issues/280)) ([95d36c1](https://github.com/runloopai/api-client-python/commit/95d36c1cb3280e8f42d46dcdcc8df16781d60a07))
* **api:** api update ([#281](https://github.com/runloopai/api-client-python/issues/281)) ([d0e7fac](https://github.com/runloopai/api-client-python/commit/d0e7faca52892ff1c711ff3505b059c86b6452f8))
* **api:** api update ([#282](https://github.com/runloopai/api-client-python/issues/282)) ([774ba0e](https://github.com/runloopai/api-client-python/commit/774ba0e1cb1336b25e690c6541e22eefae405afa))
* **api:** api update ([#283](https://github.com/runloopai/api-client-python/issues/283)) ([302e7c3](https://github.com/runloopai/api-client-python/commit/302e7c377e769b51beeec0d42cb5a1a6b739d17f))
* **api:** api update ([#284](https://github.com/runloopai/api-client-python/issues/284)) ([aef73c2](https://github.com/runloopai/api-client-python/commit/aef73c253698f08bfd41e1ecff973a049d7c396b))
* **api:** api update ([#285](https://github.com/runloopai/api-client-python/issues/285)) ([1a6003d](https://github.com/runloopai/api-client-python/commit/1a6003d88c6a63c2fde4a0a005db61f325aa6c01))
* **api:** api update ([#286](https://github.com/runloopai/api-client-python/issues/286)) ([9037685](https://github.com/runloopai/api-client-python/commit/9037685a4878a19d019f8f7be82aaf9403a1f91a))
* **api:** api update ([#287](https://github.com/runloopai/api-client-python/issues/287)) ([8ecabea](https://github.com/runloopai/api-client-python/commit/8ecabea02eea09845fd8a95e835b1e81f727c184))
* **api:** api update ([#288](https://github.com/runloopai/api-client-python/issues/288)) ([c6ef6fc](https://github.com/runloopai/api-client-python/commit/c6ef6fcc80d222dd18deafb403da917586aa6c6e))
* **api:** api update ([#289](https://github.com/runloopai/api-client-python/issues/289)) ([72f5f56](https://github.com/runloopai/api-client-python/commit/72f5f56a91d93ae27963b3d04f7be2cac4a3407c))
* **api:** api update ([#290](https://github.com/runloopai/api-client-python/issues/290)) ([508bb3f](https://github.com/runloopai/api-client-python/commit/508bb3f4fdcea37e132daeec0ac541716a6593f0))
* **api:** api update ([#291](https://github.com/runloopai/api-client-python/issues/291)) ([2df9175](https://github.com/runloopai/api-client-python/commit/2df9175bb461c32c5a76ed022041a37ff90b884b))
* **api:** api update ([#292](https://github.com/runloopai/api-client-python/issues/292)) ([141e1f3](https://github.com/runloopai/api-client-python/commit/141e1f3280bffe4f157b75892c98f712ae743917))
* **api:** api update ([#293](https://github.com/runloopai/api-client-python/issues/293)) ([74ca2f8](https://github.com/runloopai/api-client-python/commit/74ca2f81390dce2102f7585ed7ce6a9258bc1937))
* **api:** api update ([#294](https://github.com/runloopai/api-client-python/issues/294)) ([8e69b95](https://github.com/runloopai/api-client-python/commit/8e69b957a277bd6a74efb3c597c1a1d17be1cb2f))
* **api:** api update ([#295](https://github.com/runloopai/api-client-python/issues/295)) ([9b3a76c](https://github.com/runloopai/api-client-python/commit/9b3a76cd012ead454dfc6091949cd68c16b38df7))
* **api:** api update ([#296](https://github.com/runloopai/api-client-python/issues/296)) ([4bd3edb](https://github.com/runloopai/api-client-python/commit/4bd3edb4653302caf33fc0c55ac557fb3a0fb121))
* **api:** api update ([#297](https://github.com/runloopai/api-client-python/issues/297)) ([3922954](https://github.com/runloopai/api-client-python/commit/392295465ee6e84bb89684c8695183e6fa5ce1e8))
* **api:** api update ([#298](https://github.com/runloopai/api-client-python/issues/298)) ([a4c9fb4](https://github.com/runloopai/api-client-python/commit/a4c9fb4c54499214cd4f6615d62bb14f793f234e))
* **api:** api update ([#299](https://github.com/runloopai/api-client-python/issues/299)) ([ba67b5d](https://github.com/runloopai/api-client-python/commit/ba67b5d476802b0834a0b8f0899a66763d36dea6))
* **api:** api update ([#300](https://github.com/runloopai/api-client-python/issues/300)) ([a571b57](https://github.com/runloopai/api-client-python/commit/a571b572959c4be2f650d675206bd0f01292c838))
* **api:** api update ([#301](https://github.com/runloopai/api-client-python/issues/301)) ([e8606c3](https://github.com/runloopai/api-client-python/commit/e8606c34b0e0a0045e0b936144508279386b0948))
* **api:** api update ([#302](https://github.com/runloopai/api-client-python/issues/302)) ([b7014fd](https://github.com/runloopai/api-client-python/commit/b7014fd51e57aa6c039a03c64e300a0d7fbafb12))
* **api:** api update ([#303](https://github.com/runloopai/api-client-python/issues/303)) ([4ffec44](https://github.com/runloopai/api-client-python/commit/4ffec442400cd8f5ae6e38947a0e553ba1c2d337))
* **api:** api update ([#304](https://github.com/runloopai/api-client-python/issues/304)) ([dbede4f](https://github.com/runloopai/api-client-python/commit/dbede4f50a54b1ff01ca8acc27c29a8b64be3bc9))
* **api:** api update ([#305](https://github.com/runloopai/api-client-python/issues/305)) ([d62a804](https://github.com/runloopai/api-client-python/commit/d62a8048c54c122b1f7b8bf089a4c95ee99fb0b8))
* **api:** api update ([#306](https://github.com/runloopai/api-client-python/issues/306)) ([ebf7fe1](https://github.com/runloopai/api-client-python/commit/ebf7fe15dced48ed132f58a94c90df1d3718d9f8))
* **api:** api update ([#309](https://github.com/runloopai/api-client-python/issues/309)) ([3fd934e](https://github.com/runloopai/api-client-python/commit/3fd934e52e9b19be00d28af23bb517e3a0ae3697))
* **api:** api update ([#311](https://github.com/runloopai/api-client-python/issues/311)) ([2524093](https://github.com/runloopai/api-client-python/commit/252409344c379fe9727ece4a1596f427a2ebc2e8))
* **api:** api update ([#312](https://github.com/runloopai/api-client-python/issues/312)) ([f2b4f2e](https://github.com/runloopai/api-client-python/commit/f2b4f2e2c1e0dbf7ae37d727cd1093ca5a41a46a))
* **api:** api update ([#313](https://github.com/runloopai/api-client-python/issues/313)) ([a896e14](https://github.com/runloopai/api-client-python/commit/a896e149b0fe163943e3b7f3f9dd7ddd0e60a6e4))
* **api:** api update ([#314](https://github.com/runloopai/api-client-python/issues/314)) ([3982687](https://github.com/runloopai/api-client-python/commit/3982687a256f394ea63f033fd813be7e5b31d427))
* **api:** api update ([#315](https://github.com/runloopai/api-client-python/issues/315)) ([1ee6056](https://github.com/runloopai/api-client-python/commit/1ee6056207eb7f703cb95ebe9727e622af69b3a7))
* **api:** api update ([#316](https://github.com/runloopai/api-client-python/issues/316)) ([e64ddd0](https://github.com/runloopai/api-client-python/commit/e64ddd09504b49e4242a2e9232dc8f595815851b))
* **api:** api update ([#317](https://github.com/runloopai/api-client-python/issues/317)) ([4800de8](https://github.com/runloopai/api-client-python/commit/4800de804b193396267ca7d82827c671bf07cc69))
* **api:** api update ([#318](https://github.com/runloopai/api-client-python/issues/318)) ([60ba766](https://github.com/runloopai/api-client-python/commit/60ba766d958773f72ff75eb9053f2b5c14a2bf95))
* **api:** api update ([#319](https://github.com/runloopai/api-client-python/issues/319)) ([b999876](https://github.com/runloopai/api-client-python/commit/b9998763ff2cd25e8bffa62b67cb89725ed6e3d2))
* **api:** api update ([#320](https://github.com/runloopai/api-client-python/issues/320)) ([ed99ec5](https://github.com/runloopai/api-client-python/commit/ed99ec5c2cae033e1dc9dafa008e0b671d9df34e))
* **api:** api update ([#321](https://github.com/runloopai/api-client-python/issues/321)) ([d7ce737](https://github.com/runloopai/api-client-python/commit/d7ce737ee6b7c344775f771ea2f30c2c1a784de2))
* **api:** api update ([#322](https://github.com/runloopai/api-client-python/issues/322)) ([e579ee9](https://github.com/runloopai/api-client-python/commit/e579ee9a22c83ba70c1aa10e6d9914918a75f071))
* **api:** api update ([#323](https://github.com/runloopai/api-client-python/issues/323)) ([06bb999](https://github.com/runloopai/api-client-python/commit/06bb999b0c035ed3eba2afca77d5ed8255504c8d))
* **api:** api update ([#324](https://github.com/runloopai/api-client-python/issues/324)) ([42230ec](https://github.com/runloopai/api-client-python/commit/42230ecaabbdc11a5f679f0a08ade37d20054209))
* **api:** api update ([#325](https://github.com/runloopai/api-client-python/issues/325)) ([9436f02](https://github.com/runloopai/api-client-python/commit/9436f027948774046458eabe6e944c57ffedcda9))
* **api:** api update ([#326](https://github.com/runloopai/api-client-python/issues/326)) ([2a97e59](https://github.com/runloopai/api-client-python/commit/2a97e59370c7f5e8abf401925c34467d394bc0ca))
* **api:** api update ([#327](https://github.com/runloopai/api-client-python/issues/327)) ([a6d07d7](https://github.com/runloopai/api-client-python/commit/a6d07d7c76fb9603efd16a7cacd772fee20bf00a))
* **api:** api update ([#328](https://github.com/runloopai/api-client-python/issues/328)) ([c419733](https://github.com/runloopai/api-client-python/commit/c4197333afcca88247de48454aeec3b73dc6f311))
* **api:** api update ([#329](https://github.com/runloopai/api-client-python/issues/329)) ([27e682c](https://github.com/runloopai/api-client-python/commit/27e682cc6dbb4bc26e9aff61ff15750d2a81b35f))
* **api:** api update ([#330](https://github.com/runloopai/api-client-python/issues/330)) ([4c27571](https://github.com/runloopai/api-client-python/commit/4c27571161a897fcc91ef5ed03f412b576422d7e))
* **api:** api update ([#331](https://github.com/runloopai/api-client-python/issues/331)) ([2c25235](https://github.com/runloopai/api-client-python/commit/2c2523591b58197c9b4f2bc66bf62778ec755116))
* **api:** api update ([#332](https://github.com/runloopai/api-client-python/issues/332)) ([60a1eeb](https://github.com/runloopai/api-client-python/commit/60a1eeb424ee0f98086040df97adf8d35f3de853))
* **api:** api update ([#333](https://github.com/runloopai/api-client-python/issues/333)) ([76b345c](https://github.com/runloopai/api-client-python/commit/76b345cb318a5a35843c56d9dc2bd3d8feb35332))
* **api:** api update ([#334](https://github.com/runloopai/api-client-python/issues/334)) ([e77b717](https://github.com/runloopai/api-client-python/commit/e77b717c18eb666a537e4bb8d1df8835d6f34524))
* **api:** api update ([#335](https://github.com/runloopai/api-client-python/issues/335)) ([5eb9c88](https://github.com/runloopai/api-client-python/commit/5eb9c88abe61ad81b20d8fcf98a74f28361f61f7))
* **api:** api update ([#336](https://github.com/runloopai/api-client-python/issues/336)) ([fa539cd](https://github.com/runloopai/api-client-python/commit/fa539cd278e71823e8269a1930fbca4a88d3501c))
* **api:** api update ([#337](https://github.com/runloopai/api-client-python/issues/337)) ([f9abf13](https://github.com/runloopai/api-client-python/commit/f9abf131f6fd9f55820fe752c939445814bfc7f3))
* **api:** api update ([#338](https://github.com/runloopai/api-client-python/issues/338)) ([475b693](https://github.com/runloopai/api-client-python/commit/475b693bbc0f7b33a5a5521a977034c26b0a9a1a))
* **api:** api update ([#339](https://github.com/runloopai/api-client-python/issues/339)) ([916bc6e](https://github.com/runloopai/api-client-python/commit/916bc6e1a13647c807efff4caa5154878b34f255))
* **api:** api update ([#340](https://github.com/runloopai/api-client-python/issues/340)) ([e42de98](https://github.com/runloopai/api-client-python/commit/e42de98281c8a85de94b7c73f9d4bff5bf9c06d1))
* **api:** api update ([#341](https://github.com/runloopai/api-client-python/issues/341)) ([710172d](https://github.com/runloopai/api-client-python/commit/710172d20f6b6d146e6bf162b6eb6ba23a0d8a61))
* **api:** api update ([#342](https://github.com/runloopai/api-client-python/issues/342)) ([6a3dbb2](https://github.com/runloopai/api-client-python/commit/6a3dbb21f7dec203a87a0bf107ad3c9c8639871c))
* **api:** api update ([#344](https://github.com/runloopai/api-client-python/issues/344)) ([59209ff](https://github.com/runloopai/api-client-python/commit/59209ffdf4281004001334e1c42d49d1e86e0af1))
* **api:** api update ([#345](https://github.com/runloopai/api-client-python/issues/345)) ([9a8181d](https://github.com/runloopai/api-client-python/commit/9a8181d13f619f837d314602ce386f6670b065db))
* **api:** api update ([#346](https://github.com/runloopai/api-client-python/issues/346)) ([f708cd1](https://github.com/runloopai/api-client-python/commit/f708cd15a4854ef22efd57d0c1f4a8be5fbfbd27))
* **api:** api update ([#347](https://github.com/runloopai/api-client-python/issues/347)) ([30b5ee7](https://github.com/runloopai/api-client-python/commit/30b5ee74fd1e5e7f2e46320e34fa62ed7a919703))
* **api:** api update ([#348](https://github.com/runloopai/api-client-python/issues/348)) ([782a004](https://github.com/runloopai/api-client-python/commit/782a00400b83412f825a4d444e22a367744897aa))
* **api:** api update ([#349](https://github.com/runloopai/api-client-python/issues/349)) ([acd7cfb](https://github.com/runloopai/api-client-python/commit/acd7cfb069944becb21eedaf87e7440c24b20f3a))
* **api:** api update ([#350](https://github.com/runloopai/api-client-python/issues/350)) ([9858df4](https://github.com/runloopai/api-client-python/commit/9858df4f852a7ce483c4cfe8b699f890a2ea4e22))
* **api:** api update ([#351](https://github.com/runloopai/api-client-python/issues/351)) ([c1e84ff](https://github.com/runloopai/api-client-python/commit/c1e84ff7abf538dfc679043c0daeaaa1e0f80421))
* **api:** api update ([#352](https://github.com/runloopai/api-client-python/issues/352)) ([fc60fd0](https://github.com/runloopai/api-client-python/commit/fc60fd02dd00af413821efcc785466efae9bef74))
* **api:** api update ([#353](https://github.com/runloopai/api-client-python/issues/353)) ([d29d0c4](https://github.com/runloopai/api-client-python/commit/d29d0c449ef2f7b9a907bb367e25b48268a0f52d))
* **api:** api update ([#354](https://github.com/runloopai/api-client-python/issues/354)) ([30c029d](https://github.com/runloopai/api-client-python/commit/30c029da2929112aeb9235fefe90c8214386e69d))
* **api:** api update ([#358](https://github.com/runloopai/api-client-python/issues/358)) ([c237f10](https://github.com/runloopai/api-client-python/commit/c237f108a6e821ec1d7314eae4a80f1ae2915de2))


### Bug Fixes

* **client:** compat with new httpx 0.28.0 release ([#360](https://github.com/runloopai/api-client-python/issues/360)) ([5e16307](https://github.com/runloopai/api-client-python/commit/5e16307ebb08fca6109d091110a31ac4f4ce0c3d))


### Chores

* **internal:** codegen related update ([#343](https://github.com/runloopai/api-client-python/issues/343)) ([68a4523](https://github.com/runloopai/api-client-python/commit/68a4523484de412f223a9fc23f7fd7c899bfac1b))
* **internal:** exclude mypy from running on tests ([#359](https://github.com/runloopai/api-client-python/issues/359)) ([8b8fe06](https://github.com/runloopai/api-client-python/commit/8b8fe069e4ad23fc135edbec1f1cf820af3051fe))
* **internal:** fix compat model_dump method when warnings are passed ([#355](https://github.com/runloopai/api-client-python/issues/355)) ([59c36a0](https://github.com/runloopai/api-client-python/commit/59c36a0f71664897f3e052b88fae4ecef1be5293))
* rebuild project due to codegen change ([#307](https://github.com/runloopai/api-client-python/issues/307)) ([6e6a696](https://github.com/runloopai/api-client-python/commit/6e6a696b3022be537883fcc8043621995a2d38e7))
* rebuild project due to codegen change ([#308](https://github.com/runloopai/api-client-python/issues/308)) ([11883c9](https://github.com/runloopai/api-client-python/commit/11883c976db1945018715995d61130d6bbb3cb32))
* remove now unused `cached-property` dep ([#357](https://github.com/runloopai/api-client-python/issues/357)) ([919b44c](https://github.com/runloopai/api-client-python/commit/919b44c00b390614192d74048b7468b00fea336a))


### Documentation

* add info log level to readme ([#356](https://github.com/runloopai/api-client-python/issues/356)) ([8fc311d](https://github.com/runloopai/api-client-python/commit/8fc311d98d4c14ae5336b2cc21f686ce2bb414a8))

## 0.10.0 (2024-11-08)

Full Changelog: [v0.9.0...v0.10.0](https://github.com/runloopai/api-client-python/compare/v0.9.0...v0.10.0)

### Features

* **api:** api update ([#257](https://github.com/runloopai/api-client-python/issues/257)) ([d4d01da](https://github.com/runloopai/api-client-python/commit/d4d01da46da8bd0382c363d7fdfd07a173df258f))
* **api:** api update ([#259](https://github.com/runloopai/api-client-python/issues/259)) ([c695aa0](https://github.com/runloopai/api-client-python/commit/c695aa09be21d33c93f81ed96a03fe962f05502f))
* **api:** api update ([#260](https://github.com/runloopai/api-client-python/issues/260)) ([ac9193f](https://github.com/runloopai/api-client-python/commit/ac9193f436faab5dc5bf50b4370209c9b20e0f8f))
* **api:** api update ([#261](https://github.com/runloopai/api-client-python/issues/261)) ([5a7fce2](https://github.com/runloopai/api-client-python/commit/5a7fce220c30d8d506a476da5a04bb358d12c5b4))
* **api:** api update ([#262](https://github.com/runloopai/api-client-python/issues/262)) ([b463693](https://github.com/runloopai/api-client-python/commit/b463693a843a2e1326794f80d5392555249a82ba))
* **api:** api update ([#263](https://github.com/runloopai/api-client-python/issues/263)) ([dbd490a](https://github.com/runloopai/api-client-python/commit/dbd490a359ad8c18f6fdaa03cea217e6e7621149))
* **api:** api update ([#264](https://github.com/runloopai/api-client-python/issues/264)) ([0380eb2](https://github.com/runloopai/api-client-python/commit/0380eb25cc4f938ae4c03d5ddcaa172f3bd1bc4b))
* **api:** api update ([#265](https://github.com/runloopai/api-client-python/issues/265)) ([2827aeb](https://github.com/runloopai/api-client-python/commit/2827aeb67e07858e28752b19e1184c4479f0a73e))

## 0.9.0 (2024-11-07)

Full Changelog: [v0.8.0...v0.9.0](https://github.com/runloopai/api-client-python/compare/v0.8.0...v0.9.0)

### Features

* **api:** api update ([#252](https://github.com/runloopai/api-client-python/issues/252)) ([aa42dcb](https://github.com/runloopai/api-client-python/commit/aa42dcb4969d68d69c6a421dd709593e5b8cadf7))
* **api:** api update ([#254](https://github.com/runloopai/api-client-python/issues/254)) ([a310c68](https://github.com/runloopai/api-client-python/commit/a310c68d10e409feaac6ce65e1e69ae44fb42e8f))
* **api:** manual updates ([#255](https://github.com/runloopai/api-client-python/issues/255)) ([4eafcf0](https://github.com/runloopai/api-client-python/commit/4eafcf077fa764359f26e01ad85024dc1db9873e))

## 0.8.0 (2024-11-06)

Full Changelog: [v0.7.0...v0.8.0](https://github.com/runloopai/api-client-python/compare/v0.7.0...v0.8.0)

### Features

* **api:** api update ([#239](https://github.com/runloopai/api-client-python/issues/239)) ([e265611](https://github.com/runloopai/api-client-python/commit/e2656115c0ee73db6d73cf1e1efbec97988ff064))
* **api:** api update ([#241](https://github.com/runloopai/api-client-python/issues/241)) ([d69d8a8](https://github.com/runloopai/api-client-python/commit/d69d8a86ab004b4b689a8585c570ed4857af4353))
* **api:** api update ([#242](https://github.com/runloopai/api-client-python/issues/242)) ([ad2f4c7](https://github.com/runloopai/api-client-python/commit/ad2f4c75052d843b3ae1bf174b37d8b3cbfe682d))
* **api:** api update ([#243](https://github.com/runloopai/api-client-python/issues/243)) ([7b6c98f](https://github.com/runloopai/api-client-python/commit/7b6c98f6e753f36ace4804c8b3e50d2f24fca817))
* **api:** api update ([#244](https://github.com/runloopai/api-client-python/issues/244)) ([12d0039](https://github.com/runloopai/api-client-python/commit/12d0039440149afac4e599333d3c8390239f0c0f))
* **api:** api update ([#245](https://github.com/runloopai/api-client-python/issues/245)) ([2b82f31](https://github.com/runloopai/api-client-python/commit/2b82f3176032293211710a81c9c18b326cc703ad))
* **api:** api update ([#246](https://github.com/runloopai/api-client-python/issues/246)) ([ee79233](https://github.com/runloopai/api-client-python/commit/ee7923350b3bb77b52cfc30d94cadd0c06965a9d))
* **api:** api update ([#247](https://github.com/runloopai/api-client-python/issues/247)) ([492e315](https://github.com/runloopai/api-client-python/commit/492e3150dd7b27ba1b849dec84e11e9e37997037))
* **api:** api update ([#248](https://github.com/runloopai/api-client-python/issues/248)) ([045ec22](https://github.com/runloopai/api-client-python/commit/045ec22efdee8eee4f016560a16c8900666b604d))
* **api:** api update ([#249](https://github.com/runloopai/api-client-python/issues/249)) ([baa457c](https://github.com/runloopai/api-client-python/commit/baa457c6a26cca584443372f0663477fd9bc7cdd))
* **api:** api update ([#250](https://github.com/runloopai/api-client-python/issues/250)) ([e69b069](https://github.com/runloopai/api-client-python/commit/e69b069b03683916c6c96ee8a8fa1a4f2d8ba557))

## 0.7.0 (2024-10-24)

Full Changelog: [v0.6.0...v0.7.0](https://github.com/runloopai/api-client-python/compare/v0.6.0...v0.7.0)

### Features

* **api:** api update ([#236](https://github.com/runloopai/api-client-python/issues/236)) ([912af5f](https://github.com/runloopai/api-client-python/commit/912af5fa9dfa10f999727d912cd06483ce197a68))

## 0.6.0 (2024-10-23)

Full Changelog: [v0.5.0...v0.6.0](https://github.com/runloopai/api-client-python/compare/v0.5.0...v0.6.0)

### Features

* **api:** api update ([#231](https://github.com/runloopai/api-client-python/issues/231)) ([c71e7f5](https://github.com/runloopai/api-client-python/commit/c71e7f5cdc94bd826218c4034abc222b40349e39))
* **api:** api update ([#233](https://github.com/runloopai/api-client-python/issues/233)) ([5ca0335](https://github.com/runloopai/api-client-python/commit/5ca0335166c5f731fb0fd19909fb7d5605631605))
* **api:** api update ([#234](https://github.com/runloopai/api-client-python/issues/234)) ([e43ae1a](https://github.com/runloopai/api-client-python/commit/e43ae1abca60530ebd439c454e56b8a2a9116554))

## 0.5.0 (2024-10-22)

Full Changelog: [v0.4.0...v0.5.0](https://github.com/runloopai/api-client-python/compare/v0.4.0...v0.5.0)

### Features

* **api:** api update ([#224](https://github.com/runloopai/api-client-python/issues/224)) ([f536d22](https://github.com/runloopai/api-client-python/commit/f536d22b28c9c92d08267ae902dafb2e9a825e38))
* **api:** api update ([#226](https://github.com/runloopai/api-client-python/issues/226)) ([c3f93d1](https://github.com/runloopai/api-client-python/commit/c3f93d1109b5e04afe3c42881b6989e4a940dbf0))
* **api:** api update ([#227](https://github.com/runloopai/api-client-python/issues/227)) ([ea18fbc](https://github.com/runloopai/api-client-python/commit/ea18fbca67b109d03123effd8b1a5451d041fef5))
* **api:** api update ([#228](https://github.com/runloopai/api-client-python/issues/228)) ([e5ac996](https://github.com/runloopai/api-client-python/commit/e5ac996e3e4092c2ee513cfe928650f7c3628eb7))
* **api:** api update ([#229](https://github.com/runloopai/api-client-python/issues/229)) ([df42110](https://github.com/runloopai/api-client-python/commit/df4211097357294424738157119e43f03e9e6da5))

## 0.4.0 (2024-10-22)

Full Changelog: [v0.3.0...v0.4.0](https://github.com/runloopai/api-client-python/compare/v0.3.0...v0.4.0)

### Features

* **api:** api update ([#206](https://github.com/runloopai/api-client-python/issues/206)) ([1018bb4](https://github.com/runloopai/api-client-python/commit/1018bb4e9416e4d88ba82f435b61c8aba3f1235a))
* **api:** api update ([#208](https://github.com/runloopai/api-client-python/issues/208)) ([d0c2bd8](https://github.com/runloopai/api-client-python/commit/d0c2bd8ec96edae0a96208d12049991e3ed05a87))
* **api:** api update ([#209](https://github.com/runloopai/api-client-python/issues/209)) ([5ba4709](https://github.com/runloopai/api-client-python/commit/5ba470949ffd1772f7211769aaf44d848f46fc58))
* **api:** api update ([#210](https://github.com/runloopai/api-client-python/issues/210)) ([620fcb9](https://github.com/runloopai/api-client-python/commit/620fcb90f24fe01804bd73ed970e3af0d3f65009))
* **api:** api update ([#211](https://github.com/runloopai/api-client-python/issues/211)) ([b181289](https://github.com/runloopai/api-client-python/commit/b18128942293ab07b3fa1b40cd05061746b5d17c))
* **api:** api update ([#212](https://github.com/runloopai/api-client-python/issues/212)) ([6410fed](https://github.com/runloopai/api-client-python/commit/6410fed4c958f4d38dea32fa7c2b894fb2424549))
* **api:** api update ([#213](https://github.com/runloopai/api-client-python/issues/213)) ([4c7552a](https://github.com/runloopai/api-client-python/commit/4c7552ae74d688a75a95cbf9e0147156dd558469))
* **api:** api update ([#214](https://github.com/runloopai/api-client-python/issues/214)) ([a02b476](https://github.com/runloopai/api-client-python/commit/a02b4763d6c7e2a47b300c6274a9b6b0a5f620dd))
* **api:** api update ([#215](https://github.com/runloopai/api-client-python/issues/215)) ([87fb66e](https://github.com/runloopai/api-client-python/commit/87fb66ed3d8126db93eb5b7245c10fb2fcf4533b))
* **api:** api update ([#216](https://github.com/runloopai/api-client-python/issues/216)) ([568d2f8](https://github.com/runloopai/api-client-python/commit/568d2f821df99bff0bd4ea31f1398df94dccbf2d))
* **api:** api update ([#217](https://github.com/runloopai/api-client-python/issues/217)) ([23902ae](https://github.com/runloopai/api-client-python/commit/23902aead147c749528b726d25c92d72cf0fb5f5))
* **api:** api update ([#218](https://github.com/runloopai/api-client-python/issues/218)) ([5bd1497](https://github.com/runloopai/api-client-python/commit/5bd1497d6b23f0630b74a38696f52c7d691a9a50))
* **api:** api update ([#219](https://github.com/runloopai/api-client-python/issues/219)) ([c2f5075](https://github.com/runloopai/api-client-python/commit/c2f5075c8a230524c457b491a8a796550d43695b))
* **api:** api update ([#220](https://github.com/runloopai/api-client-python/issues/220)) ([6bc6ffb](https://github.com/runloopai/api-client-python/commit/6bc6ffbd7f13204744b9f7e29f129326ea38229a))
* **api:** api update ([#221](https://github.com/runloopai/api-client-python/issues/221)) ([da27ecc](https://github.com/runloopai/api-client-python/commit/da27eccbfa6df1075e1a20d9e4a4d6abea31f731))
* **api:** api update ([#222](https://github.com/runloopai/api-client-python/issues/222)) ([753ea7c](https://github.com/runloopai/api-client-python/commit/753ea7cd62cccc384166223f762af1cfea06c08e))

## 0.3.0 (2024-10-14)

Full Changelog: [v0.2.2...v0.3.0](https://github.com/runloopai/api-client-python/compare/v0.2.2...v0.3.0)

### Features

* **api:** api update ([#203](https://github.com/runloopai/api-client-python/issues/203)) ([596e9db](https://github.com/runloopai/api-client-python/commit/596e9db0165308c969e1c7dc2079d4d12961b382))

## 0.2.2 (2024-10-11)

Full Changelog: [v0.2.0...v0.2.2](https://github.com/runloopai/api-client-python/compare/v0.2.0...v0.2.2)

### Features

* **api:** api update ([#190](https://github.com/runloopai/api-client-python/issues/190)) ([4b40a20](https://github.com/runloopai/api-client-python/commit/4b40a20d3603f8a0dfdb0ecf8884682193e986d9))
* **api:** api update ([#192](https://github.com/runloopai/api-client-python/issues/192)) ([51358a5](https://github.com/runloopai/api-client-python/commit/51358a52a59b31729f05c40a6f84af467313f568))
* **api:** api update ([#193](https://github.com/runloopai/api-client-python/issues/193)) ([d4c04da](https://github.com/runloopai/api-client-python/commit/d4c04da4e1726dd70a638748034e2c86ead63142))
* **api:** api update ([#194](https://github.com/runloopai/api-client-python/issues/194)) ([31fcc6c](https://github.com/runloopai/api-client-python/commit/31fcc6cc52cc1e7cf782b9fd00d75049f455bb98))
* **api:** api update ([#195](https://github.com/runloopai/api-client-python/issues/195)) ([4b3112b](https://github.com/runloopai/api-client-python/commit/4b3112bb3e0620fbce4f37bdd4fe06e3bdbaa0d5))
* **api:** api update ([#196](https://github.com/runloopai/api-client-python/issues/196)) ([f367ac3](https://github.com/runloopai/api-client-python/commit/f367ac3014e94f4be43480fbb8404a8c95b853fe))
* **api:** api update ([#197](https://github.com/runloopai/api-client-python/issues/197)) ([f5d88d9](https://github.com/runloopai/api-client-python/commit/f5d88d970de6e2820449eedbddc424f387a147ff))
* **api:** api update ([#198](https://github.com/runloopai/api-client-python/issues/198)) ([6a8c688](https://github.com/runloopai/api-client-python/commit/6a8c688473c715c6bf82a81084a414ea844bac01))
* **api:** api update ([#199](https://github.com/runloopai/api-client-python/issues/199)) ([e36adf9](https://github.com/runloopai/api-client-python/commit/e36adf900d0c7ee4e25ea1d806c2da2f17cc48eb))
* **api:** api update ([#200](https://github.com/runloopai/api-client-python/issues/200)) ([2b51e56](https://github.com/runloopai/api-client-python/commit/2b51e5641684c23ddaaf23131b3fe8eba0877925))

## 0.2.0 (2024-10-10)

Full Changelog: [v0.1.0-alpha.23...v0.2.0](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.23...v0.2.0)

### Features

* **api:** api update ([#186](https://github.com/runloopai/api-client-python/issues/186)) ([bee1e4f](https://github.com/runloopai/api-client-python/commit/bee1e4fb7aa9e167396927f712400223a6f176b2))
* **api:** api update ([#188](https://github.com/runloopai/api-client-python/issues/188)) ([0b28873](https://github.com/runloopai/api-client-python/commit/0b28873e3bf6ce5ab6d35e8a30e0184d431fad4f))
* **api:** api update ([#189](https://github.com/runloopai/api-client-python/issues/189)) ([b0226b9](https://github.com/runloopai/api-client-python/commit/b0226b926a346ef24886dc5550da8a5275f9c9a2))

## 0.1.0-alpha.23 (2024-10-07)

Full Changelog: [v0.1.0-alpha.22...v0.1.0-alpha.23](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.22...v0.1.0-alpha.23)

### Features

* **api:** OpenAPI spec update via Stainless API ([#177](https://github.com/runloopai/api-client-python/issues/177)) ([ffb1036](https://github.com/runloopai/api-client-python/commit/ffb1036dbfc4cbd07a13ecdd2b18325604d7674c))
* **api:** OpenAPI spec update via Stainless API ([#179](https://github.com/runloopai/api-client-python/issues/179)) ([77911b5](https://github.com/runloopai/api-client-python/commit/77911b5618161d23bba170802f102308ba21c13e))
* **api:** OpenAPI spec update via Stainless API ([#180](https://github.com/runloopai/api-client-python/issues/180)) ([0849ddb](https://github.com/runloopai/api-client-python/commit/0849ddb9062ba0c2e3d2adfb2e2b3f2f72f4c29b))
* **api:** OpenAPI spec update via Stainless API ([#184](https://github.com/runloopai/api-client-python/issues/184)) ([7022855](https://github.com/runloopai/api-client-python/commit/702285559eac8be1082f7a0b7a8f66d034377286))


### Bug Fixes

* **client:** avoid OverflowError with very large retry counts ([#182](https://github.com/runloopai/api-client-python/issues/182)) ([c183989](https://github.com/runloopai/api-client-python/commit/c183989104d3e2e283a082999ca5c6b5e93a463e))


### Chores

* add repr to PageInfo class ([#183](https://github.com/runloopai/api-client-python/issues/183)) ([29b7283](https://github.com/runloopai/api-client-python/commit/29b7283228e3fa02621d65b93efff058c4330cba))
* **internal:** add support for parsing bool response content ([#181](https://github.com/runloopai/api-client-python/issues/181)) ([e2f1795](https://github.com/runloopai/api-client-python/commit/e2f1795c158baaf93118af62d4156629aa2ac816))

## 0.1.0-alpha.22 (2024-10-01)

Full Changelog: [v0.1.0-alpha.21...v0.1.0-alpha.22](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.21...v0.1.0-alpha.22)

### Features

* **api:** OpenAPI spec update via Stainless API ([#174](https://github.com/runloopai/api-client-python/issues/174)) ([83ea2bc](https://github.com/runloopai/api-client-python/commit/83ea2bc3a8e222ab35f23145ba30a003574719a8))

## 0.1.0-alpha.21 (2024-10-01)

Full Changelog: [v0.1.0-alpha.20...v0.1.0-alpha.21](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.20...v0.1.0-alpha.21)

### Features

* **api:** OpenAPI spec update via Stainless API ([#156](https://github.com/runloopai/api-client-python/issues/156)) ([1594f34](https://github.com/runloopai/api-client-python/commit/1594f3430e0ad1f1441fdeaaf374760b9e2edfe6))
* **api:** OpenAPI spec update via Stainless API ([#160](https://github.com/runloopai/api-client-python/issues/160)) ([ee5dccc](https://github.com/runloopai/api-client-python/commit/ee5dccc7797e5786d627c5df12c9ccdf9bcf46c5))
* **api:** OpenAPI spec update via Stainless API ([#161](https://github.com/runloopai/api-client-python/issues/161)) ([47f9ac6](https://github.com/runloopai/api-client-python/commit/47f9ac690ce50b93675eab8bfa0d17b9059b8a44))
* **api:** OpenAPI spec update via Stainless API ([#162](https://github.com/runloopai/api-client-python/issues/162)) ([0ac9009](https://github.com/runloopai/api-client-python/commit/0ac900945faa6d3d273011e1928be6601e8497bb))
* **api:** OpenAPI spec update via Stainless API ([#163](https://github.com/runloopai/api-client-python/issues/163)) ([c819584](https://github.com/runloopai/api-client-python/commit/c8195846f3185b500783ece288d3252690c75ab9))
* **api:** OpenAPI spec update via Stainless API ([#167](https://github.com/runloopai/api-client-python/issues/167)) ([3a84eea](https://github.com/runloopai/api-client-python/commit/3a84eea63b488bde4821fe8787aa4c5a3abb98a0))
* **api:** OpenAPI spec update via Stainless API ([#168](https://github.com/runloopai/api-client-python/issues/168)) ([c9a19cb](https://github.com/runloopai/api-client-python/commit/c9a19cb521ce8168566f01373039d555dde6ff08))
* **api:** OpenAPI spec update via Stainless API ([#171](https://github.com/runloopai/api-client-python/issues/171)) ([d814a44](https://github.com/runloopai/api-client-python/commit/d814a441646b587ad10d985cc8e38c2e2e5399a4))
* **client:** send retry count header ([#170](https://github.com/runloopai/api-client-python/issues/170)) ([8390f52](https://github.com/runloopai/api-client-python/commit/8390f52895f48665cf09c3a87e61fef2cc0c3027))


### Bug Fixes

* **client:** handle domains with underscores ([#169](https://github.com/runloopai/api-client-python/issues/169)) ([8485f86](https://github.com/runloopai/api-client-python/commit/8485f8692c5bcb94cbc4f4389b6e30117c0231aa))


### Chores

* add docstrings to raw response properties ([#158](https://github.com/runloopai/api-client-python/issues/158)) ([762a6b3](https://github.com/runloopai/api-client-python/commit/762a6b3ae34b6b4f3797e56a0464c421d66edeb8))
* **internal:** bump pyright / mypy version ([#166](https://github.com/runloopai/api-client-python/issues/166)) ([69bc4f3](https://github.com/runloopai/api-client-python/commit/69bc4f338353430426ca64873bff8fff5a40313a))
* **internal:** bump ruff ([#165](https://github.com/runloopai/api-client-python/issues/165)) ([1085a1c](https://github.com/runloopai/api-client-python/commit/1085a1cbd2f039c971b337827bb87e35d9f9941f))
* **internal:** codegen related update ([#172](https://github.com/runloopai/api-client-python/issues/172)) ([b2e05d5](https://github.com/runloopai/api-client-python/commit/b2e05d5f307c618a0407a55744c97c9a44721f60))


### Documentation

* **readme:** add section on determining installed version ([#159](https://github.com/runloopai/api-client-python/issues/159)) ([9f23958](https://github.com/runloopai/api-client-python/commit/9f239589e7a058b54ef79d25944f43a49621940b))
* update CONTRIBUTING.md ([#164](https://github.com/runloopai/api-client-python/issues/164)) ([169ef14](https://github.com/runloopai/api-client-python/commit/169ef149c8db980beb50b72823d4b2b87c202846))

## 0.1.0-alpha.20 (2024-09-06)

Full Changelog: [v0.1.0-alpha.19...v0.1.0-alpha.20](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.19...v0.1.0-alpha.20)

### Features

* **api:** OpenAPI spec update via Stainless API ([#143](https://github.com/runloopai/api-client-python/issues/143)) ([8cd8b77](https://github.com/runloopai/api-client-python/commit/8cd8b77a11e70d8a9c46d813ffc5d99ba7fc956d))
* **api:** OpenAPI spec update via Stainless API ([#145](https://github.com/runloopai/api-client-python/issues/145)) ([ce6146e](https://github.com/runloopai/api-client-python/commit/ce6146e94e0e54c2c3eabe091129c172f0bc146e))
* **api:** OpenAPI spec update via Stainless API ([#146](https://github.com/runloopai/api-client-python/issues/146)) ([21a9a9c](https://github.com/runloopai/api-client-python/commit/21a9a9cc37354f1d4b597e24de694cd9680b95d0))
* **api:** OpenAPI spec update via Stainless API ([#147](https://github.com/runloopai/api-client-python/issues/147)) ([79994e5](https://github.com/runloopai/api-client-python/commit/79994e52f36038f3d2a38f9cb9639a753ac9d7f4))
* **api:** OpenAPI spec update via Stainless API ([#148](https://github.com/runloopai/api-client-python/issues/148)) ([e645bda](https://github.com/runloopai/api-client-python/commit/e645bda8f821763db0b184f2ad3e66220b844a55))
* **api:** OpenAPI spec update via Stainless API ([#150](https://github.com/runloopai/api-client-python/issues/150)) ([0017597](https://github.com/runloopai/api-client-python/commit/00175979cd1f3ccad4b9ded0b27e0fbb15b31fd6))
* **api:** OpenAPI spec update via Stainless API ([#151](https://github.com/runloopai/api-client-python/issues/151)) ([7b9f2fa](https://github.com/runloopai/api-client-python/commit/7b9f2fad3474a08fc4814574db7715b7c4d69182))
* **api:** OpenAPI spec update via Stainless API ([#152](https://github.com/runloopai/api-client-python/issues/152)) ([9845185](https://github.com/runloopai/api-client-python/commit/98451858216e7f414e6c81e32e3401bb0eee2f5d))
* **api:** OpenAPI spec update via Stainless API ([#154](https://github.com/runloopai/api-client-python/issues/154)) ([e6350ec](https://github.com/runloopai/api-client-python/commit/e6350ec396f5f081b8099e3cd760de097f0120f8))


### Chores

* pyproject.toml formatting changes ([#149](https://github.com/runloopai/api-client-python/issues/149)) ([9370c54](https://github.com/runloopai/api-client-python/commit/9370c543098a995dfdd10f5b020da92567af814e))

## 0.1.0-alpha.19 (2024-08-28)

Full Changelog: [v0.1.0-alpha.18...v0.1.0-alpha.19](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.18...v0.1.0-alpha.19)

### Features

* **api:** OpenAPI spec update via Stainless API ([#139](https://github.com/runloopai/api-client-python/issues/139)) ([f359981](https://github.com/runloopai/api-client-python/commit/f359981163f1358b9556c53a5f72e9cbe5a56a81))
* **api:** OpenAPI spec update via Stainless API ([#141](https://github.com/runloopai/api-client-python/issues/141)) ([ebd75f4](https://github.com/runloopai/api-client-python/commit/ebd75f4c3e4348e01cb107a77d92477d0906329a))

## 0.1.0-alpha.18 (2024-08-28)

Full Changelog: [v0.1.0-alpha.17...v0.1.0-alpha.18](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.17...v0.1.0-alpha.18)

### Features

* **api:** OpenAPI spec update via Stainless API ([#136](https://github.com/runloopai/api-client-python/issues/136)) ([ff032bf](https://github.com/runloopai/api-client-python/commit/ff032bfe0559d9057ff6c890349b5d002a60e6e6))

## 0.1.0-alpha.17 (2024-08-27)

Full Changelog: [v0.1.0-alpha.16...v0.1.0-alpha.17](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.16...v0.1.0-alpha.17)

### Features

* **api:** OpenAPI spec update via Stainless API ([#130](https://github.com/runloopai/api-client-python/issues/130)) ([fc8ef2f](https://github.com/runloopai/api-client-python/commit/fc8ef2f0b7510d5f368b5d0a12be0fcca1079f14))
* **api:** OpenAPI spec update via Stainless API ([#132](https://github.com/runloopai/api-client-python/issues/132)) ([29725a4](https://github.com/runloopai/api-client-python/commit/29725a4d63e38ef1f12cd19ead545cbb33a9e338))
* **api:** OpenAPI spec update via Stainless API ([#133](https://github.com/runloopai/api-client-python/issues/133)) ([9e05c97](https://github.com/runloopai/api-client-python/commit/9e05c97d9bf083d4356b71a141c988422484e6f5))
* **api:** OpenAPI spec update via Stainless API ([#134](https://github.com/runloopai/api-client-python/issues/134)) ([4c3fd59](https://github.com/runloopai/api-client-python/commit/4c3fd59f4c2e4a0bd87b7539b6cc37979bd4594e))

## 0.1.0-alpha.16 (2024-08-26)

Full Changelog: [v0.1.0-alpha.15...v0.1.0-alpha.16](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.15...v0.1.0-alpha.16)

### Features

* **api:** OpenAPI spec update via Stainless API ([#122](https://github.com/runloopai/api-client-python/issues/122)) ([e65a4b5](https://github.com/runloopai/api-client-python/commit/e65a4b5a0fafa23ba8070300dc11b4727ae03ed1))
* **api:** OpenAPI spec update via Stainless API ([#124](https://github.com/runloopai/api-client-python/issues/124)) ([cb87b6f](https://github.com/runloopai/api-client-python/commit/cb87b6f85ee0afcf20e6d5d9bb469b51cda29abe))
* **api:** OpenAPI spec update via Stainless API ([#125](https://github.com/runloopai/api-client-python/issues/125)) ([b1f126d](https://github.com/runloopai/api-client-python/commit/b1f126d5ff0492f1115f5d0d587291ff0cfa9cde))
* **api:** OpenAPI spec update via Stainless API ([#126](https://github.com/runloopai/api-client-python/issues/126)) ([db6ba44](https://github.com/runloopai/api-client-python/commit/db6ba44ed380eb5728db4b40654cf1be4c8d8775))
* **api:** OpenAPI spec update via Stainless API ([#127](https://github.com/runloopai/api-client-python/issues/127)) ([3940b9f](https://github.com/runloopai/api-client-python/commit/3940b9f88c25a518bbcb302b1f5a22ce7c2ba495))
* **api:** OpenAPI spec update via Stainless API ([#128](https://github.com/runloopai/api-client-python/issues/128)) ([ff9ade1](https://github.com/runloopai/api-client-python/commit/ff9ade1369c3407ab27ea17957f33ae2f4e1eb84))

## 0.1.0-alpha.15 (2024-08-23)

Full Changelog: [v0.1.0-alpha.14...v0.1.0-alpha.15](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.14...v0.1.0-alpha.15)

### Features

* **api:** manual updates ([#117](https://github.com/runloopai/api-client-python/issues/117)) ([5222c74](https://github.com/runloopai/api-client-python/commit/5222c7462dae22befa4cbfe000635660c0b72070))
* **api:** manual updates ([#118](https://github.com/runloopai/api-client-python/issues/118)) ([2801d62](https://github.com/runloopai/api-client-python/commit/2801d62df46e79a9054a4c32453b46436362aa2c))
* **api:** OpenAPI spec update via Stainless API ([#106](https://github.com/runloopai/api-client-python/issues/106)) ([977e845](https://github.com/runloopai/api-client-python/commit/977e845bb31245f85aa00e1c0bdd091ed81967df))
* **api:** OpenAPI spec update via Stainless API ([#110](https://github.com/runloopai/api-client-python/issues/110)) ([dc0bc88](https://github.com/runloopai/api-client-python/commit/dc0bc888d147dce2619d0e0f38897bd1df4372e6))
* **api:** OpenAPI spec update via Stainless API ([#111](https://github.com/runloopai/api-client-python/issues/111)) ([82a1581](https://github.com/runloopai/api-client-python/commit/82a158114880b0d416ae4e9660926151daf1a60f))
* **api:** OpenAPI spec update via Stainless API ([#112](https://github.com/runloopai/api-client-python/issues/112)) ([cfddae4](https://github.com/runloopai/api-client-python/commit/cfddae44be11039af98c8d6f570990351c552d9d))
* **api:** OpenAPI spec update via Stainless API ([#113](https://github.com/runloopai/api-client-python/issues/113)) ([23d90e8](https://github.com/runloopai/api-client-python/commit/23d90e8d22775abcaf90e44fa7b9dc112d6d36ad))
* **api:** OpenAPI spec update via Stainless API ([#114](https://github.com/runloopai/api-client-python/issues/114)) ([f754530](https://github.com/runloopai/api-client-python/commit/f7545300ecc975f555178729c987fa506d8c0dde))
* **api:** OpenAPI spec update via Stainless API ([#115](https://github.com/runloopai/api-client-python/issues/115)) ([b5200de](https://github.com/runloopai/api-client-python/commit/b5200dedec44c8785daf06cb1acfa3b6909d8361))
* **api:** OpenAPI spec update via Stainless API ([#120](https://github.com/runloopai/api-client-python/issues/120)) ([e432b64](https://github.com/runloopai/api-client-python/commit/e432b64ee28bf061878cba1bf76285d847cd3ce7))


### Chores

* **ci:** also run pydantic v1 tests ([#109](https://github.com/runloopai/api-client-python/issues/109)) ([23009f0](https://github.com/runloopai/api-client-python/commit/23009f032c59a5ab216c7602cabfe63253dd33b5))
* **client:** fix parsing union responses when non-json is returned ([#108](https://github.com/runloopai/api-client-python/issues/108)) ([9133e9b](https://github.com/runloopai/api-client-python/commit/9133e9b87be8d363742b08f2f829699657982a6e))

## 0.1.0-alpha.14 (2024-08-16)

Full Changelog: [v0.1.0-alpha.13...v0.1.0-alpha.14](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.13...v0.1.0-alpha.14)

### Features

* **api:** OpenAPI spec update via Stainless API ([#104](https://github.com/runloopai/api-client-python/issues/104)) ([ac4c9fa](https://github.com/runloopai/api-client-python/commit/ac4c9fa9d73c01a5cb6dd01955647cb823427fad))

## 0.1.0-alpha.13 (2024-08-16)

Full Changelog: [v0.1.0-alpha.12...v0.1.0-alpha.13](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.12...v0.1.0-alpha.13)

### Features

* **api:** OpenAPI spec update via Stainless API ([#100](https://github.com/runloopai/api-client-python/issues/100)) ([772cfa1](https://github.com/runloopai/api-client-python/commit/772cfa19fb0c666540b39613ca1fc4a22bdffe82))
* **api:** OpenAPI spec update via Stainless API ([#101](https://github.com/runloopai/api-client-python/issues/101)) ([a0841a4](https://github.com/runloopai/api-client-python/commit/a0841a410113bc784cca786a2774aea67c9f3a58))
* **api:** OpenAPI spec update via Stainless API ([#102](https://github.com/runloopai/api-client-python/issues/102)) ([158d661](https://github.com/runloopai/api-client-python/commit/158d661d90493597b1500b6ef4cfcfe6b7fa6d30))
* **api:** OpenAPI spec update via Stainless API ([#96](https://github.com/runloopai/api-client-python/issues/96)) ([fb6dd1d](https://github.com/runloopai/api-client-python/commit/fb6dd1d4c536f0c518c6399ec543ea92162782ff))
* **api:** OpenAPI spec update via Stainless API ([#98](https://github.com/runloopai/api-client-python/issues/98)) ([0d77cac](https://github.com/runloopai/api-client-python/commit/0d77cacb4b4c582826b9772a287cced25b1210bf))
* **api:** OpenAPI spec update via Stainless API ([#99](https://github.com/runloopai/api-client-python/issues/99)) ([081978b](https://github.com/runloopai/api-client-python/commit/081978b3867fe873b52ea475cbe6e69e50448e51))

## 0.1.0-alpha.12 (2024-08-15)

Full Changelog: [v0.1.0-alpha.11...v0.1.0-alpha.12](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.11...v0.1.0-alpha.12)

### Features

* **api:** OpenAPI spec update via Stainless API ([#83](https://github.com/runloopai/api-client-python/issues/83)) ([df99a13](https://github.com/runloopai/api-client-python/commit/df99a130b3dbbba6b122a65bc9c822b6d589ca26))
* **api:** OpenAPI spec update via Stainless API ([#88](https://github.com/runloopai/api-client-python/issues/88)) ([a8882d4](https://github.com/runloopai/api-client-python/commit/a8882d440edc71f2922e2fa2dff3d0f0b080eb35))
* **api:** OpenAPI spec update via Stainless API ([#89](https://github.com/runloopai/api-client-python/issues/89)) ([a8b5d6a](https://github.com/runloopai/api-client-python/commit/a8b5d6a94d38bc593b8ca48014dcba17c783d297))
* **api:** OpenAPI spec update via Stainless API ([#90](https://github.com/runloopai/api-client-python/issues/90)) ([dc4b13c](https://github.com/runloopai/api-client-python/commit/dc4b13cd4d4fa17f203626e88187f8784ecbac6f))
* **api:** OpenAPI spec update via Stainless API ([#93](https://github.com/runloopai/api-client-python/issues/93)) ([d6ba90f](https://github.com/runloopai/api-client-python/commit/d6ba90fa6af62f376578aa14a5b50e759fc30898))
* **api:** update via SDK Studio ([#91](https://github.com/runloopai/api-client-python/issues/91)) ([612ce32](https://github.com/runloopai/api-client-python/commit/612ce3279298c1158ce963471cd6d53b4a822718))


### Chores

* **ci:** bump prism mock server version ([#85](https://github.com/runloopai/api-client-python/issues/85)) ([ff2c8dd](https://github.com/runloopai/api-client-python/commit/ff2c8ddeaec8bfaa9ebd71886126f02ede9bb2db))
* **ci:** minor changes ([#84](https://github.com/runloopai/api-client-python/issues/84)) ([32f527f](https://github.com/runloopai/api-client-python/commit/32f527f1802bfc63c2156ad7eefd7773a007f501))
* **examples:** minor formatting changes ([#87](https://github.com/runloopai/api-client-python/issues/87)) ([64c9bd5](https://github.com/runloopai/api-client-python/commit/64c9bd5c499d56772028679aa974eac5e78c3b15))
* **internal:** codegen related update ([#92](https://github.com/runloopai/api-client-python/issues/92)) ([0c34d9a](https://github.com/runloopai/api-client-python/commit/0c34d9a7a296d0e0fd4626b6f9629ff737e61590))
* **internal:** ensure package is importable in lint cmd ([#86](https://github.com/runloopai/api-client-python/issues/86)) ([ecf2a95](https://github.com/runloopai/api-client-python/commit/ecf2a95f550db94d2d16ea3774bd9c9bea42b3a4))
* **internal:** remove deprecated ruff config ([#81](https://github.com/runloopai/api-client-python/issues/81)) ([2916f9f](https://github.com/runloopai/api-client-python/commit/2916f9fdc0b19758767e5c93875e14cc3bce4049))
* **internal:** use different 32bit detection method ([#94](https://github.com/runloopai/api-client-python/issues/94)) ([cf748e3](https://github.com/runloopai/api-client-python/commit/cf748e337f3e1f443be098c1b0e72e3c321815c6))

## 0.1.0-alpha.11 (2024-08-07)

Full Changelog: [v0.1.0-alpha.10...v0.1.0-alpha.11](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.10...v0.1.0-alpha.11)

### Features

* **api:** OpenAPI spec update via Stainless API ([#66](https://github.com/runloopai/api-client-python/issues/66)) ([291eddb](https://github.com/runloopai/api-client-python/commit/291eddbf05d2e12d882f8d53baac9617149a1e34))
* **api:** OpenAPI spec update via Stainless API ([#68](https://github.com/runloopai/api-client-python/issues/68)) ([91913d6](https://github.com/runloopai/api-client-python/commit/91913d6fc7582204fbfa37bf780ea287c0940e97))
* **api:** OpenAPI spec update via Stainless API ([#69](https://github.com/runloopai/api-client-python/issues/69)) ([f82c51c](https://github.com/runloopai/api-client-python/commit/f82c51cc8d5a5b8588d0b8e98cae7bcbf06d4f09))
* **api:** OpenAPI spec update via Stainless API ([#70](https://github.com/runloopai/api-client-python/issues/70)) ([b0ffcf0](https://github.com/runloopai/api-client-python/commit/b0ffcf0031ac84240728907ee722ed3e21de3735))
* **api:** OpenAPI spec update via Stainless API ([#75](https://github.com/runloopai/api-client-python/issues/75)) ([213734e](https://github.com/runloopai/api-client-python/commit/213734e474bce92394eea0aea69132d95850f3c8))
* **api:** OpenAPI spec update via Stainless API ([#76](https://github.com/runloopai/api-client-python/issues/76)) ([d6370bc](https://github.com/runloopai/api-client-python/commit/d6370bce09d23275d632e1b265f6207a189fedc7))
* **api:** OpenAPI spec update via Stainless API ([#79](https://github.com/runloopai/api-client-python/issues/79)) ([23d4705](https://github.com/runloopai/api-client-python/commit/23d470542689d3d227ddff7c11464f6a1849003b))
* **client:** add `retry_count` to raw response class ([#73](https://github.com/runloopai/api-client-python/issues/73)) ([e17fb03](https://github.com/runloopai/api-client-python/commit/e17fb0352e692b04df6f67d98a67182a13cd95ee))


### Chores

* **internal:** bump pyright ([#72](https://github.com/runloopai/api-client-python/issues/72)) ([3fcd1bf](https://github.com/runloopai/api-client-python/commit/3fcd1bf654826a81efea4f3b67fc85a124141d41))
* **internal:** bump ruff version ([#77](https://github.com/runloopai/api-client-python/issues/77)) ([240971d](https://github.com/runloopai/api-client-python/commit/240971d1eac9b67a3e85369b0617fc9821e048b3))
* **internal:** test updates ([#74](https://github.com/runloopai/api-client-python/issues/74)) ([cac724a](https://github.com/runloopai/api-client-python/commit/cac724a5db2acdecc40a9775dcde49b9f8f9a277))
* **internal:** update pydantic compat helper function ([#78](https://github.com/runloopai/api-client-python/issues/78)) ([3befea7](https://github.com/runloopai/api-client-python/commit/3befea7ec40892a6f6455d81eb87d8c4ab8a7629))
* **internal:** use `TypeAlias` marker for type assignments ([#71](https://github.com/runloopai/api-client-python/issues/71)) ([4de0849](https://github.com/runloopai/api-client-python/commit/4de08497452923cfa328aadfd6626286b3248d17))

## 0.1.0-alpha.10 (2024-08-02)

Full Changelog: [v0.1.0-alpha.9...v0.1.0-alpha.10](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.9...v0.1.0-alpha.10)

### Features

* **api:** update via SDK Studio ([#63](https://github.com/runloopai/api-client-python/issues/63)) ([d2aefd1](https://github.com/runloopai/api-client-python/commit/d2aefd19566d6a90121cfd6b4a188a538b496d98))

## 0.1.0-alpha.9 (2024-08-01)

Full Changelog: [v0.1.0-alpha.8...v0.1.0-alpha.9](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.8...v0.1.0-alpha.9)

### Chores

* update SDK settings ([#60](https://github.com/runloopai/api-client-python/issues/60)) ([0ccfd28](https://github.com/runloopai/api-client-python/commit/0ccfd28645206b0dedc2dac42e17fcaec14c293e))

## 0.1.0-alpha.8 (2024-08-01)

Full Changelog: [v0.1.0-alpha.7...v0.1.0-alpha.8](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.7...v0.1.0-alpha.8)

### Features

* **api:** OpenAPI spec update via Stainless API ([#52](https://github.com/runloopai/api-client-python/issues/52)) ([f7b6f31](https://github.com/runloopai/api-client-python/commit/f7b6f31ac8c9f75f821497eeb4840ded40a156af))
* **api:** OpenAPI spec update via Stainless API ([#54](https://github.com/runloopai/api-client-python/issues/54)) ([008ea96](https://github.com/runloopai/api-client-python/commit/008ea96ea340405d5660aef5024127764380e149))
* **api:** OpenAPI spec update via Stainless API ([#55](https://github.com/runloopai/api-client-python/issues/55)) ([daae357](https://github.com/runloopai/api-client-python/commit/daae357f65e078a1e156ddeeb8cf908339caa2e4))
* **api:** OpenAPI spec update via Stainless API ([#56](https://github.com/runloopai/api-client-python/issues/56)) ([ba93ed6](https://github.com/runloopai/api-client-python/commit/ba93ed64442f52fd482f499183eb6a0d405de4be))
* **api:** OpenAPI spec update via Stainless API ([#57](https://github.com/runloopai/api-client-python/issues/57)) ([12018b3](https://github.com/runloopai/api-client-python/commit/12018b32ac22d69ebc84e01e00c8b48a08d20224))
* **api:** update via SDK Studio ([#58](https://github.com/runloopai/api-client-python/issues/58)) ([86cf18f](https://github.com/runloopai/api-client-python/commit/86cf18f654a62dd48e2d6d36d6d5f2e57d362470))

## 0.1.0-alpha.7 (2024-07-30)

Full Changelog: [v0.1.0-alpha.6...v0.1.0-alpha.7](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.6...v0.1.0-alpha.7)

### Features

* **api:** OpenAPI spec update via Stainless API ([#41](https://github.com/runloopai/api-client-python/issues/41)) ([d4da50f](https://github.com/runloopai/api-client-python/commit/d4da50fc963abf097b5d214df1cc3ee641281ab3))
* **api:** OpenAPI spec update via Stainless API ([#43](https://github.com/runloopai/api-client-python/issues/43)) ([2eed5ae](https://github.com/runloopai/api-client-python/commit/2eed5aed9091a2040efe730cb63baa8b284f1c4d))
* **api:** OpenAPI spec update via Stainless API ([#44](https://github.com/runloopai/api-client-python/issues/44)) ([d936662](https://github.com/runloopai/api-client-python/commit/d936662a5aea53a50f8ccf7e7d29c3634a8567d7))
* **api:** OpenAPI spec update via Stainless API ([#46](https://github.com/runloopai/api-client-python/issues/46)) ([cd62f94](https://github.com/runloopai/api-client-python/commit/cd62f949150028cdd481966722d26f1ea3333cd2))
* **api:** OpenAPI spec update via Stainless API ([#47](https://github.com/runloopai/api-client-python/issues/47)) ([218b9b0](https://github.com/runloopai/api-client-python/commit/218b9b0a1af247c96d7ca5299cf5c855bc4e3dfd))
* **api:** OpenAPI spec update via Stainless API ([#48](https://github.com/runloopai/api-client-python/issues/48)) ([b866f26](https://github.com/runloopai/api-client-python/commit/b866f2684b69ba1f5b3ed4f360c8de03aefa63e4))
* **api:** OpenAPI spec update via Stainless API ([#49](https://github.com/runloopai/api-client-python/issues/49)) ([3a39028](https://github.com/runloopai/api-client-python/commit/3a390287c870129265fc9f2cee6c6042430ea61f))
* **api:** OpenAPI spec update via Stainless API ([#50](https://github.com/runloopai/api-client-python/issues/50)) ([c6d26f4](https://github.com/runloopai/api-client-python/commit/c6d26f407dffb8b65342476e129e11a2caa481db))


### Chores

* **internal:** add type construction helper ([#45](https://github.com/runloopai/api-client-python/issues/45)) ([8b05828](https://github.com/runloopai/api-client-python/commit/8b058280802b5ce7987065d17806632de4a80d32))

## 0.1.0-alpha.6 (2024-07-25)

Full Changelog: [v0.1.0-alpha.5...v0.1.0-alpha.6](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.5...v0.1.0-alpha.6)

### Features

* **api:** codegen changes ([4dc6179](https://github.com/runloopai/api-client-python/commit/4dc617943e2830fce6aa785c2d22205d486f0614))
* **api:** OpenAPI spec update via Stainless API ([#24](https://github.com/runloopai/api-client-python/issues/24)) ([d89833e](https://github.com/runloopai/api-client-python/commit/d89833e862433a467101b70d514287587aa0557b))
* **api:** OpenAPI spec update via Stainless API ([#26](https://github.com/runloopai/api-client-python/issues/26)) ([0418fb3](https://github.com/runloopai/api-client-python/commit/0418fb3400c9566af460c8890f807a3fc77ffbe1))
* **api:** OpenAPI spec update via Stainless API ([#28](https://github.com/runloopai/api-client-python/issues/28)) ([4b90fc2](https://github.com/runloopai/api-client-python/commit/4b90fc2fb979b15a64cddd05d49a492c6548b2e7))
* **api:** OpenAPI spec update via Stainless API ([#29](https://github.com/runloopai/api-client-python/issues/29)) ([351c37b](https://github.com/runloopai/api-client-python/commit/351c37bc328f53f26c094ae440a31b10b300559e))
* **api:** OpenAPI spec update via Stainless API ([#30](https://github.com/runloopai/api-client-python/issues/30)) ([877f6a4](https://github.com/runloopai/api-client-python/commit/877f6a48a13bb4cc4e2810fd155b2356cd21e709))
* **api:** OpenAPI spec update via Stainless API ([#31](https://github.com/runloopai/api-client-python/issues/31)) ([dd37c08](https://github.com/runloopai/api-client-python/commit/dd37c0807fe91ae9a6d0d3c18a9dad11f53ad83a))
* **api:** OpenAPI spec update via Stainless API ([#32](https://github.com/runloopai/api-client-python/issues/32)) ([8572bf8](https://github.com/runloopai/api-client-python/commit/8572bf848e258f802e2fdc699e227c6db33d04ba))
* **api:** OpenAPI spec update via Stainless API ([#33](https://github.com/runloopai/api-client-python/issues/33)) ([aff00c2](https://github.com/runloopai/api-client-python/commit/aff00c248594876293eff6269dd2397e3aa313c4))
* **api:** OpenAPI spec update via Stainless API ([#34](https://github.com/runloopai/api-client-python/issues/34)) ([706ca4f](https://github.com/runloopai/api-client-python/commit/706ca4f535ee0ea572aaea7a2c138a09c5a371fb))
* **api:** OpenAPI spec update via Stainless API ([#37](https://github.com/runloopai/api-client-python/issues/37)) ([c30452b](https://github.com/runloopai/api-client-python/commit/c30452b3dae499d892384be9b76fe36255302b1c))
* **api:** OpenAPI spec update via Stainless API ([#38](https://github.com/runloopai/api-client-python/issues/38)) ([399782f](https://github.com/runloopai/api-client-python/commit/399782fa56fd8744f5836913dd408eed49f80007))
* **api:** OpenAPI spec update via Stainless API ([#39](https://github.com/runloopai/api-client-python/issues/39)) ([76ed1ec](https://github.com/runloopai/api-client-python/commit/76ed1ec92b5eee1ceeebadb7a01af34e5b00c2c1))


### Chores

* **internal:** refactor release doctor script ([#35](https://github.com/runloopai/api-client-python/issues/35)) ([3189cad](https://github.com/runloopai/api-client-python/commit/3189cad0f77f1fdd67c0af290dc87c0f22eb5690))
* **tests:** update prism version ([#36](https://github.com/runloopai/api-client-python/issues/36)) ([8ad7914](https://github.com/runloopai/api-client-python/commit/8ad7914681564cb307174e0c33456c566603319b))

## 0.1.0-alpha.5 (2024-07-03)

Full Changelog: [v0.1.0-alpha.4...v0.1.0-alpha.5](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.4...v0.1.0-alpha.5)

### Features

* **api:** OpenAPI spec update via Stainless API ([#19](https://github.com/runloopai/api-client-python/issues/19)) ([9def751](https://github.com/runloopai/api-client-python/commit/9def7518972cdb0c0a03728408d8e10f79090ba5))
* **api:** OpenAPI spec update via Stainless API ([#20](https://github.com/runloopai/api-client-python/issues/20)) ([a0bf266](https://github.com/runloopai/api-client-python/commit/a0bf2667f1831d91cc1375328f355dc561b98a37))
* **api:** OpenAPI spec update via Stainless API ([#21](https://github.com/runloopai/api-client-python/issues/21)) ([9e9f3c2](https://github.com/runloopai/api-client-python/commit/9e9f3c2150928658c49e5c18569411766be60bbe))
* **api:** OpenAPI spec update via Stainless API ([#22](https://github.com/runloopai/api-client-python/issues/22)) ([5bf8bc0](https://github.com/runloopai/api-client-python/commit/5bf8bc0c5030ed78d04b7a513a0d167aa3e9acf8))

## 0.1.0-alpha.4 (2024-06-26)

Full Changelog: [v0.1.0-alpha.3...v0.1.0-alpha.4](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.3...v0.1.0-alpha.4)

### Features

* **api:** update via SDK Studio ([#15](https://github.com/runloopai/api-client-python/issues/15)) ([4813de5](https://github.com/runloopai/api-client-python/commit/4813de5f1d73df3e39a4efff76d7d80202e65162))

## 0.1.0-alpha.3 (2024-06-26)

Full Changelog: [v0.1.0-alpha.2...v0.1.0-alpha.3](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.2...v0.1.0-alpha.3)

### Features

* **api:** update via SDK Studio ([#12](https://github.com/runloopai/api-client-python/issues/12)) ([a86d706](https://github.com/runloopai/api-client-python/commit/a86d7069570b8d0360d3e67b90ee1fed736ec1df))

## 0.1.0-alpha.2 (2024-06-25)

Full Changelog: [v0.1.0-alpha.1...v0.1.0-alpha.2](https://github.com/runloopai/api-client-python/compare/v0.1.0-alpha.1...v0.1.0-alpha.2)

### Features

* **api:** update via SDK Studio ([#9](https://github.com/runloopai/api-client-python/issues/9)) ([9a53399](https://github.com/runloopai/api-client-python/commit/9a533998e9f44bf77fc0697c32af441ab1ec49fc))

## 0.1.0-alpha.1 (2024-06-25)

Full Changelog: [v0.0.1-alpha.0...v0.1.0-alpha.1](https://github.com/runloopai/api-client-python/compare/v0.0.1-alpha.0...v0.1.0-alpha.1)

### Features

* **api:** OpenAPI spec update via Stainless API ([17991ec](https://github.com/runloopai/api-client-python/commit/17991ec2bd449f7ffef39a9da4b274f82c61c364))
* **api:** OpenAPI spec update via Stainless API ([a624924](https://github.com/runloopai/api-client-python/commit/a62492427ea762b1fa8e6e438ba489ff08b798e5))
* **api:** OpenAPI spec update via Stainless API ([#4](https://github.com/runloopai/api-client-python/issues/4)) ([134f28f](https://github.com/runloopai/api-client-python/commit/134f28ff63f25f18d3a4b7e2300b768ffa4c7590))
* **api:** update via SDK Studio ([88939b3](https://github.com/runloopai/api-client-python/commit/88939b3e46af521bc43a7b25e66ddb5a553a2af6))
* **api:** update via SDK Studio ([e2cca37](https://github.com/runloopai/api-client-python/commit/e2cca3796d1a2b128abb6f93b8e444f0dd4da501))


### Chores

* go live ([#2](https://github.com/runloopai/api-client-python/issues/2)) ([3ae4996](https://github.com/runloopai/api-client-python/commit/3ae4996b2474aabb19a98cf38b834ca3e91d7c2b))
* go live ([#5](https://github.com/runloopai/api-client-python/issues/5)) ([626be20](https://github.com/runloopai/api-client-python/commit/626be201c2ed40ac34f2b5869f6c17c431ee543b))
* update SDK settings ([ac8358a](https://github.com/runloopai/api-client-python/commit/ac8358ae8d3ac7ba5bab2082384ae5029c50fcc8))
* update SDK settings ([#3](https://github.com/runloopai/api-client-python/issues/3)) ([ef88178](https://github.com/runloopai/api-client-python/commit/ef88178299ae3988bc3d1e813c462d609312f69a))
* update SDK settings ([#6](https://github.com/runloopai/api-client-python/issues/6)) ([82a6f56](https://github.com/runloopai/api-client-python/commit/82a6f56061cd0ebfa88ed3ec71d044a0fb131f0a))
* update SDK settings ([#7](https://github.com/runloopai/api-client-python/issues/7)) ([aa9d69b](https://github.com/runloopai/api-client-python/commit/aa9d69b15a011dfa8381ec08327c88e5c2a1ab8d))
