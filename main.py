# TO DO:
# Check wifi, drive auth, check log
# Read savefolder
# Save folder in drive
# Update log
# Display info
from drive import *

def main():
    creds = authenticate()
    service = build("drive", "v3", credentials=creds)

    list_files(service)


if __name__ == "__main__":
    main()