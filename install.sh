#!/bin/bash

# Clone the repository
git clone https://github.com/ShijazKS/Quran-Reciters.git

# Move into the repository directory
cd Quran-Reciters

# Make the Python script executable
chmod +x quran_recitation.py

# Optionally, move the script to a location in the user's PATH
mv quran_recitation.py ~/bin/Quran

echo "Installation complete."
echo "You can now run the program by typing 'Quran' in the terminal."
echo "Type 'q' to go previous page."
