
from pathlib import Path
from datetime import datetime
import streamlit as st

from integrity import scan_files, load_baseline, save_baseline

BASE_DIR = Path(__file__).resolve().parent
FOLDER = BASE_DIR / "monitored_files"
BASELINE = BASE_DIR / "baseline.json"
LOG_FILE = BASE_DIR / "logs.txt"

FOLDER.mkdir(exist_ok=True)

st.set_page_config(
    page_title="FIM Security Dashboard",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ File Integrity Monitoring System")
st.caption("Monitor file changes using SHA-256 hashing")

st.sidebar.header("Controls")

if st.sidebar.button("Create / Update Baseline"):
    files = scan_files("monitored_files")
    save_baseline(files, str(BASELINE))
    st.sidebar.success("Baseline created successfully!")

if st.sidebar.button("Scan Files"):
    if not BASELINE.exists():
        st.sidebar.error("Create a baseline first!")
    else:
        old_files = load_baseline(str(BASELINE))
        new_files = scan_files("monitored_files")

        added = [p for p in new_files if p not in old_files]
        modified = [
            p for p in new_files
            if p in old_files and new_files[p] != old_files[p]
        ]
        deleted = [p for p in old_files if p not in new_files]

        results = {
            "New Files": added,
            "Modified Files": modified,
            "Deleted Files": deleted
        }

        st.session_state["results"] = results

        with open(LOG_FILE, "a", encoding="utf-8") as log:
            for category, paths in results.items():
                for path in paths:
                    message = f"{category.upper()}: {path}"
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    log.write(f"[{timestamp}] {message}\n")

        st.sidebar.success("Scan completed!")

st.subheader("Security Overview")

if "results" not in st.session_state:
    st.session_state["results"] = {
        "New Files": [],
        "Modified Files": [],
        "Deleted Files": []
    }

results = st.session_state["results"]

current_files = scan_files("monitored_files")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Files", len(current_files))
col2.metric("New Files", len(results["New Files"]))
col3.metric("Modified Files", len(results["Modified Files"]))
col4.metric("Deleted Files", len(results["Deleted Files"]))

st.divider()

for category, paths in results.items():
    st.subheader(category)

    if paths:
        st.write(paths)
    else:
        st.success("No changes detected.")

st.divider()

st.subheader("Event Logs")

if LOG_FILE.exists():
    log_text = LOG_FILE.read_text(encoding="utf-8")
    st.text_area("Activity History", log_text, height=200)
else:
    st.info("No activity logs available yet.")

st.caption("Educational project | Python + Streamlit + SHA-256")
