BoolNexa v1.1.0 — Advanced SEO Release
=======================================

FILES INCLUDED

digital_logic_lab\digital_logic_lab.py
    Complete replacement based on your uploaded local file.

digital_logic_lab\seo.py
    Central SEO constants, metadata, canonical URL, social cards,
    and SoftwareApplication JSON-LD structured data.

assets\og-image.png
    Social sharing image used by Open Graph and Twitter/X cards.

INSTALLATION

1. Close the running Reflex development server.

2. Back up the current files:

   cd /d D:\Projects\BoolNexa
   copy digital_logic_lab\digital_logic_lab.py digital_logic_lab\digital_logic_lab.py.v1.0.2.bak

3. Extract this ZIP directly into:

   D:\Projects\BoolNexa

4. Choose Replace when Windows asks about digital_logic_lab.py.

5. Validate:

   cd /d D:\Projects\BoolNexa
   .venv\Scripts\activate
   python -m compileall digital_logic_lab
   reflex run

6. Open the local site and verify that the application loads and operates normally.

GIT COMMANDS AFTER SUCCESSFUL TESTING

   git status
   git add digital_logic_lab\digital_logic_lab.py digital_logic_lab\seo.py assets\og-image.png
   git commit -m "Release BoolNexa v1.1.0 advanced SEO"
   git push origin main

SOURCE BACKUP

   git archive --format=zip --output=D:\Projects\Backups\BoolNexa\BoolNexa_v1.1.0_Source.zip HEAD

CLEANUP

The old root-level files below are no longer required after successful testing:

   install_v1_1_0_seo.py
   install_v1_1_0_seo_fixed.py
   seo.py
   README_INSTALL.txt
   README_FIXED_INSTALL.txt

Do not delete them until the replacement release has passed validation.
