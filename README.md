# CodeShield-SDP: Technical Debt and Security Scanner

[![Python](https://img.shields.io/badge/Python-100%25-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-%23FF6B35.svg?&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![License: GPL-3.0](https://img.shields.io/badge/License-GPL3-yellow.svg)](https://www.gnu.org/licenses/gpl-3.0)

**CodeShield-SDP** is an AI-powered web application built with Streamlit that scans Python code for technical debt metrics (e.g., cyclomatic complexity via AST parsing) and security vulnerabilities. Upload code, visualize graphs of nodes/edges, and get actionable insights.[page:1]

## ✨ Click for Details

### <details>

<summary>🛠️ Key Features</summary>

- **Code Analysis**: Parses Python AST to calculate nodes, edges, and complexity scores for technical debt.
- **Security Scanning**: Detects common vulnerabilities like hardcoded secrets or unsafe practices.
- **Interactive Dashboard**: Streamlit UI with graphs and Supabase-backed storage for results.
- **Deployment Ready**: Includes `app.py`, requirements, and utils for easy local or cloud setup.

</details>

### <details>

<summary>📁 Tech Stack & Structure</summary>

- **Frontend/Backend**: Streamlit (`app.py`, `pages/`).
- **Utils**: Code parsing (`utils/` with AST module), Supabase client integration.
- **Key Files**:
  | File | Purpose |
  |------|---------|
  | `app.py` | Main Streamlit app |
  | `testing.py` | Testing scripts |
  | `requirements.txt` | Dependencies (e.g., streamlit, supabase) |
  | `utils/` | Analysis logic |

</details>

### <details>

<summary>🚀 Quick Start</summary>

1. Clone: `git clone https://github.com/afsheenkhan-24/codeshield-sdp.git`
2. Install: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
4. Open browser to `localhost:8501` and upload Python code for scanning.

Set Supabase env vars for full features.

</details>

### <details>

<summary>📈 Recent Updates</summary>

- Switched to AST module for accurate node/edge calculation.
- Supabase integration for persistent data.
- CSS refinements and testing enhancements.

See [commits](https://github.com/afsheenkhan-24/codeshield-sdp/commits/main/) for full history.

</details>

## 🤝 Contributing

Fork, PRs welcome! Focus on adding more vuln detectors or ML-based debt scoring.

## 📄 License

GPL-3.0 [LICENSE](LICENSE)

**Stars and feedback appreciated! ⭐** [page:1]
