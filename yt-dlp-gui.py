import os
import threading
import subprocess
import tkinter as tk
import sys

class YouTubeDownloader:
    def __init__(self):
        self.total_urls = 0
        self.remaining_urls = 0
        self.window = tk.Tk()
        self.window.title("yt_dlp")
        self.window.configure(bg="#000")
        self.window.option_add("*Foreground", "#8C7828")
        self.create_widgets()

    def create_widgets(self):
        url_label = tk.Label(self.window, text="URLs:", font=("Arial", 12), bg="#000")
        url_label.grid(row=0, column=0, sticky="NSEW")

        self.url_box = tk.Text(self.window, height=10, width=50, bg="#000", fg="#8C7828", font=("Arial", 12), insertbackground="#8C7828", undo=True)
        self.url_box.grid(row=1, column=0, sticky="NSEW")
        self.url_box.focus_set()

        # context menu
        menu = tk.Menu(self.window, tearoff=0, bg="#111")
        menu.add_command(label="Cut", command=lambda: self.url_box.event_generate("<<Cut>>"))
        menu.add_command(label="Copy", command=lambda: self.url_box.event_generate("<<Copy>>"))
        menu.add_command(label="Paste", command=lambda: self.url_box.event_generate("<<Paste>>"))
        self.url_box.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(1, weight=1)

        download_button = tk.Button(self.window, text="Download", command=self.download_button_pressed, bg="#8C7828", fg="#000", font=("Arial", 16), relief="groove")
        download_button.grid(row=2, column=0, sticky = "NSEW")

        self.status_label = tk.Label(self.window, text="Feed Your Head", font=("Arial", 12), bg="#000", fg="#44f")
        self.status_label.grid(row=3, column=0, sticky="NSEW")

        self.window.iconbitmap('yt-dlp.ico')

    def download_button_pressed(self):
        urls = self.url_box.get("1.0", tk.END).strip().split("\n")
        urls = list(set(urls))
        self.url_box.delete("1.0", tk.END)
        output_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.start_download(urls, output_dir)

    def start_download(self, urls, output_dir):
        urls[:] = [u for u in urls if u != '']
        if len(urls) > 0:
            self.remaining_urls += len(urls)
            self.total_urls = self.remaining_urls
            r_plural = "" if self.total_urls == 1 else "s"
            self.status_label.config(text=f"{self.remaining_urls}/{self.total_urls} URL{r_plural} remaining", fg=f"#007f00")
            for url in urls:
                if "list" in url:
                    output_formatting = os.path.join(output_dir, '%(playlist_uploader)s', '%(playlist_title)s', '%(playlist_index)s - %(title)s.%(ext)s')
                else:
                    output_formatting = os.path.join(output_dir, '%(uploader)s', '%(title)s.%(ext)s')
                cmd = [
                    os.path.join(os.getcwd(), "yt-dlp.exe"),
                    '--extract-audio', '--audio-format', 'mp3',
                    url, '--output', output_formatting, '--embed-thumbnail'
                ]
                try:
                    process = subprocess.Popen(cmd)
                    thread = threading.Thread(target=self.update_status_label, args=[process])
                    thread.start()
                except Exception as err:
                    self.status_label.config(text=err, fg="#f44")
        else:
            self.status_label.config(fg="#f44")
            if self.remaining_urls == 0:
                self.status_label.config(text="Zero URLs")

    def update_status_label(self, process):
        process.wait()
        self.remaining_urls -= 1
        greenness = hex(255 - int(self.remaining_urls*128/self.total_urls))[-2:]
        t_plural = "" if self.total_urls == 1 else "s"
        r_plural = "" if self.remaining_urls == 1 else "s"
        if self.remaining_urls == 0:
            self.status_label.config(text=f"Download{t_plural} complete", fg=f"#00{greenness}00")
        else:
            self.status_label.config(text=f"{self.remaining_urls} of {self.total_urls} URL{r_plural} remaining", fg=f"#00{greenness}00")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    downloader = YouTubeDownloader()
    downloader.run()