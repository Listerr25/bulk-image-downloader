import streamlit as st
import os
import shutil
import zipfile
import io

# Import the image downloader
from simple_image_download import simple_image_download as simp

st.title("Bulk Image Downloader")

st.markdown(
    """
    Enter comma-separated keywords, the number of images per keyword, and a label to download images.
    Once the images are downloaded, they will be zipped and you can download the zip file.
    """
)

# User inputs
keywords = st.text_input("Enter the keywords (comma-separated):")
count = st.number_input("Enter the number of images per keyword:", value=5, min_value=1, step=1)
label = st.text_input("Enter the label:")

if st.button("Download Images"):
    if not keywords:
        st.error("Please enter at least one keyword.")
    else:
        # Remove any existing folder to start fresh
        if os.path.exists("simple_images"):
            shutil.rmtree("simple_images")
        
        # Split and clean the keywords
        lst = [kw.strip() for kw in keywords.split(",") if kw.strip()]
        response = simp.simple_image_download
        
        st.info("Starting image download...")
        # Download images for each keyword
        for keyword in lst:
            # The library creates a subfolder named: simple_images/<keyword>_<label>
            folder_name = f"{keyword}_{label}"
            response().download(folder_name, count)
            st.write(f"Downloaded images for **{folder_name}**.")
        
        st.info("Zipping downloaded images...")
        # Create a zip file from the simple_images folder
        zip_filename = "simple_images.zip"
        with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk("simple_images"):
                for file in files:
                    filepath = os.path.join(root, file)
                    # arcname ensures the folder structure inside the zip remains relative
                    arcname = os.path.relpath(filepath, os.path.join("simple_images", ".."))
                    zipf.write(filepath, arcname)
        
        # Read the zip file into a bytes buffer for download
        with open(zip_filename, "rb") as f:
            zip_bytes = f.read()
        
        st.success("Zipping complete!")
        
        st.download_button(
            label="Download ZIP",
            data=zip_bytes,
            file_name=zip_filename,
            mime="application/zip",
        )
        
        # OPTIONAL: Cleanup the created files and folders
        if os.path.exists("simple_images"):
            shutil.rmtree("simple_images")
        if os.path.exists(zip_filename):
            os.remove(zip_filename)
        st.info("Temporary files have been removed.")
