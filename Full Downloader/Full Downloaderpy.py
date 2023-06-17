import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter
import threading
import yt_dlp as youtube_dl
import re
import os
import yt_dlp
import webbrowser



class YoutubeDownloadWindow(tk.Tk):
    
    #___________________________________get res from youtube video_______________________#
    def get_unique_resolutions(self, inf_dict):
       youtube_link="https://youtu.be" 
       short_link="https://youtube.com/shorts/" 
       if youtube_link in self.url_field.get() or short_link in self.url_field.get() :  
        resolutions = {}
        for format in inf_dict['formats']:
            if re.match(r'^\d+p', format['format_note']) :
                resolution_id = format['format_id']
                resolution = format['format_note']
                if 'HDR' in resolution:
                    resolution = re.search(r'\d+p\d* HDR', resolution)[0]
                resolutions[resolution ] =resolution_id
                
        resolutions = [(v, k) for k, v in resolutions.items()]
        return sorted(resolutions, key=lambda k: [int(k[1].split('p')[0]), k[1].split('p')[-1]])
       else:
           return ""
    #___________________________________get res from youtube video_______________________#
    
    
    #___________________________________Enter res in compobox_______________________#
    def create_resolutions_dropdown(self, info_dict):
        resolutions = self.get_unique_resolutions(info_dict)
        self.resolutions_fields['values'] = [res[1] for res in resolutions]
        self.ids = {res[1]: res[0] for res in resolutions}
        self.resolutions_fields.current(0)
    #___________________________________Enter res in compobox_______________________#    
    
        
    #___________________________________progress_bar_downloading_______________________#
    def progress_hook(self , data):
        if data['status'] == 'downloading':
            downloaded = data['downloaded_bytes']

            total = data['total_bytes']  if data.get('total_bytes' ,None) else data['total_bytes_estimate']
            self.percentage = downloaded / total * 100
            self.percentage = round(self.percentage, 2)
           
            self.progress_bar["value"] =  self.percentage
            self.progress_bar.update()
            
            self.style.configure('text.Horizontal.TProgressbar', text=f'%{self.percentage}')
            self.progress_bar.place(x=220,y=365)
            self.download_type_label.place(x=3,y=365)
    #___________________________________progress_bar_downloading_______________________#
    
    
            
    #___________________________________We Call This Function When Press On (browse)_______________________#        
    def get_ready(self):
        info_dict = self.download_info_dict()
        self.create_resolutions_dropdown(info_dict)
        self.status.configure(text=f"{info_dict['title']}")
    #___________________________________We Call This Function When Press On (browse)_______________________#       
