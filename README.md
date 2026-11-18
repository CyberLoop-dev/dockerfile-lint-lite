<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:f97316&height=170&section=header&text=Dockerfile%20Lint%20Lite&fontColor=ffffff&fontSize=38&animation=fadeIn" width="100%" alt="Dockerfile Lint Lite banner"/>
<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=18&duration=2800&pause=900&color=F97316&center=true&vCenter=true&width=650&lines=Read-only+Dockerfile+checks;Spot+common+configuration+risks;No+daemon+or+network+needed" alt="Typing introduction"/>
<p>A small, read-only checklist for common Dockerfile mistakes.</p>
<p><img src="https://img.shields.io/github/license/CyberLoop-dev/dockerfile-lint-lite?style=for-the-badge" alt="License"/> <img src="https://img.shields.io/github/languages/top/CyberLoop-dev/dockerfile-lint-lite?style=for-the-badge" alt="Language"/> <img src="https://img.shields.io/github/stars/CyberLoop-dev/dockerfile-lint-lite?style=for-the-badge" alt="Stars"/> <img src="https://img.shields.io/github/last-commit/CyberLoop-dev/dockerfile-lint-lite?style=for-the-badge" alt="Last commit"/></p>
<img src="assets/icon.svg" width="112" alt="Project icon"/>
</div>

## ✨ Overview
Dockerfile Lint Lite statically inspects a Dockerfile and reports a handful of explainable configuration hints. It does not build images, run containers, or contact a registry.

## 🚀 Features
- ✨ Warn about floating `:latest` or untagged base images
- ✨ Flag the use of ADD where COPY is usually clearer
- ✨ Check for a non-root USER instruction
- ✨ Detect suspicious hard-coded secret assignments in ARG and ENV
- ✨ Print line numbers and support CI-friendly strict mode

## 🎬 Demo
Run `python main.py Dockerfile` to see findings grouped by line and severity.

## ⚡ Quick Start
```bash
python main.py Dockerfile
python main.py Dockerfile --strict
```

## 🧰 Tech Stack
Python 3.10+ and the standard library only. Static analysis; no Docker daemon required.

## 🗂️ Folder Structure
```text
.
├── main.py
├── requirements.txt
├── tests/test_main.py
├── assets/icon.svg
├── .gitignore
└── LICENSE
```

## 🧭 Roadmap
- [ ] Add configurable rule levels
- [ ] Support stdin input
- [ ] Export SARIF-compatible findings

## 🤝 Contributing
Issues and focused pull requests are welcome. Add a test for each new rule and keep the checker read-only.

## 📄 License
Released under the [MIT License](LICENSE).

<div align="center"><img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f172a,100:f97316&height=100&section=footer" width="100%" alt="Animated wave footer"/></div>
