#!/bin/bash
pyside6-uic src/ui/main_window.ui -o src/views/main_window.py
pyside6-uic src/ui/preference.ui -o src/views/preference.py
pyside6-uic src/ui/camera_calibration.ui -o src/views/camera_calibration.py
pyside6-uic src/ui/stereo_calibration.ui -o src/views/stereo_calibration_ui.py
pyside6-uic src/ui/stereo_calibration2.ui -o src/views/stereo_calibration2_ui.py
pyside6-uic src/ui/camera_inspect.ui -o src/views/camera_inspect_ui.py