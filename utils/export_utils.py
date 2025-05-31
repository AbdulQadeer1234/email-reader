# import pandas as pd
# import zipfile
# import os

# def export_to_file(data, format):
#     df = pd.DataFrame(data)
#     filename = f"email_export.{format}"
#     filepath = os.path.join("downloads", filename)
#     if format == "csv":
#         df.to_csv(filepath, index=False)
#     elif format == "xlsx":
#         df.to_excel(filepath, index=False)
#     return filepath

# def zip_attachments(attachments):
#     zip_path = os.path.join("downloads", "attachments.zip")
#     with zipfile.ZipFile(zip_path, 'w') as zipf:
#         for file in attachments:
#             zipf.write(file, arcname=os.path.basename(file))
#     return zip_path
import pandas as pd
import zipfile
import os

DOWNLOADS_DIR = "downloads"

# Ensure the downloads directory exists
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def export_to_file(data, format):
    df = pd.DataFrame(data)
    filename = f"email_export.{format}"
    filepath = os.path.join(DOWNLOADS_DIR, filename)
    if format == "csv":
        df.to_csv(filepath, index=False)
    elif format == "xlsx":
        df.to_excel(filepath, index=False)
    return filepath

def zip_attachments(attachments):
    zip_path = os.path.join(DOWNLOADS_DIR, "attachments.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for file in attachments:
            zipf.write(file, arcname=os.path.basename(file))
    return zip_path
