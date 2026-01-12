Static Site Generator – Markdown to HTML
A small static site generator written in Python that turns Markdown content into a complete HTML website. You write pages in Markdown, run the generator, and it produces a fully static site ready to deploy anywhere (GitHub Pages, Netlify, etc.).

Features
Markdown → HTML
Converts .md files into HTML pages.

HTML Templates
Wraps content in a shared template (header, footer, navigation).

Directory-Based Routing
Uses your content/ folder structure to create clean URLs in public/.

Static Assets
Copies things like CSS, images, and JS into the output so they’re ready to serve.

Fully Static Output
The generated site is just HTML/CSS/JS. No backend needed.

How It Works (Overview)
Scans the content/ directory for .md files.
Reads each Markdown file and converts it to HTML.
Injects that HTML into an HTML template (e.g. templates/base.html).
Decides an output path based on the original file’s location.
Writes complete HTML files into public/.
Copies everything from static/ into public/ so assets are available.
Requirements
Python 3.10+ (or your actual minimum version)
This project uses only the Python standard library. No extra dependencies required.

Installation
Clone the repository and move into it:

git clone https://github.com/BorascuDan/static_site_generator.git
cd static_site_generator

Running the Generator Locally
From the project root, simply run the ./main.sh script(for local testing):

This will:

Read Markdown from content/
Apply your templates
Write the generated site into the docs/ directory
Previewing the Site
Option 1: Open the file directly
After running the generator, open:

docs/index.html

in your browser.

Option 2: Run a simple local server (recommended)
From the project root:

cd public
python3 -m http.server 8000

Then visit:

http://localhost:8000

Customizing the Site
Content – Edit or add .md files in content/.
Layout – Modify templates/base.html (or other templates) for structure/navigation.
Styling – Change static/styles.css to completely re-theme the site.
New sections – Create new folders under content/ (for example: blog/, projects/) and rerun python3 main.py.
Deployment
Because everything in public/ is static, you can deploy it almost anywhere:

GitHub Pages
Netlify
Vercel (as a static site)
Any static file host or simple web server
A simple approach is:

Run ./build.sh(for deployment for local testing main.sh) to rebuild docs/.
Commit and push your repo to GitHub.
Configure your host (e.g. GitHub Pages) to serve the public/ directory or a branch containing its contents.
Learning Goals
This project was built to understand how static site generators work under the hood:

Walking directories and working with files in Python
Parsing and transforming Markdown into HTML
Applying HTML templates to content
Designing a simple build pipeline for static sites
You’re encouraged to extend it: add more templates, metadata, blog indexes, tags, or whatever magic you’d like.
