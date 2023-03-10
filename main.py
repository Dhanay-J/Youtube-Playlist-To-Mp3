import os, threading

from pytube import Playlist
from moviepy.editor import AudioFileClip

err_chars = '/\\:*?\"<>|'


class AutoDownloader:

    def __init__(self, url):
        self.p = Playlist(url)

    def converter(self, mp4, mp3):  # Converts video to mp3
        aud = AudioFileClip(mp4)
        aud.write_audiofile(mp3)
        aud.close()
        os.popen(f'del \"{mp4}\"')
        print('Completed : ', mp3)

    def run(self):

        try:
            new_folder = ''.join(i for i in self.p.title if i not in err_chars)
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)  # Makes a new folder with playlist title

            for vid in self.p.videos:
                old_name = vid.streams.get_audio_only().default_filename
                old_dest = new_folder + '\\' + old_name
                new_dest = new_folder + '\\' + old_name[:-3] + 'mp3'

                if not os.path.exists(old_dest):  # If the file alredey exists avoid download 
                    vid.streams.get_audio_only().download(new_folder)
                    t = threading.Thread(target=self.converter, args=[old_dest, new_dest, ])
                    t.start()
        except Exception as e:
            print(e)


p_urls = [ ]  # Playlist URLs

for url in p_urls:
    r = AutoDownloader(url)
    r.run()
print('\n\n\n\n\n\n\n', '*' * 10, 'Complete All Downloads', '*' * 10)
# os.system('rundll32.exe powrprof.dll,SetSuspendState sleep')  # This line will sleep the running windows system to sleep mode after completion
