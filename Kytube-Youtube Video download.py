import os
import sys
import time

try:
    import yt_dlp
except ImportError:
    os.system("pip install yt-dlp")
    import yt_dlp

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    RED = Fore.RED + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    os.system("pip install colorama")
    from colorama import init, Fore, Style
    init(autoreset=True)
    RED = Fore.RED + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    CYAN = Fore.CYAN + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_banner():
    clear_screen()
    banner = f"""
{RED}   #####################################################################################
   #                                                                                   #
   #   {RED}██╗  ██╗██╗   ██╗████████╗██╗   ██╗██████╗ ███████╗{WHITE}   |   Developed by:       #
   #   {RED}██║ ██╔╝╚██╗ ██╔╝╚══██╔══╝██║   ██║██╔══██╗██╔════╝{WHITE}   |                       #
   #   {RED}█████═╝  ╚████╔╝    ██║   ██║   ██║██████╔╝█████╗  {CYAN}   |   ██╗  ██╗██╗   ██╗   #
   #   {RED}██╔═██╗   ╚██╔╝     ██║   ██║   ██║██╔══██╗██╔══╝  {CYAN}   |   ██║ ██╔╝╚██╗ ██╔╝   #
   #   {RED}██║  ██╗   ██║      ██║   ╚██████╔╝██████╔╝███████╗{CYAN}   |   █████═╝  ╚████╔╝    #
   #   {RED}╚═╝  ╚═╝   ╚═╝      ╚═╝    ╚═════╝ ╚═════╝ ╚══════╝{CYAN}   |   ██╔═██╗   ╚██╔╝     #
   #                                                     {CYAN}   |   ██║  ██╗   ██║      #
   #   {WHITE}===============================================   {CYAN}   |   ╚═╝  ╚═╝   ╚═╝      #
   #   {GREEN}              Y O U T U B E  D O W N L O A D E R   {CYAN}   |     Kyronoid v1.0     #
   #                                                                                   #
   #####################################################################################{RESET}
"""
    print(banner)

def download_hook(d):
    if d['status'] == 'downloading':
        pct = d.get('_percent_str', '0%').strip()
        speed = d.get('_speed_str', 'N/A').strip()
        eta = d.get('_eta_str', 'N/A').strip()
        
        try:
            val = float(pct.replace('%', ''))
            fill_len = int(25 * val / 100)
            bar_str = '█' * fill_len + '░' * (25 - fill_len)
        except:
            bar_str = '░' * 25

        sys.stdout.write(f"\r{GREEN}[+] Downloading: {CYAN}[{bar_str}] {YELLOW}{pct}{RESET} | Speed: {WHITE}{speed}{RESET} | ETA: {WHITE}{eta}{RESET}   ")
        sys.stdout.flush()

def download_media(url, mode):
    user_home = os.path.expanduser('~')
    target_dir = os.path.join(user_home, 'Downloads')

    print(f"\n{YELLOW}[i] Fetching video metadata...{RESET}")
    
    try:
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Unknown Title')
            channel = info.get('uploader', info.get('channel', 'Unknown Channel'))
            
        print(f"{CYAN}--------------------------------------------------{RESET}")
        print(f"{WHITE} Title   : {GREEN}{title}{RESET}")
        print(f"{WHITE} Channel : {GREEN}{channel}{RESET}")
        print(f"{CYAN}--------------------------------------------------{RESET}\n")

        if mode == '1':
            opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [download_hook],
                'quiet': True,
                'no_warnings': True
            }
        else:
            opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(target_dir, '%(title)s.%(ext)s'),
                'progress_hooks': [download_hook],
                'quiet': True,
                'no_warnings': True
            }

        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
            
        print(f"\n\n{GREEN}[✔] Success: '{title}' has been saved to your Downloads folder!{RESET}")

    except Exception as err:
        print(f"\n{RED}[✘] Error encountered: {err}{RESET}")

def main():
    while True:
        draw_banner()
        print(f"{WHITE}  [1] Download Video (MP4)")
        print(f"  [2] Download Audio Only")
        print(f"  [Q] Exit\n")
        
        user_choice = input(f"{CYAN}KyTuber: {RESET}").strip().lower()
        
        if user_choice == 'q':
            print(f"\n{GREEN}Exiting. Kyronoid v1.0{RESET}\n")
            break
        elif user_choice in ['1', '2']:
            target_url = input(f"\n{YELLOW}Enter YouTube URL: {RESET}").strip()
            if target_url:
                download_media(target_url, user_choice)
                input(f"\n{WHITE}Press Enter to return to main menu...{RESET}")
            else:
                print(f"{RED}[!] Empty URL given.{RESET}")
                time.sleep(1.2)
        else:
            print(f"{RED}[!] Invalid menu option.{RESET}")
            time.sleep(1)

if __name__ == "__main__":
    main()
