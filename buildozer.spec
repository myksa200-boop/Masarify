[app]

# (str) Title of your application
title = مصاريفي

# (str) Package name
package.name = masarify

# (str) Package domain (needed for android/ios packaging)
package.domain = com.masarify.budget

# (str) Source code where the main.py lives
source.dir = .

# (list) Source files to include (let you install python dependencies)
source.include_exts = py,png,jpg,kv,ttf,atlas

# (list) Source files to exclude
source.exclude_exts = spec

# (list) List of additional paths to include in the APK
source.include_patterns = fonts/*.ttf

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.3.1,kivymd==1.2.0,plyer

# (str) Custom source folders for requirements
# requirements.source.kivy = ../kivy

# (list) Garden requirements
# garden_requirements =

# (str) Presplash of the application
presplash.filename = %(source.dir)s/Masarify_icon.png

# (str) Icon of the application
icon.filename = %(source.dir)s/Masarify_icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API
android.api = 33

# (int) Minimum API
android.minapi = 21

# (int) Android SDK version
android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (bool) Use --private storage
android.private_storage = True

# (str) Android logcat filters
android.logcat_filters = *:S python:I

# (bool) Enable AndroidX
android.enable_androidx = True

# (str) Android archs
android.archs = arm64-v8a

# (int) Log level (0 = error only, 1 = info, 2 = debug, 3 = verbose)
log_level = 2

# (str) Window icon (Android)
window_icon = %(source.dir)s/Masarify_icon.png

# (str) Application versioning
version = 1.0.0

# (int) Android numeric version code
version.code = 1

# (bool) Enable the ARM binary translation layer
android.armv7_disabled = True

# (bool) Copy the packaged APK to this directory
android.copy_apk = ./bin/

# (str) The debug keystore for signing
# android.debug_keystore = ~/.android/debug.keystore

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 1

# (int) Number of concurrent jobs for building
jobs = 2
