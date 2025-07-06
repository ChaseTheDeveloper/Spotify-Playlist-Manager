import subprocess
import sys

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False
    return True

if __name__ == "__main__":
    print("Setting up Spotify Playlist Manager...")
    if install_requirements():
        print("\n🎵 Setup complete! You can now run: python spotify_playlist_manager.py")
    else:
        print("\n❌ Setup failed. Please install dependencies manually.")