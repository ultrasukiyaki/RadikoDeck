#!/bin/bash

set -e

APP_NAME="RadikoDeck"

DESKTOP_FILE="${HOME}/.local/share/applications/radikodeck.desktop"

ICON_FILE="${HOME}/.local/share/icons/hicolor/256x256/apps/radikodeck.png"


echo "================================"
echo " 🗑 Removing ${APP_NAME}"
echo "================================"
echo ""


echo "[1/3] Removing desktop entry..."

rm -f "${DESKTOP_FILE}"


echo "[2/3] Removing icon..."

rm -f "${ICON_FILE}"


echo "[3/3] Updating desktop cache..."

update-desktop-database \
"${HOME}/.local/share/applications" \
2>/dev/null || true


gtk-update-icon-cache \
"${HOME}/.local/share/icons/hicolor" \
2>/dev/null || true


echo ""
echo "================================"
echo " ✅ ${APP_NAME} removed"
echo "================================"
echo ""

echo "Note:"
echo "Project files and .venv were kept."
echo "Remove manually if needed:"
echo ""
echo "  rm -rf .venv"

