[app]

# Application identity
title = Math Guessing
package.name = guessmath
package.domain = org.myko

# Source
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,ttf

# Version
version = 0.1

# Requirements
requirements = python3,kivy

# Orientation
orientation = portrait
fullscreen = 0

# Android configuration
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Architectures
android.archs = arm64-v8a, armeabi-v7a

# SDK / NDK (let buildozer manage them)
# DO NOT duplicate these anywhere else
android.sdk = 33
android.ndk = 25b

# Output format
android.debug_artifact = apk

# Bootstrap
p4a.bootstrap = sdl2

# Permissions (optional, safe default)
android.permissions = INTERNET

# Allow backup
android.allow_backup = True


[buildozer]

log_level = 2
warn_on_root = 1
