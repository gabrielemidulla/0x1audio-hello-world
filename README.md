# Hello

The 0x1audio app template. The page is Vite and React. The worker is Python.

Copy this repository to start another app. The desktop opens `dist/index.html`, which is what `app.json` points at, so build the page before you publish.

```sh
pnpm install
pnpm dev
pnpm build
```

The page uses `@0x1audio/design-system` and `host` from `@0x1audio/sdk/page`. Those packages are linked from the sibling `0x1audio-cloud` and `0x1audio-sdk-ts` checkouts.