##################
########## 
#####     
#     
#
#           
##################
##########  #download video#
#####   
    def download_info_dict(self):# to get all information from your video    #
        global ydl_opts
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio/best',
            'forcejson': True,
            'dump_single_json': True,
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(self.url_field.get(), download=False)
        return info_dict

    def setup_ydl_opts(self):
        youtube_link="https://youtu.be"
        if youtube_link in self.url_field.get():
         format = self.ids[self.resolutions_fields.get()]
         download_folder = self.des_field.get()

         return {
            'format': f"{format}+bestaudio",
            'merge_output_format': 'mkv' ,
            'quiet': True,
            'no_warnings': True,
            'progress':True,
            'progress_hooks': [self.progress_hook],
            "external_downloader_args": ['-loglevel', 'panic'],
            'outtmpl': os.path.join(
                download_folder, '%(title)s-%(format)s.%(ext)s'
            ),
            }
        else:
            self.resolutions_fields.configure(state="disabled")
            download_folder = self.des_field.get()
            self.status.configure(text=f"Downloading Your Video Please Wait....")
            return {
            'format': f"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            '--rm-cache-dir': True,
             'html5': '1',
             'c': 'TVHTML5',
             'cver': '6.20180913',
            'progress_hooks': [self.progress_hook],
            "external_downloader_args": ['-loglevel', 'panic'],
            'outtmpl': os.path.join(download_folder, '%(title)s.%(ext)s'),
            }
            

    def download_video(self):
        # Retrieve the string from the entry fields
        youtube_url = self.url_field.get()
        download_folder = self.des_field.get()
        Basic_link="https://"
        Not_Basic_Link="https://youtube.com/playlist"
        # Check if the entry fields are not empty
        if self.url_field.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")
            self.status.configure(text="Erorr , PLease check again...")
        elif self.des_field.get()=="":
            messagebox.showerror("Empty Field", "Enter Destination....")
            self.status.configure(text="Erorr , PLease check again...")
        
        elif self.des_field.get()=="" and self.url_field.get()=="":
            messagebox.showerror("Empty Fields", "Fields are empty!")
            self.status.configure(text="Erorr , PLease check again...")
            
        elif Basic_link not in self.url_field.get():
            messagebox.showerror("Error", "Invalid Link....")
            self.des_field.delete(0,1000)
            self.url_field.delete(0,1000)
            self.resolutions_fields.configure(state="normal")
            self.download_video_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")
        
        elif Not_Basic_Link  in self.url_field.get():
            messagebox.showerror("Error", "This Link Is Playlist Link Make Sure To Put In his Field....")
            self.des_field.delete(0,1000)
            self.url_field.delete(0,1000)
            self.url_playlist_field.delete(0,1000)
            self.resolutions_fields.configure(state="normal")
            self.download_video_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")
            
        else:
           if  self.pause_downloading:
            ydl_opts = self.setup_ydl_opts()

            # Download the video
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([youtube_url])
                ex=ydl.extract_info(self.url_field.get(), download=False)
                ex.get("title")

            # Hide progress bar and show download complete message
         
            messagebox.showinfo(title='Download Complete', message=f'downloaded successfully {ex.get("title")}')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
             info_dict = ydl.extract_info(self.url_field.get(), download=False)
             
            self.status.configure(text=f"Video downloaded successfully in {self.des_field.get()}")
            self.download_video_button.configure(state="disabled")
            self.resolutions_fields.configure(state="normal")
            self.des_field.delete(0,1000)
            self.url_playlist_field.delete(0,1000)
            self.url_sound_field.delete(0,1000)
            self.url_field.delete(0,1000)
            self.resolutions_fields.set("")
            self.progress_bar.place(x=170,y=500)
            self.download_type_label.place(x=170,y=500)
##################
##########   #download video#
#####       
#
#
#
##################
##########   #download Sound#
#####       
    
    def down_sound(self):
        self.pause=False
        Basic_link="https://"
        Not_Basic_Link="https://youtube.com/playlist"
        if self.url_sound_field.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")
            self.status.configure(text="Erorr , PLease check again...")
        elif self.des_field.get()=="":
            messagebox.showerror("Empty Field", "Enter Destination....")
            self.status.configure(text="Erorr , PLease check again...")
        
        elif self.des_field.get()=="" and self.url_sound_field.get()=="":
            messagebox.showerror("Empty Fields", "Fields are empty!")
            self.status.configure(text="Erorr , PLease check again...")
            
        elif Basic_link not in self.url_sound_field.get():
            messagebox.showerror("Error", "Invalid Link....")
            self.des_field.delete(0,1000)
            self.url_field.delete(0,1000)
            self.url_sound_field.delete(0,1000)
            self.download_music_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")
            
        elif Not_Basic_Link  in self.url_sound_field.get():
            messagebox.showerror("Error", "This Link Is Playlist Link Make Sure To Put In his Field....")
            self.des_field.delete(0,1000)
            self.url_field.delete(0,1000)
            self.url_sound_field.delete(0,1000)
            self.download_music_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")
        
        else:
         if  self.pause_downloading:
          URLS =f'{self.url_sound_field.get()}'
          info_dict = yt_dlp.YoutubeDL().extract_info(url=self.url_sound_field.get(), download=False)
          self.get_sound_information=info_dict.get("title")
          self.status.configure(text=f"{self.get_sound_information}")
          download_folder = self.des_field.get()
          sound_format=self.bitrat_fields.get().replace("kbps","")
          ydl_opts1 = {
          'format': 'bestaudio/best',
          'quiet': True,
          'no_warnings': True,
          'progress':True,
          'progress_hooks': [self.progress_hook],
          "external_downloader_args": ['-loglevel', 'panic'],
          'postprocessors': [{
          'key': 'FFmpegExtractAudio',
          'preferredcodec': 'mp3',
          'preferredquality': f'{sound_format}',
           }],
           'outtmpl':os.path.join(download_folder,f'{"%(title)s-%(format)s.%(ext)s"}'),
           }  
         
          with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
           download_sound = ydl.download(self.url_sound_field.get())
           messagebox.showinfo("Congratulations",f"Sound Downloaded Successfully..{self.get_sound_information}")
           self.status.config(text=f"Successfully Downloading Sound in {self.des_field.get()}......")
           self.download_music_button.config(state="disabled")
           self.des_field.delete(0,1000)
           self.url_playlist_field.delete(0,1000)
           self.url_sound_field.delete(0,1000)
           self.url_field.delete(0,1000)
           self.resolutions_fields.delete(0,1000)
           self.progress_bar.place(x=170,y=500)
           self.download_type_label.place(x=170,y=500)
        
       
