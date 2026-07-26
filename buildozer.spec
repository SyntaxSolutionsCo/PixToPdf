[app]

# (str) Title of your application
title = PixToPdf

# (str) Package name
package.name = pixtopdf

# (str) Package domain (needed for android packaging)
package.domain = org.pixtopdf

# (list) Source files to include (let it include python files, png icons, etc.)
source.include_exts = py,png,jpg,kv,atlas

# (list) List of inclusion patterns naming the files/directories to include
source.include_patterns = assets/*,images/*

# (list) Source files to exclude (let it exclude non-essential files)
source.exclude_exts = spec

# (list) List of directory to exclude (from source dir)
source.exclude_dirs = tests, bin, venv

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,pillow,pyjnius

# (str) Supported orientations
orientation = portrait

# (list) Permissions
# Needed for accessing images and saving generated PDF files
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_IMAGES

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Graphics API to use (opengles 2 or 3)
android.graphics = opengles2

# (bool) Indicate whether the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color
presplash.color = #0F172A