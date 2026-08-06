BOOLNEXA v1.1.0 SEO INSTALLATION

1. Extract these files into:
   D:\Projects\BoolNexa

2. Open Command Prompt:

   cd /d D:\Projects\BoolNexa
   .venv\Scripts\activate
   python install_v1_1_0_seo.py

3. Validate:

   python -m compileall digital_logic_lab
   reflex run

4. Open the local site and confirm it loads normally.

5. Commit after testing:

   git status
   git add digital_logic_lab\seo.py digital_logic_lab\digital_logic_lab.py
   git commit -m "Add advanced SEO metadata and structured data"
   git push origin main

6. Create the release backup:

   git archive --format=zip --output=D:\Projects\Backups\BoolNexa\BoolNexa_v1.1.0_Source.zip HEAD

The installer creates:
   digital_logic_lab\digital_logic_lab.py.v1.0.2.bak

That backup is intentionally not staged in the commands above.
Delete it after successful testing or keep it outside the repository.