##################
##########   #download Sound#
#####        
#
#
#
##################
##########   #download Playlist#
#####     
   
    def down_playlist(self):
        global home_directory
        download_folder = self.des_field.get()
        Basic_link="https://youtube.com/playlist?list"
        Not_Basic_Link="https://youtu.be/"
        # Check if the entry fields are not empty
        if self.url_playlist_field.get()=="":
            messagebox.showerror("Empty Field", "Enter Link....")
            self.status.configure(text="Erorr , PLease check again...")
        
        elif Not_Basic_Link  in self.url_playlist_field.get():
            messagebox.showerror("Error", "This Link Is Youtube Link Make Sure To Put In his Field....")
            self.des_field.delete(0,1000)
            self.url_playlist_field.delete(0,1000)
            self.download_playist_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")
            
        elif Basic_link not in self.url_playlist_field.get():
            messagebox.showerror("Error", "Invalid Link...")
            self.des_field.delete(0,1000)
            self.url_playlist_field.delete(0,1000)
            self.download_playist_button.configure(state="disabled")
            self.status.configure(text="Erorr , PLease check again...")

        elif Basic_link  in self.url_playlist_field.get():
            if  self.pause_downloading:
             if self.playlist_type_fields.get()=="mp4":
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.url_playlist_field.get()}', download=False)
              playlist_title = playlist_info.get('title', None)
              self.status.config(text=f"Downloading {playlist_title}......")
              playlist_opts = {
             'format': f'{"bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"}',
             'outtmpl': f'{download_folder}//{"%(title)s.%(ext)s"}',
             'playlist': True,
             'quiet': True,
             'no_warnings': True,
             'progress':True,
             'progress_hooks': [self.progress_hook],
             "external_downloader_args": ['-loglevel', 'panic'],
             'video-multistreams ':True,
              }
             elif self.playlist_type_fields.get()=="mp3":
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.url_playlist_field.get()}', download=False)
              playlist_title = playlist_info.get('title', None)
              self.status.config(text=f"Downloading {playlist_title}......")
              playlist_opts = {
             'format': f'{"bestaudio/best[ext=mp3]"}',
             'outtmpl': f'{download_folder}//{"%(title)s"}.mp3',
             'playlist': True,
             'quiet': True,
             'no_warnings': True,
             'progress':True,
             'progress_hooks': [self.progress_hook],
             "external_downloader_args": ['-loglevel', 'panic'],
             'audio-multistreams ':True,
              }
            
             with yt_dlp.YoutubeDL(playlist_opts) as ydl:
              playlist_info = yt_dlp.YoutubeDL().extract_info(f'{self.url_playlist_field.get()}', download=False)
              playlist_title = playlist_info.get('title', None)        
              ydl.download([f'{self.url_playlist_field.get()}']) 
              messagebox.showinfo("Congratulations","Sound Downloaded Successfully...")
              self.status.config(text=f"Playlist Successfully Downloading in {self.des_field.get()}......")
              self.download_playist_button.config(state="normal")
              self.des_field.delete(0,1000)
              self.url_playlist_field.delete(0,1000)
              self.url_sound_field.delete(0,1000)
              self.url_field.delete(0,1000)
              self.resolutions_fields.delete(0,1000)
              self.progress_bar.place(x=170,y=500)
              self.download_type_label.place(x=170,y=500)

