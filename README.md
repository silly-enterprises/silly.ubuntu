# Silly Ubuntu Packages 🍥🐧

Welcome to **silly.ubuntu**, the official base config package repo of **Silly Enterprises™**.

This project provides `.deb` packages to customize Ubuntu systems into their silliest form possible — with fun tools, helpful defaults, and a dash of digital chaos.

---

## 🎯 Project Structure

```
silly.ubuntu/
├── packages/                # All individual .deb packages live here
│   ├── silly-base-config/   # Default configs, MOTD, aliases, and the 'silly' command
│   ├── silly-small-demo/    # A tiny demo package (e.g., figlet banner)
│   ├── silly-extra-silly/   # The silly one’s hand-picked extras (cowsay, fortune, moofortune)
│   └── silly-full/          # A metapackage that installs base + demo
├── scripts/                 # Local dev build scripts
│   └── build-all.sh         # Builds all .deb packages into apt/pool/
├── .github/workflows/       # CI and publishing logic
└── README.md                # You are here
```

---

## 📦 Package Philosophy

We organize our configs into small, self-contained `.deb` packages so you can:

- 🧩 Install only what you need
- 🔁 Mix and match across systems
- 🧼 Keep updates clean and predictable

Each package follows Debian best practices (permissions, rules files, etc.).

### Example Packages:

| Package             | Purpose                                           |
|---------------------|---------------------------------------------------|
| `silly-base-config` | Custom login banner, bashrc, the `silly` CLI tool |
| `silly-extra-silly` | Fortune + cowsay + `moofortune` wrapper 🐮        |
| `silly-small-demo`  | A figlet-style welcome banner                     |
| `silly-full`        | Meta-package that pulls in base + demo            |

---

## 🛠 GitHub Actions + APT Repo

Our GitHub Actions build all packages on push, and publish them to an APT-compatible structure under `apt/`.

Want to install them?

```bash
echo "deb [trusted=yes] https://deb.silly.enterprises stable main" | sudo tee /etc/apt/sources.list.d/silly.list
sudo apt update
sudo apt install silly-full
```

---

## 🧠 Related Repos in the Silly Ecosystem

| Repo                                                                  | Description                                                         |
|-----------------------------------------------------------------------|---------------------------------------------------------------------|
| [`silly.install`](https://github.com/silly-enterprises/silly.install) | The bootstrapper script (used via `curl install.silly.enterprises`) |
| [`silly.static`](https://github.com/silly-enterprises/silly.static)   | GitHub Pages for hosting our public APT repo + docs                 |
| [`silly.arch`](https://github.com/silly-enterprises/silly.arch)       | (planned) Arch version of these configs 🧪                          |

---

## 🧃 Want to Contribute?

Fork this repo, add your own package under `packages/`, and submit a PR! Each package needs:

- A `debian/` folder (with `control`, `rules`, etc.)
- Files in correct tree layout (`etc/`, `usr/`, etc.)

Need help? Ask one of the gremlins in `/usr/share/silly-enterprises/hooks.d/` 🐒

---

**Think big. Be silly.™**