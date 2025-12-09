
import platform
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

print(f"System: {platform.system()}")
print(f"Release: {platform.release()}")
print(f"Version: {platform.version()}")

# Check if Malgun Gothic is available
font_list = [f.name for f in fm.fontManager.ttflist]
malgun_fonts = [f for f in font_list if 'Malgun' in f]
print(f"Malgun fonts found: {malgun_fonts}")

# Check what matplotlib thinks it is doing
print(f"Current Font Family: {plt.rcParams['font.family']}")

# Try finding the font file path
try:
    print(f"Malgun Gothic Path: {fm.findfont('Malgun Gothic')}")
except Exception as e:
    print(f"Error finding Malgun Gothic: {e}")
