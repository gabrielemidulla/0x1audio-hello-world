# Building this app

This folder is the whole app.

- `app.py` is the work. A function decorated with `@ox.screen` becomes a screen.
- `app.json` names the app.
- `ui/App.tsx` is optional. `ox eject` writes it when the screen needs a custom layout.
- `ui/components/` holds a React component the kit does not have.
- `AGENTS.md` is the spec. Read this and stop.

Controls: `Files`, `Choice`, `Text`, `Number`, `Toggle`, `Slider`.
Yield `ox.progress(fraction, label)` to report progress.
Yield `ox.sound`, `ox.midi`, or `ox.file` to add to the Library.
`ox.test(hello, name="world")` runs the function without the desktop.
`print` goes to the log. The desktop owns the protocol stream.
Permissions come from the controls and the exports. A custom page lists them in `app.json`: `files`, `library`, `network`, `data`.
