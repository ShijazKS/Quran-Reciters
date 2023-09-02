#!/usr/bin/env python3

import curses
import requests
import subprocess

def audi_link(reciter, number):
    return f"{reciter}/{str(number).zfill(3)}.mp3"



def fetch_reciters():
    url = "https://mp3quran.net/api/_english.php"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        reciters = data.get("reciters", [])
        
        # Remove duplicates by converting the list to a set and back to a list
        reciters = list({reciter["name"]: reciter for reciter in reciters}.values())
        
        return reciters
    else:
        print("Failed to fetch reciters")
        return []

def fetch_chapters():
    url = "https://api.quran.com/api/v4/chapters"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        chapters_data = data.get("chapters", [])

        # Remove duplicates by converting the list to a set and back to a list
        chapters = list({chapter["name_simple"]: chapter for chapter in chapters_data}.values())

        return chapters
    else:
        print("Failed to fetch chapters")
        return []


def display_reciters(stdscr, reciters, start_index, current_item):
    # Clear the screen
    stdscr.clear()

    # Display a subset of reciters with the specified text color
    for i in range(start_index, min(start_index + curses.LINES - 2, len(reciters))):
        reciter = reciters[i]
        try:
            reciter_name = reciter["name"].encode('utf-8', 'ignore').decode('utf-8')
            if i == current_item:
                stdscr.addstr(i - start_index, 0, reciter_name, curses.color_pair(2) | curses.A_BOLD)  # Selected reciter is displayed in red
            else:
                stdscr.addstr(i - start_index, 0, reciter_name, curses.color_pair(1))
        except UnicodeEncodeError:
            # Handle encoding errors gracefully
            stdscr.addstr(i - start_index, 0, "Unsupported characters", curses.color_pair(1))

    stdscr.refresh()

def display_chapters(stdscr, chapters, start_index, current_item):
    # Clear the screen
    stdscr.clear()

    # Display a subset of chapters with the specified text color
    for i in range(start_index, min(start_index + curses.LINES - 2, len(chapters))):
        chapter = chapters[i]
        chapter_name = chapter.get("name_simple", "N/A")  # Get the chapter name or use "N/A" if the key is not found
        try:
            chapter_name = chapter_name.encode('utf-8', 'ignore').decode('utf-8')
            if i == current_item:
                stdscr.addstr(i - start_index, 0, chapter_name, curses.color_pair(2) | curses.A_BOLD)  # Selected chapter is displayed in green
            else:
                stdscr.addstr(i - start_index, 0, chapter_name, curses.color_pair(1))
        except UnicodeEncodeError:
            # Handle encoding errors gracefully
            stdscr.addstr(i - start_index, 0, "Unsupported characters", curses.color_pair(1))

    stdscr.refresh()



def main(stdscr):
    # Initialize curses
    curses.curs_set(0)
    stdscr.clear()

    # Set the color pairs for text and background
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, -1)  # White text, default background
    curses.init_pair(2, curses.COLOR_RED, -1)  # Red text, default background

    reciters = fetch_reciters()
    if not reciters:
        stdscr.addstr(0, 0, "Failed to fetch reciters. Press any key to exit.")
        stdscr.refresh()
        stdscr.getch()
        return

    current_item = 0
    start_index = 0

    while True:
        display_reciters(stdscr, reciters, start_index, current_item)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_item = max(0, current_item - 1)
            if current_item < start_index:
                start_index = current_item
        elif key == curses.KEY_DOWN:
            current_item = min(len(reciters) - 1, current_item + 1)
            if current_item >= start_index + curses.LINES - 2:
                start_index = current_item - curses.LINES + 3
        elif key == ord('q'):
            break
        elif key == 10:  # Enter key
            if current_item == len(reciters):
                break  # Exit the program
            else:
                selected_reciter = reciters[current_item]["name"]
                selected_server = reciters[current_item]["Server"]
                # stdscr.addstr(len(reciters) - start_index, 0, f"You selected: {selected_reciter}", curses.color_pair(3) | curses.A_BOLD)
                stdscr.clear()
                stdscr.refresh()
                # stdscr.getch() 

                chapters = fetch_chapters()
                if not chapters:
                    stdscr.addstr(0, 0, "Failed to fetch chapters. Press any key to exit.")
                    stdscr.refresh()
                    stdscr.getch()
                    return

                current_item = 0
                start_index = 0

                while True:
                    display_chapters(stdscr, chapters, start_index, current_item)
                    key = stdscr.getch()

                    if key == curses.KEY_UP:
                        current_item = max(0, current_item - 1)
                        if current_item < start_index:
                            start_index = current_item
                    elif key == curses.KEY_DOWN:
                        current_item = min(len(chapters) - 1, current_item + 1)
                        if current_item >= start_index + curses.LINES - 2:
                            start_index = current_item - curses.LINES + 3
                    elif key == ord('q'):
                        break
                    elif key == 10:  # Enter key
                        if current_item == len(reciters):
                            break  # Exit the program
                        else:
                            selected_chapter = chapters[current_item]["name_simple"]
                            selected_ch_id = chapters[current_item]["id"]
                            # stdscr.addstr(len(chapters) - start_index, 0, f"You selected: {selected_chapter}", curses.color_pair(3) | curses.A_BOLD)
                            stdscr.clear()
                            stdscr.refresh()
                            # stdscr.addstr(0, 0, f"You selected: {selected_chapter}", curses.color_pair(3) | curses.A_BOLD)
                            audio_link = audi_link(selected_server,selected_ch_id)
                            stdscr.addstr(0, 0, f"Surah: {selected_chapter} | Reciter:{selected_reciter} \n", curses.color_pair(1) | curses.A_BOLD)  # Use color pair 1 (white text) with a bold attribute
                            # stdscr.addstr(1, 0, f"Audio Link: {audio_link}", curses.color_pair(1))
                            stdscr.refresh()
                            # stdscr.getch()

                            # Play the audio using mpv
                            subprocess.run(["mpv", audio_link])

    
if __name__ == "__main__":
    curses.wrapper(main)

# url={audiLink(reciterDetail.Server, chapterDetail.id)}
# const audiLink = (reciter, number) =>
#     reciter + '/' + ('00' + number).slice(-3) + '.mp3'
# http://server9.mp3quran.net/zahrani/001.mp3