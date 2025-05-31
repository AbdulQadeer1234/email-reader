import streamlit as st
import os
from utils.email_utils import fetch_emails
from utils.export_utils import export_to_file, zip_attachments
from utils.creds_utils import save_credentials, load_credentials

st.set_page_config(page_title="Email Reader", layout="wide")
st.title("📬 Email Reader")

# Initialize session state
if "data_fetched" not in st.session_state:
    st.session_state.data_fetched = False

# Load saved creds if available
saved = load_credentials()

# ---- Login Form ----
with st.form("login_form"):
    st.subheader("Login")

    email_user = st.text_input("Email", value=saved.get("email", ""))

    email_pass = st.text_input(
        "App Password",
        type="password",
        value=saved.get("password", ""),
        help=(
            "Go to myaccount.google.com and navigate to the Security section."
            "Under “Signing in to Google,” enable 2-Step Verification. Once 2FA is enabled, return to the Security page and open App passwords"
            "There you'll see your existing app passwords, or you can create a new one by giving it an app name. "
            "Use the generated 16-character password here."
        )
    )

    remember_me = st.checkbox("Remember me")
    mail_filter = st.radio("Fetch:", ["Unread Emails", "All Emails"])
    file_format = st.selectbox("Export Format", ["csv", "xlsx"])
    submitted = st.form_submit_button("Fetch Emails")

# ---- On Submit ----
if submitted:
    if not email_user or not email_pass:
        st.error("Please enter valid email and password.")
    else:
        with st.spinner("📨 Fetching emails..."):
            data, attachments = fetch_emails(
                email_user,
                email_pass,
                unread_only=(mail_filter == "Unread Emails")
            )

        if data:
            if remember_me:
                save_credentials(email_user, email_pass)

            st.session_state["email_data"] = data
            st.session_state["attachments"] = attachments
            st.session_state["file_format"] = file_format
            st.session_state["exported_file"] = export_to_file(data, file_format)
            st.session_state["zip_path"] = zip_attachments(attachments)
            st.session_state["data_fetched"] = True
        else:
            st.warning("No emails found with the selected filter.")
            st.session_state["data_fetched"] = False

# ---- Email Preview and Downloads ----
if st.session_state.get("data_fetched"):
    data = st.session_state["email_data"]
    file_path = st.session_state["exported_file"]
    zip_path = st.session_state["zip_path"]
    attachments = st.session_state["attachments"]

    st.success(f"✅ Fetched {len(data)} emails.")
    st.dataframe(data)

    col1, col2 = st.columns(2)

    with col1:
        with open(file_path, "rb") as f:
            st.download_button(
                "⬇️ Download Email Data",
                f,
                file_name=os.path.basename(file_path),
                mime="text/csv" if file_path.endswith(".csv") else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    with col2:
        if attachments:
            with open(zip_path, "rb") as f:
                st.download_button(
                    "⬇️ Download Attachments ZIP",
                    f,
                    file_name="attachments.zip",
                    mime="application/zip"
                )
        else:
            st.info("No attachments found.")

# ---- Clear Saved Credentials Option ----
if os.path.exists("saved_creds.json") and os.path.exists("key.key"):
    if st.button("🔒 Clear Saved Credentials"):
        os.remove("saved_creds.json")
        os.remove("key.key")
        st.success("Credentials cleared. Please reload the page.")