##################
##########   #download Playlist#
#####     
#
#
#
##################
##########   #Call Functions#
#####     
    def browse_folder(self):
        self.status.configure(text=f"State : Ready")
        self.resolutions_fields.delete(0,1000)
        self.download_music_button.configure(state="disabled")
        self.download_playist_button.configure(state="disabled")
        self.download_video_button.configure(state="disabled")
        self.des_field.delete(0,1000)
        download_path = filedialog.askdirectory(initialdir = "Desktop", title = "Select the folder to save the video")  
        self.des_field.insert(0,download_path)
        youtube_link="https://youtu.be"
        short_link="https://youtube.com/shorts/" 
        if self.url_field.get()!="" and (youtube_link in self.url_field.get() or short_link in self.url_field.get()) :
            self.download_video_button.configure(state="normal")
            self.resolutions_fields.configure(state="normal")
            download_thread = threading.Thread(target=self.get_ready)
            download_thread.start()
        elif self.url_sound_field.get()!="":
            self.download_music_button.configure(state="normal")   
        elif self.url_playlist_field.get()!="":
            self.download_playist_button.configure(state="normal")
        elif self.url_field.get()!="" and youtube_link not in self.url_field.get() :
            self.download_video_button.configure(state="normal")
            self.resolutions_fields.configure(state="disabled")
        
    def download_video_thread(self):
        basic="https://"
        if not self.pause_downloading:
            messagebox.showinfo("Download Manager","Unlock Lock Key.... ")
        elif basic not in self.url_field.get():
             messagebox.showerror("Error","Invalid Link....")
        elif basic  in self.url_field.get():
          webbrowser.open(self.url_field.get())
          download_thread = threading.Thread(target=self.download_video)
          if download_thread.start():
            self.progress_bar.place(x=170,y=340)
            self.status.configure(text="Downloading Please Wait....")
          else:
            self.progress_bar.place(x=170,y=500)
            return ""
    
    def download_Sound_thread(self):
        basic="https://"
        if not self.pause_downloading:
            messagebox.showinfo("Download Manager","Unlock Lock Key.... ")
        elif basic not in self.url_sound_field.get():
            messagebox.showerror("Error","Invalid Link....")
        elif basic in self.url_sound_field.get():
         webbrowser.open(self.url_sound_field.get())
         download_thread = threading.Thread(target=self.down_sound)
         if  download_thread.start():
          self.progress_bar.place(x=170,y=340)
          self.status.configure(text=f"{self.get_sound_information}")
         else:
            self.progress_bar.place(x=170,y=500)
            return ""
        
    def download_Playlist_thread(self):
        basic="https://"
        if not self.pause_downloading:
            messagebox.showinfo("Download Manager","Unlock Lock Key.... ")
        elif basic not in self.url_playlist_field.get():
            messagebox.showerror("Error","Invalid Link....")
        elif basic in self.url_playlist_field.get():
         webbrowser.open(self.url_playlist_field.get())
         download_thread = threading.Thread(target=self.down_playlist)
         if  download_thread.start():
          self.progress_bar.place(x=170,y=340)
          self.status.configure(text="Downloading Please Wait....")
         else:
            self.progress_bar.place(x=170,y=500)
            return ""
        
   
    def reset(self):
        self.des_field.delete(0,1000)
        self.url_playlist_field.delete(0,1000) 
        self.url_sound_field.delete(0,1000)
        self.url_field.delete(0,1000)
    
    def cancel_down(self):
        self.status.config(text=f"Closing Program Goodbye....")
        messagebox.showinfo("Downloading Manager","Downloading has been stopped\nThanks For Using Our Program..")
        os._exit(0)
     
     
    def about_program(self):
        messagebox.showinfo("About Program","""Note:\n1) Download Video: Input Any Link Of Any Video From Any Platform You Want , Choose Your LOcation To Save And Wait For (1) Second To Load Video Qualities Then, Choose Your Qulaity And Click Download.\n
2) Download Sound: Input Any Link Of Any Sound From Any Platform You Want , Choose Your LOcation To Save And Your Bitrat Then Click Download .\n
3) Download Playlist: Input Any Link Of Any Playlist From Any Platform You Want , Choose Your Playlist Type , Then Click Download  (Choose Location).'""")
    
    def git_hub(self):
        webbrowser.open("https://github.com/KILLER-RAMADAN")

    def about_me(self):
        messagebox.showinfo("Hello Im Ahmed Ramadan","Aouther;Ahmed Rmadan\nVersion;1.0\nDeveloped By Me Dont Worry.")
        
        
        
        
    def stop_download(self):
        if not self.pause_downloading:
            self.pause_downloading=True
            self.lock_button.configure(image=self.img5)
        else:
            self.pause_downloading=False
            self.lock_button.configure(image=self.img6)
            
    def black_color(self):
        self.configure(bg="#1f1f1f")  
        self.header_label.configure(bg="#1f1f1f",fg="white")
        self.header_frame.configure(bg="white")
        self.url_label.configure(bg="#1f1f1f",fg="white")
        self.url_playlist_label.configure(bg="#1f1f1f",fg="white")
        self.url_sound_label.configure(bg="#1f1f1f",fg="white")
        self.des_label.configure(bg="#1f1f1f",fg="white")
        self.resolutions_label.configure(bg="#1f1f1f",fg="white")
        self.sound_bitrat_label.configure(bg="#1f1f1f",fg="white")
        self.playlist_type_label.configure(bg="#1f1f1f",fg="white")
        self.lock_button.configure(bg="#1f1f1f")
        self.status.configure(bg="#1f1f1f",fg="white")
        self.progress_bar.configure(bg="#1f1f1f",fg="white")
        self.download_type_label.configure(bg="#1f1f1f",fg="white")
    def white_color(self):
        self.configure(bg="white") 
        self.header_label.configure(bg="white",fg="black")
        self.header_frame.configure(bg="black")
        self.url_label.configure(bg="white",fg="black")
        self.url_playlist_label.configure(bg="white",fg="black")
        self.url_sound_label.configure(bg="white",fg="black")
        self.des_label.configure(bg="white",fg="black")
        self.resolutions_label.configure(bg="white",fg="black")
        self.sound_bitrat_label.configure(bg="white",fg="black")
        self.playlist_type_label.configure(bg="white",fg="black")
        self.lock_button.configure(bg="white")
        self.status.configure(bg="white",fg="black") 
        self.progress_bar.configure(bg="white",fg="black")
        self.download_type_label.configure(bg="white",fg="black")
            
                                                       
