#!/bin/bash
set -ex

_VENV="$1"
_SRCDIR="$2"
_PACKAGE="mohd_pdf_enhance"
_BUILD_DIR="${_SRCDIR}/build"
_DESTINATION="${_SRCDIR}/${_PACKAGE}.exe"

# Copy package
rm -rf "${_BUILD_DIR}"
mkdir "${_BUILD_DIR}"
cp -r "${_SRCDIR}/code/${_PACKAGE}" "${_BUILD_DIR}"

# Add main script to package
cp main.py "${_BUILD_DIR}/__main__.py"

# Build zipapp and make the exe
python -m zipapp --output "${_BUILD_DIR}/${_PACKAGE}.pyz" --python "python/pythonw.exe" "${_BUILD_DIR}"
cp "${_VENV}/lib/python3.11/site-packages/distlib/w64.exe" "${_DESTINATION}"
#echo '#!python/pythonw.exe' >> "${_DESTINATION}"
cat "${_BUILD_DIR}/${_PACKAGE}.pyz" >> "${_DESTINATION}"
