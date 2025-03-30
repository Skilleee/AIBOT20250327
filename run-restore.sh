#!/bin/bash
cd "$(dirname "$0")"

echo "Vill du återställa senaste backup eller välja version?"
echo "1) Återställ senaste version"
echo "2) Välj specifik backupversion"
read -p "Ditt val [1/2]: " choice

if [ "$choice" == "2" ]; then
    read -p "Ange filnamn (ex: strategy.py): " filename
    python3 restore_backups.py --file "$filename" --choose
else
    python3 restore_backups.py
fi
