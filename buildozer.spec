[app]

# Application title
title = Math Guessing

# Package name
package.name = guessmath

# Package domain
package.domain = org.example

# Source directory
source.dir = .

# File extensions to include
source.include_exts = py,png,jpg,kv,atlas,ttf

# Application version
version = 0.1

# Requirements
requirements = python3,kivy

# Orientation
orientation = portrait

# Fullscreen (0 = false, 1 = true)
fullscreen = 0


#
# ANDROID SETTINGS
#

# Target Android API (compile SDK)
android.api = 33

# Minimum supported Android API
android.minapi = 21

# Android SDK version
android.sdk = 33

# REQUIRED: Supported NDK version
android.ndk = 25b

# NDK API (must match minapi)
android.ndk_api = 21

# Architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# Allow Android backup
android.allow_backup = True

# Debug build artifact
android.debug_artifact = apk


#
# PYTHON-FOR-ANDROID (p4a)
#
# Use pre-cloned python-for-android
p4a.source_dir = /root/python-for-android

p4a.source_dir = /home/guessmath/python-for-android

# Bootstrap
p4a.bootstrap = sdl2


#
# BUILDOZER SETTINGS
#

[buildozer]

# Log level (2 = full debug output)
log_level = 2

# Warn if run as root
warn_on_root = 1
