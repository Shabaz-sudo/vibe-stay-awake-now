
# Resource file for icons and other resources

# This is a placeholder for a real resource file
# In a real application, you would use PyQt's resource system (pyrcc5)
# to compile resources into a Python module

# For now, we'll create some dummy icons as base64 data

import os
from PyQt5.QtCore import QDir

# Create a directory for icons if it doesn't exist
icons_dir = os.path.join(os.path.dirname(__file__), "icons")
os.makedirs(icons_dir, exist_ok=True)

# Create a simple cursor icon
with open(os.path.join(icons_dir, "cursor.png"), "wb") as f:
    # This is a simple base64-encoded PNG image of a cursor
    cursor_icon_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00uIDAT8OcDP\xb3\xfe\x9f\x01\x0b`DW\xc0\xc8\xc0\xc0\xf0\x9f\x01\x07\xa0\xa2\x00\x97Z\\\x8a\xd0\x15\xe0P\x88\xaa\x00W\xc0\xa3*\xc0\x1d\xc1\xc8\n\x08\xf8\x0e\xd5\x12\x06\x06\xc2\xc1\x8e*@\xf5$\x81\n\xc8I\'(\x89\x14e\x90\x98T/\x81\x9c\xa4J\x9er\xbciA\x8e\x02\xf4T\x8e-\x15\x13\xd3\x00N+\xc8\x01\x14\xa5\x02|\x86\x10S\r\xce4@\xb1\x02\x00\xe8\\\x17\xba\xf1\xb5?\xd7\x00\x00\x00\x00IEND\xaeB`\x82'
    f.write(cursor_icon_data)

# Create a check icon for the checkbox
with open(os.path.join(icons_dir, "check.svg"), "w") as f:
    f.write("""<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <polyline points="20 6 9 17 4 12"></polyline>
</svg>""")

print("Created resources in:", icons_dir)