##################
##########   #Call Functions#
#####  
#
#
#
##################
##########   # Main Window #
#####   
    def __init__(self):
        super().__init__()
        
        self.pause_downloading=False
        
        # To Access At Any Desktop #
        global home_directory 
        home_directory = os.path.expanduser( '~' )
        # To Access At Any Desktop #
        #______________________________________ Main Window _________________________________ 
        
        # setting the title of the window  
        self.title("⚡Downloader With Full Access⚡")
        
    
        # setting the size and position of the window  
        self.geometry("700x431+420+200")  
        
        
    
        # disabling the resizable option for better UI  
       
        self.resizable(0,0) 
        self.attributes("-topmost",True)
        self.configure(bg="white")  
        # configuring the background color of the window  
                  
        self.img3=tk.PhotoImage(file="images//about.png")
        
        self.img4=tk.PhotoImage(file="images//git.png")
        
        self.img5=tk.PhotoImage(file="images//unlock.png")
    
        self.img6=tk.PhotoImage(file="images//lock.png")
        
        self.img7=tk.PhotoImage(file="images//theme.png")
        # configuring the icon of the window  
        self.iconbitmap("images//download.ico") 
        
        self.menu = tk.Menu(self)
        self.configure(menu=self.menu)
        
        m1 = tk.Menu(self.menu,background="white",activebackground="black")
        self.menu.add_cascade(label="Help",menu=m1)
        m1.add_command(label="developed by",command=self.about_me,image=self.img3,compound="left")
        m1.add_command(label="About Programe",command=self.about_program,image=self.img3,compound="left")
        m1.add_command(label="My GitHub",command=self.git_hub,image=self.img4,compound="left")
        m2 = tk.Menu(self.menu,background="white",tearoff=True,bd=0,activebackground="black")
        self.menu.add_cascade(label="Theme",menu=m2)
        m2.add_command(label="Light",command=self.white_color,image=self.img7,compound="left")
        m2.add_command(label="Dark",command=self.black_color,image=self.img7,compound="left")
        self.menu.add_cascade(label="Exit",command=self.destroy)
        
        #______________________________________ Main Window _________________________________ 
 
    
        #______________________________________ All Text Labels __________________________________# 
        self.header_frame=tk.Frame(width=100000,height=1,bg="black")
        self.header_frame.place(x=0,y=35)
        
        self.header_label = tk.Label(  
             
            text = "⚡Downloader With Full Access⚡",  
            font = ("arial", "15", "bold"),  
            bg = "white",  

            )  
        self.header_label.place(x=170,y=0)
        
        # header_img_label = tk.Label(  
        #     bg="white", 
        #     image=self.img1

        #     )  
        # header_img_label.place(x=425,y=0)
        
        self.url_label = tk.Label(  
            text = "Video URL:",  
            font = ("arial", "15"),  
            bg = "white",  
            fg = "#000000",  
            )  
        self.url_label.place(x=0,y=50)
        
        
        self.url_sound_label = tk.Label(  
            text = "Sound URL:",  
            font = ("arial", "15"),  
            bg = "white",  
            fg = "#000000",  
            )  
        self.url_sound_label.place(x=0,y=125)
        
        
        
        self.url_playlist_label = tk.Label(  
            text = "Playlist URL:",  
            font = ("arial", "15"),  
            bg = "white",  
            fg = "#000000",  
            )  
        self.url_playlist_label.place(x=0,y=200)
        
        self.des_label = tk.Label(  
            text = "Destination:",  
            font = ("arial", "15"),  
            bg = "white",  
            fg = "#000000",  
            anchor = tk.SE  
            )  
        self.des_label.place(x=0,y=260)
        
        self.resolutions_label = tk.Label(
            text="Resolutions:",
            font=("verdana", "12"),
            bg="white",
            fg="#000000",
         
        )
        self.resolutions_label.place(x=470,y=56)
        
        
        
        self.sound_bitrat_label = tk.Label(
            text="Sound Bitrat:",
            font=("verdana", "12"),
            bg="white",
            fg="#000000",
           
        )
        self.sound_bitrat_label.place(x=470,y=130)
        
        
        self.playlist_type_label = tk.Label(
            text="Playlist Type:",
            font=("verdana", "12"),
            bg="white",
            fg="#000000",
         
        )
        self.playlist_type_label.place(x=470,y=208)
        
        self.download_type_label = tk.Label(
            text="Download Progress:",
            font=("verdana", "12"),
            bg="white",
            fg="#000000",
         
        )
        
        
        
 
        
        
        #______________________________________ All Text Labels __________________________________# 
        
        
        
        #______________________________________ Entry Fields __________________________________# 
        self.url_field =ttk.Entry(  
            width = 30,  
            font = ("verdana", "13"),  
            )  
        self.url_field.place(x=118,y=51)
        
        
        self.url_sound_field =ttk.Entry(   
            width = 30,  
            font = ("verdana", "13"),  
            )  
        self.url_sound_field.place(x=118,y=126)
        
        
        self.url_playlist_field =ttk.Entry(
            width = 30,  
            font = ("verdana", "13"),  
           
        
            )  
        self.url_playlist_field.place(x=118,y=200)
        
        
        self.des_field = ttk.Entry(  
            width = 30,  
            font = ("verdana", "13"),   
            )  
        self.des_field.place(x=118,y=260)
        #______________________________________ Entry Fields __________________________________# 

         
    
        
       
        
        #_______________________________________ combobox of res _________________________________#
        
        self.resolutions_fields = ttk.Combobox( state= "readonly", width = 10, font = ("verdana", "8"))
        self.resolutions_fields.place(x=590,y=58)
        
        self.bitrat_fields = ttk.Combobox( state= "readonly", width = 10, font = ("verdana", "8"))
        self.bitrat_fields.place(x=590,y=130)
        self.bitrat_fields['values']=("251kbps","129kbps","128kbps","96kbps")
        self.bitrat_fields.set("251kbps")
        
        
        
        self.playlist_type_fields = ttk.Combobox( state= "readonly", width = 10, font = ("verdana", "8"))
        self.playlist_type_fields.place(x=590,y=208)
        self.playlist_type_fields['values']=("mp3","mp4")
        self.playlist_type_fields.set("mp4")
        
        
        #_______________________________________ combobox of res _________________________________#
        
        
         
        # _____________________________ progress_bar__________________________________#
        self.style = ttk.Style(self)
        self.style.layout('text.Horizontal.TProgressbar',
                    [('Horizontal.Progressbar.trough',
                    {'children': [('Horizontal.Progressbar.pbar',
                                    {'side': 'left', 'sticky': 'ns'})],
                        'sticky': 'nswe'}),
                    ('Horizontal.Progressbar.label', {'sticky': ''})])
        self.style.configure('text.Horizontal.TProgressbar', text='0 %')

        self.progress_bar = ttk.Progressbar( orient = tk.HORIZONTAL, style='text.Horizontal.TProgressbar',
                length = 250, mode = 'determinate')
        
        # _____________________________ progress_bar__________________________________#
        
        
        
        # __________________________________ All Buttons _____________________________#  
        
        self.style.configure("TButton",font =
               ('calibri', 20, 'bold', 'underline'),borderwidth="2")
        self.style.map("info.TButton",foreground=[('active','!disabled','green')],
        background=[('active','green')])

        self.download_video_button = ttk.Button(  
            text = "Download Video",  
            width = 15,  
            state="disabled",
            command = self.download_video_thread  
            )  
        self.download_video_button.place(x=5,y=310)
        
        
        self.download_music_button = ttk.Button( 
            text = "Download Sound",  
            width = 15,  
            state="disabled",
            command = self.download_Sound_thread
            )  
        self.download_music_button.place(x=240,y=310)
        
        
        self.download_playist_button = ttk.Button(  
            text = "Download Playlist",  
            width = 15, 
            state="disabled",
            
            command = self.download_Playlist_thread
            )  
        self.download_playist_button.place(x=470,y=310)
        
        self.browse_button = ttk.Button(   
            text = "Browse",    
            command = self.browse_folder  
            )  
        self.browse_button.place(x=480,y=260)
        
        
        # about_button = tk.Button(   
        #     text = "About Program",  
        #     width = 0,  
        #     bg = "white",  
        #     bd=0,
        #     image=self.img3 ,
        #     relief = tk.GROOVE,  
        #     command = self.about_program 
        #     )  
        # about_button.place(x=620,y=3)
        
        # about_git_hub = tk.Button(   
        #     text = "About Program",  
        #     width = 0,  
        #     bg = "white",  
        #     bd=0,
        #     image=self.img4 ,
        #     relief = tk.GROOVE,  
        #     command = self.git_hub
        #     )  
        # about_git_hub.place(x=660,y=3)
        
        
        self.lock_button = tk.Button(   
            text = "pause",  
            width = 0,  
            bg = "white",  
            bd=0,
            relief = tk.GROOVE,  
            command = self.stop_download
            )  
        self.lock_button.place(x=650,y=260)
        
        self.lock_button.configure(image=self.img6)
       
        self.status = tk.Label(self,text="State : Ready",width=0,fg="black",anchor="w",background="white",
                               font="arial 10 ",bd=1,relief="ridge")
        self.status.place(x=0,y=392,relwidth=1)
        
        
        
        # __________________________________ All Buttons _____________________________#
##################
##########   # Main Window #
#####  
# Call Class To Run Window #
app = YoutubeDownloadWindow()
app.mainloop()
# Call Class To Run Window #
