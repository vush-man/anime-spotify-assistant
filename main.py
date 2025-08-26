import tkinter as tk
from ui import AnimeSpotifyUI

def main():
    root = tk.Tk()
    app = AnimeSpotifyUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()