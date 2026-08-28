#!/bin/bash

set -e

APP_NAME="RadikoDeck"

APP_DIR="$(cd "$(dirname "$0")" && pwd)"

VENV_DIR="${APP_DIR}/.venv"

DESKTOP_DIR="${HOME}/.local/share/applications"

ICON_DIR="${HOME}/.local/share/icons/hicolor/256x256/apps"

ICON_SOURCE="${APP_DIR}/assets/radiko-icon-circle.png"

DESKTOP_FILE="${DESKTOP_DIR}/radikodeck.desktop"


echo "================================"
echo " 📻 Installing ${APP_NAME}"
echo "================================"
echo ""


#
# Python
#

echo "[1/7] Checking Python..."

if ! command -v python3 >/dev/null 2>&1
then
    echo ""
    echo "ERROR: python3 not found"
    exit 1
fi


PYTHON_VERSION=$(python3 --version)

echo "Found: ${PYTHON_VERSION}"


#
# venv
#

echo ""
echo "[2/7] Checking venv support..."

if ! python3 -m venv --help >/dev/null 2>&1
then
    echo ""
    echo "ERROR: python3-venv is required"
    echo ""
    echo "Install:"
    echo "  sudo apt install python3-venv"
    exit 1
fi


#
# mpv
#

echo ""
echo "[3/7] Checking mpv..."

if ! command -v mpv >/dev/null 2>&1
then
    echo ""
    echo "ERROR: mpv not found"
    echo ""
    echo "Install:"
    echo "  sudo apt install mpv"
    exit 1
fi


echo "Found: $(which mpv)"


#
# Virtual Environment
#

echo ""
echo "[4/7] Creating virtual environment..."


if [ ! -d "${VENV_DIR}" ]
then
    python3 -m venv "${VENV_DIR}"
else
    echo "Existing venv found"
fi


echo ""
echo "Installing Python packages..."


"${VENV_DIR}/bin/python" -m pip install \
    --upgrade pip


"${VENV_DIR}/bin/pip" install \
    -r "${APP_DIR}/requirements.txt"


#
# Icon
#

echo ""
echo "[5/7] Installing icon..."


if [ -f "${ICON_SOURCE}" ]
then

    mkdir -p "${ICON_DIR}"

    cp \
    "${ICON_SOURCE}" \
    "${ICON_DIR}/radikodeck.png"

else

    echo "Warning: icon not found"
    echo "${ICON_SOURCE}"

fi


#
# Desktop Entry
#

echo ""
echo "[6/7] Creating desktop entry..."


mkdir -p "${DESKTOP_DIR}"


cat > "${DESKTOP_FILE}" <<DESKTOP
[Desktop Entry]
Type=Application
Name=RadikoDeck
Comment=Linux Radio Player
Exec=${VENV_DIR}/bin/python ${APP_DIR}/main.py
Path=${APP_DIR}
Icon=radikodeck
Terminal=false
Categories=Audio;Player;
StartupNotify=true
DESKTOP


chmod +x "${DESKTOP_FILE}"


#
# Update cache
#

echo ""
echo "[7/7] Updating desktop database..."


update-desktop-database \
"${DESKTOP_DIR}" \
2>/dev/null || true


gtk-update-icon-cache \
"${HOME}/.local/share/icons/hicolor" \
2>/dev/null || true


echo ""
echo "================================"
echo " ✅ ${APP_NAME} installation complete"
echo "================================"
echo ""

echo "Launch:"
echo "  ${APP_NAME}"
echo ""

