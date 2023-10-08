import pygame
import sys
import os
import random
import math
import re
import ctypes
import pygame.mixer
import requests
import shutil
import subprocess
import platform

# Define a function to minimize the command prompt window
def minimize_console():
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 6)  # 6 corresponds to SW_MINIMIZE

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Determine the base path depending on whether it's a compiled executable or not
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")

MUSIC_END_EVENT = pygame.USEREVENT + 1


# # GitHub API URL for releases of your repository
# access_token = "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" -- Removed

# Initialize a flag to track whether the update has been performed
update_performed = False

def check_for_update(current_version, repo_owner, repo_name, asset_name):
    global update_performed  # Declare the variable as global to modify its value
    try:
        response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest")
        response.raise_for_status()
        latest_version = response.json()["tag_name"]

        if latest_version != current_version:
            print(f"New version available: {latest_version}")
            download_url = get_asset_download_url(repo_owner, repo_name, asset_name)
            if download_url:
                download_path = os.path.join(os.path.expanduser("~"), "Downloads", asset_name)
                download_file(download_url, download_path)
                print(f"New version downloaded to: {download_path}")
                print("Replace this one, with the one in your Downloads!")

                # Set window title to indicate new version is in Downloads only if update hasn't been performed
                if not update_performed:
                    pygame.display.set_caption(f"New version available: {latest_version}")
                    update_performed = True  # Update the flag to indicate the update has been performed
                
                return download_path
            else:
                print(f"Error: {asset_name} not found in the release assets.")
        else:
            print("You have the latest version.")
            pygame.display.set_caption("Stay Positive")
    except Exception as e:
        print(f"Error checking for updates: {e}")
    return None

def get_asset_download_url(repo_owner, repo_name, asset_name):
    try:
        response = requests.get(f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest")
        response.raise_for_status()
        assets = response.json()["assets"]
        for asset in assets:
            if asset["name"] == asset_name:
                return asset["browser_download_url"]
        return None
    except Exception as e:
        print(f"Error getting asset download URL: {e}")
        return None

def download_file(url, local_path):
    try:
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(local_path, "wb") as out_file:
                shutil.copyfileobj(response.raw, out_file)
    except Exception as e:
        print(f"Error downloading file: {e}")

def run_updated_version(updated_exe_path):
    try:
        subprocess.Popen([updated_exe_path])
    except Exception as e:
        print(f"Error running updated version: {e}")

# Example usage
current_version = "1.0.0"  # Replace this with your current version
repo_owner = "WaveShredder"
repo_name = "Disney-Project"
asset_name = "King-Mickey.exe"

check_for_update(current_version, repo_owner, repo_name, asset_name)

# Set up display
screen_width = 1024
screen_height = 576
screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Positive Thoughts")

# Set the application icon (icon.ico)
icon_path = 'icon.ico'

# Set the application icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(icon_path)

# Check the platform and minimize the console window if on Windows
if platform.system() == "Windows":
    minimize_console()

# Load character frames from the "CharacterAnim" folder
character_folder = os.path.join(base_path, "CharacterAnim")
character_files = [filename for filename in os.listdir(character_folder) if filename.endswith(".png")]
num_frames_character = len(character_files)

character_frames = [pygame.image.load(os.path.join(character_folder, f'character{i}.png')) for i in range(1, num_frames_character + 1)]

font = pygame.font.Font(None, 36)

# Define person's name
person_name = "Always Remember..."  # Replace with the desired name

# Load custom fonts from the "font" folder with different sizes
font_folder = os.path.join(base_path, "font")
name_font = pygame.font.Font(os.path.join(font_folder, "EnchantedLand.ttf"), 60)
button_font = pygame.font.Font(os.path.join(font_folder, "Zootopia.ttf"), 18)

# Load the background image
background_folder = os.path.join(base_path, "backdrop")
background_image = pygame.image.load(os.path.join(background_folder, "pride_rock.jpg"))

# Load the Pride Rock overlay image
overlay_image = pygame.image.load(os.path.join(background_folder, "pride_rock2.png"))
overlay_x = 0  # Set the initial X position for the overlay
overlay_y = 0  # Set the initial Y position for the overlay

# Lion Animation
lion_folder = os.path.join(base_path, "CharacterAnim/lion")
lion_files = [filename for filename in os.listdir(lion_folder) if filename.endswith(".png")]
num_frames_lion = len(lion_files)

lion_frames = [pygame.image.load(os.path.join(lion_folder, f'{i}.png')) for i in range(1, num_frames_lion + 1)]

# Lion Animation
chip_folder = os.path.join(base_path, "CharacterAnim/chip")
chip_files = [filename for filename in os.listdir(chip_folder) if filename.endswith(".png")]
num_frames_chip = len(chip_files)

chip_frames = [pygame.image.load(os.path.join(chip_folder, f'{i}.png')) for i in range(1, num_frames_chip + 1)]

# Mickey's Magic
magic_animation_folder = os.path.join(base_path, "CharacterAnim/magic")
magic_animation_files = [filename for filename in os.listdir(magic_animation_folder) if filename.endswith(".png")]
num_frames_magic = len(magic_animation_files)

magic_frames = [pygame.image.load(os.path.join(magic_animation_folder, f'{i}.png')) for i in range(1, num_frames_magic + 1)]

# Load Lion Cub Animation
lion_cub_folder = os.path.join(base_path, "CharacterAnim/lion/simba")
lion_cub_files = [filename for filename in os.listdir(lion_cub_folder) if filename.startswith("s") and filename.endswith(".png")]
num_frames_lion_cub = len(lion_cub_files)

lion_cub_frames = [pygame.image.load(os.path.join(lion_cub_folder, f)) for f in sorted(lion_cub_files)]

# Function to display the person's name without the fading effect
def display_name(screen, name):
    smaller_font_size = 30  # Change this to the desired font size
    smaller_font = pygame.font.Font(os.path.join(font_folder, "EnchantedLand.ttf"), smaller_font_size)
    
    text = smaller_font.render(name, True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 1.50, 165))
    screen.blit(text, text_rect)

# Function to display random text with pink highlighted words
def display_random_text(screen, text, alpha, max_width, max_height, time_elapsed):
    default_font_size = 40  # Default font size
    max_font_size = 60  # Maximum font size
    font_size = default_font_size
    font = pygame.font.Font(os.path.join(font_folder, "EnchantedLand.ttf"), font_size)

    # Split the text into lines that fit within the specified width
    words = re.findall(r"\b[\w`]+|[.,!?;]", text)
    lines = []
    current_line = []

    # Define a word bank of words to turn pink
    word_bank = ["beautiful", "always", "enough", "you`ve won", "totally got this", "fighter", "be proud of yourself", "focus", "positive", "start choosing yourself", "It`s okay", "stronger", "braver", "smarter"]  # Add more words as needed

    y_offset = 300  # Initial Y offset
    total_height = 0  # Total height of displayed text

    # Calculate a vertical displacement based on time_elapsed to create the wavy animation
    wave_amplitude = 10  # Adjust this value to control the amplitude of the wave
    vertical_displacement = wave_amplitude * math.sin(time_elapsed * 0.002)  # Adjust the frequency with 0.002

    for word in words:
        current_line.append(word)
        text_size = font.size(' '.join(current_line))

        # Check if adding the word exceeds the maximum width
        if text_size[0] > max_width:
            while text_size[0] > max_width:
                # Remove the last word from the current line
                current_line.pop()
                text_size = font.size(' '.join(current_line))
            lines.append(current_line)
            current_line = [word]
            total_height += text_size[1]

        # Check if adding the word exceeds the maximum height
        if total_height + text_size[1] > max_height:
            break  # Stop rendering if it exceeds the max_height

    lines.append(current_line)

    for line in lines:
        text_to_render = ' '.join(line)

        # Create a text surface without the white border
        text_surface = font.render(text_to_render, True, (255, 255, 255))

        # Calculate the position of the text
        text_rect = text_surface.get_rect(center=(screen_width // 1.5, y_offset + vertical_displacement))

        # Blit the text surface
        screen.blit(text_surface, text_rect)

        # Update the Y offset and total height
        y_offset += text_rect.height

        # Check if any word in the word bank appears in the line and turn them pink
        for word in word_bank:
            # Convert to lowercase for case-insensitive matching
            lowercase_line = text_to_render.lower()
            lowercase_word = word.lower()

            # Use regular expressions to find and highlight the word in pink
            matches = [m.start() for m in re.finditer(r'\b' + re.escape(lowercase_word) + r'\b', lowercase_line)]
            for match in matches:
                end_index = match + len(lowercase_word)
                # Calculate the corresponding position in the original text
                start_pos = len(lowercase_line[:match])
                end_pos = start_pos + len(lowercase_word)

                # Render the pink word
                pink_word_surface = font.render(text_to_render[start_pos:end_pos], True, (255, 192, 203))
                # Calculate the position of the pink word within the text surface
                pink_word_rect = pink_word_surface.get_rect()
                pink_word_rect.topleft = (
                    text_rect.left + font.size(text_to_render[:start_pos])[0] - .72,
                    text_rect.top  # Adjust for vertical displacement
                )
                # Blit the pink word onto the screen
                screen.blit(pink_word_surface, pink_word_rect)

    # Decrease font size if the text doesn't fit the specified width
    while text_rect.width > max_width and font_size > 1:
        font_size -= 1
        font = pygame.font.Font(os.path.join(font_folder, "EnchantedLand.ttf"), font_size)

        for line in lines:
            text_to_render = ' '.join(line)

            # Create a text surface without the white border
            text_surface = font.render(text_to_render, True, (0, 0, 0))

            # Calculate the position of the text
            text_rect = text_surface.get_rect(center=(screen_width // 1.5, y_offset + vertical_displacement))

            # Blit the text surface
            screen.blit(text_surface, text_rect)

            # Update the Y offset
            y_offset += text_rect.height

            # Check if any word in the word bank appears in the line and turn them pink
            for word in word_bank:
                # Convert to lowercase for case-insensitive matching
                lowercase_line = text_to_render.lower()
                lowercase_word = word.lower()

                # Use regular expressions to find and highlight the word in pink
                matches = [m.start() for m in re.finditer(r'\b' + re.escape(lowercase_word) + r'\b', lowercase_line)]
                for match in matches:
                    end_index = match + len(lowercase_word)
                    # Calculate the corresponding position in the original text
                    start_pos = len(lowercase_line[:match])
                    end_pos = start_pos + len(lowercase_word)

                    # Render the pink word
                    # pink_word_surface = font.render(text_to_render[start_pos:end_pos], True, (255, 0, 255))
                    # Calculate the position of the pink word within the text surface
                    pink_word_rect = pink_word_surface.get_rect()
                    pink_word_rect.topleft = (text_rect.left + font.size(text_to_render[:start_pos])[0], text_rect.top)
                    # Blit the pink word onto the screen
                    screen.blit(pink_word_surface, pink_word_rect)

# Fading parameters
fade_duration = 1000
current_fade_frame = 0

# Set initial character position and frame
character_x = 115
character_y = 390
character_speed = 0
character_frame_index = 0
character_frame_count = 0
character_frame_delay = 125
character_animation_finished = False

# Phase variables
current_phase = "initial"
replay_frame_start = num_frames_character - 4
replay_frame_index = 0

# Define restart button properties
button_width = 95
button_height = 30
button_color = (0, 128, 255) # Color when the button is pressed
button_pressed_color = (0, 100, 200)  # Color when the button is pressed
button_text_color = (255, 255, 255)
restart_button = pygame.Rect(screen_width - button_width - 20, 20, button_width, button_height)
button_pressed = False

# Defining the Lion
lion_x = screen_width  # Initial X position of the lion
lion_y = 500  # Y position of the lion (adjust as needed)
lion_speed = .18  # Adjust the lion's speed
lion_direction = "left"  # Initial direction (can be "right" or "left")
lion_scale = (25, 25)  # Adjust the lion's size (width, height)

# Defining the Lion Cub
lion_cub_x = screen_width  # Initial X position of the lion
lion_cub_y = 510  # Y position of the lion (adjust as needed)
lion_cub_speed = .13  # Adjust the lion's speed
lion_cub_direction = "left"  # Initial direction (can be "right" or "left")
lion_cub_scale = (15, 15)  # Adjust the lion's size (width, height)

# Defining the Lion Cub
chip_x = 230  # Initial X position of the lion
chip_y = 394  # Y position of the lion (adjust as needed)
# chip_speed = .13  # Adjust the lion's speed
chip_scale = (23, 30)  # Adjust the lion's size (width, height)

# Mickey Magic
magic_x = 300  # Initial X position of the magic animation
magic_y = 415  # Y position of the magic animation
magic_angle = 10  # Angle in degrees towards the Random Text
magic_speed = .05  # Speed of the magic animation
magic_delay = 2000  # Delay before starting the magic animation in milliseconds (5 seconds)
magic_scale = (250, 70)  # Initial size of the magic animation (width, height)


# Load the sound effect
sound_folder = os.path.join(base_path, "sounds")
sound_effect = pygame.mixer.Sound(os.path.join(sound_folder, "twinkle.wav"))

# Set the initial volume (between 0.0 and 1.0)
sound_volume = 0.08  # Adjust the volume as needed (0.5 means 50% volume)
sound_effect.set_volume(sound_volume)

# Define the folder where your background music files are stored
music_folder = os.path.join(base_path, "sounds/music")

# set the initial music volume
music_volume = .35  # Adjust the volume as needed (0.5 means 50% volume)

# Load text lines from a file
text_folder = os.path.join(base_path, "strings")
text_file_path = os.path.join(text_folder, "text.txt")
with open(text_file_path, "r") as file:
    text_lines = [line.strip() for line in file.readlines()]

# Function to get a random text that is not the same as the current text
def get_random_text(current_text, text_lines):
    new_text = current_text
    while new_text == current_text:
        new_text = random.choice(text_lines)
    return new_text

# Initialize the current text with a random text
current_text = get_random_text("", text_lines)
current_text_surface = None
current_text_alpha = 0

# Function to restart the animation
def restart_animation():
    global current_fade_frame, current_text_surface, current_text_alpha, current_text
    current_fade_frame = 3
    current_text = get_random_text(current_text, text_lines)  # Choose a new random line
    current_text_surface = None  # Reset the text surface
    current_text_alpha = 0
    return 100, 0, 0, False, "initial"

# Restart cooldown variables
restart_cooldown = False
restart_cooldown_duration = 2000  # 2 seconds

lion_frame_index = 0
lion_frame_count = 0
lion_frame_delay = 100
max_lion_distance = 20
lion_timer = 3000  # Delay for the lion in milliseconds (3 seconds)
lion_start_time = 0  # Initialize the start time for the lion

lion_cub_frame_index = 0
lion_cub_frame_count = 0
lion_cub_frame_delay = 130
max_lion_cub_distance = 20
lion_cub_timer = 8000  # Delay for the lion in milliseconds (3 seconds)
lion_cub_start_time = 0  # Initialize the start time for the lion cub

# Main animation loop
running = True
clock = pygame.time.Clock()
current_timer = 0
button_pressed = False  # Initialize button_pressed here

# Function to play random background music
def play_random_background_music():
    if not pygame.mixer.music.get_busy():
        # List all files in the music folder
        music_files = [f for f in os.listdir(music_folder) if f.endswith(".wav")]

        if music_files:
            random_music_file = random.choice(music_files)
            music_path = os.path.join(music_folder, random_music_file)
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.set_volume(music_volume)
            pygame.mixer.music.play(0)  # Play the music without looping
            pygame.mixer.music.set_endevent(MUSIC_END_EVENT)  # Set the music end event

# Play random background music on program launch
play_random_background_music()

# Display the name initially
display_name(screen, person_name)

chip_frame_index = 0  # Start with the first frames
chip_frame_count = 0
chip_frame_delay = 500  # Adjust the delay between frames

# Add a variable to control the delay before Chip animation restarts
chip_restart_delay = 10000  # 10 seconds (adjust as needed)
chip_restart_timer = current_timer + chip_restart_delay  # Initialize the restart timer

chip_animation_active = True  # Flag to control whether Chip animation is active

magic_animation_started = False
magic_animation_start_time = 0
magic_frame_index = 0
magic_frame_count = 0
magic_replay_delay = 1000

# Magic Animation Constants
magic_delay = 1500  # Delay before starting the magic animation in milliseconds (2 seconds)
magic_frame_delay = 35  # Adjust the delay between frames

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not restart_cooldown:
            if restart_button.collidepoint(event.pos):
                sound_effect.stop()
                sound_effect.play()
                character_x, character_frame_index, character_frame_count, character_animation_finished, current_phase = restart_animation()
                lion_x = screen_width  # Reset lion's position
                lion_cub_x = screen_width # Resets lion cub position
                restart_cooldown = True
                current_timer = 0
                  # Reset magic animation variables
                magic_animation_started = False
                magic_animation_start_time = current_timer  # Start magic animation after the delay
                magic_frame_index = 0
                magic_frame_count = 0
                button_pressed = True

        # Check for mouse button release to reset the button state
        if event.type == pygame.MOUSEBUTTONUP:
            button_pressed = False

    # Get the mouse cursor position
    mouse_x, mouse_y = pygame.mouse.get_pos()

     # Calculate elapsed time
    current_time = pygame.time.get_ticks()
    if 'previous_time' not in locals():
        previous_time = current_time  # Initialize previous_time if it doesn't exist
    elapsed_time = current_time - previous_time
    previous_time = current_time  # Update previous_time for the next iteration

    # Calculate magic frame index based on elapsed time since magic animation start time
    elapsed_time_since_magic_start = current_timer - magic_animation_start_time
    magic_frame_index = (elapsed_time_since_magic_start // magic_frame_delay) % num_frames_magic

    elapsed_time = clock.tick(60)
    current_timer += elapsed_time

    # Blit the background image
    screen.blit(background_image, (0, 0))

    # Update lion position and frame
    if current_timer >= lion_start_time + lion_timer:
        if lion_direction == "right":
            lion_x += lion_speed
            if lion_x > screen_width + max_lion_distance:
                lion_x = -lion_scale[0]
        else:
            lion_x -= lion_speed
            if lion_x < -lion_scale[0] - max_lion_distance:
                lion_x = screen_width

        current_lion_frame = pygame.transform.scale(lion_frames[lion_frame_index], lion_scale)
        screen.blit(current_lion_frame, (lion_x, lion_y))

        lion_frame_count += elapsed_time
        if lion_frame_count >= lion_frame_delay:
            lion_frame_index = (lion_frame_index + 1) % len(lion_frames)
            lion_frame_count = 0    

    # Update lion cub position and frame when the timer is up
    if current_timer >= lion_cub_start_time + lion_cub_timer:
        if lion_cub_direction == "right":
            lion_cub_x += lion_cub_speed
            if lion_cub_x > screen_width + max_lion_cub_distance:
                lion_cub_x = -lion_cub_scale[0]
        else:
            lion_cub_x -= lion_cub_speed
            if lion_cub_x < -lion_cub_scale[0] - max_lion_cub_distance:
                lion_cub_x = screen_width

        current_lion_cub_frame = pygame.transform.scale(lion_cub_frames[lion_cub_frame_index], lion_cub_scale)
        screen.blit(current_lion_cub_frame, (lion_cub_x, lion_cub_y))

        lion_cub_frame_count += elapsed_time
        if lion_cub_frame_count >= lion_cub_frame_delay:
            lion_cub_frame_index = (lion_cub_frame_index + 1) % len(lion_cub_frames)
            lion_cub_frame_count = 0
    
    # Render "pride_rock2" on top of "pride_rock"
    screen.blit(overlay_image, (overlay_x, overlay_y))

    # Display the Chip animation
    if chip_animation_active:
        chip_frame_count += elapsed_time
        if chip_frame_count >= chip_frame_delay:
            chip_frame_index = (chip_frame_index + 1) % len(chip_frames)
            chip_frame_count = 0

        current_chip_frame = pygame.transform.scale(chip_frames[chip_frame_index], chip_scale)
        screen.blit(current_chip_frame, (chip_x, chip_y))
    else:
        # Check if it's time to restart the Chip animation
        if chip_animation_active:
            chip_animation_active = False  # Activate Chip animation
            chip_frame_index = 0  # Reset the frame index
            chip_restart_timer = 0  # Reset the timer
        else:
            # Deactivate Chip animation and display the last frame
            current_chip_frame = pygame.transform.scale(chip_frames[chip_frame_index], chip_scale)
            screen.blit(current_chip_frame, (chip_x, chip_y))
    
    # Check if it's time to start the magic animation
    if not magic_animation_started and current_timer >= magic_animation_start_time + magic_delay:
        magic_animation_started = True
        magic_animation_start_time = current_timer  # Update the start time

    # Draw the magic animation if it has started
    if magic_animation_started:
        magic_frame_count += elapsed_time
        if magic_frame_count >= magic_frame_delay:
            magic_frame_index = (magic_frame_index + 1) % len(magic_frames)
            magic_frame_count = 0

        # Rotate and scale the magic animation image
        rotated_magic_frame = pygame.transform.rotate(magic_frames[magic_frame_index], magic_angle)
        scaled_magic_frame = pygame.transform.scale(rotated_magic_frame, magic_scale)

        # Create a new surface with the rotated and scaled magic animation
        magic_surface = pygame.Surface(scaled_magic_frame.get_size(), pygame.SRCALPHA)
        magic_surface.blit(scaled_magic_frame, (0, 0))  # Blit the magic animation onto the new surface

        # Calculate the position based on angle
        magic_rect = magic_surface.get_rect(center=(magic_x, magic_y))
        rotated_magic_surface = pygame.transform.rotate(magic_surface, magic_angle)

        # Adjust the position to simulate the angle
        rotated_magic_rect = rotated_magic_surface.get_rect(center=magic_rect.center)

        # Blit the rotated and scaled magic animation surface onto the screen
        screen.blit(rotated_magic_surface, rotated_magic_rect.topleft)

    # Display the mouse coordinates
    # mouse_x, mouse_y = pygame.mouse.get_pos()
    # # text = font.render(f"Mouse X: {mouse_x}, Mouse Y: {mouse_y}", True, (255, 255, 255))
    # screen.blit(text, (10, 10))

    # Check if it's time to restart the Chip animation
    if not chip_animation_active and current_timer >= chip_restart_timer:
        chip_animation_active = True  # Activate Chip animation
        chip_restart_timer = 0  # Reset the timer

    # screen.blit(text, (10, 10))
    if current_phase == "initial":
        alpha = int((current_fade_frame / fade_duration) * 255)
        if alpha > 255:
            alpha = 255

        current_fade_frame += 1

        display_name(screen, person_name)

        screen.blit(character_frames[character_frame_index], (character_x, character_y))

        character_x += character_speed

        if character_x > screen_width:
            character_x = -100

        character_frame_count += elapsed_time
        if character_frame_count >= character_frame_delay and not character_animation_finished:
            character_frame_index = (character_frame_index + 1) % len(character_frames)
            character_frame_count = 0

            if character_frame_index == len(character_frames) - 1:
                character_frame_count = character_frame_delay
                character_animation_finished = True

        if character_animation_finished:
            current_phase = "replay"

    elif current_phase == "replay":
        display_name(screen, person_name)  # Display the name during the replay phase
        display_random_text(screen, current_text, current_text_alpha, screen_width - 500, 415, current_timer)

        screen.blit(character_frames[replay_frame_start + replay_frame_index], (character_x, character_y))

        character_x += character_speed

        character_frame_count += elapsed_time
        if character_frame_count >= character_frame_delay:
            replay_frame_index = (replay_frame_index + 1) % 4
            character_frame_count = 0

            if character_x > screen_width:
                character_x = -100

        if current_text_alpha < 255:
            current_text_alpha = min(current_text_alpha + 2, 255)

    # Draw the button background (either pressed or normal)
    if button_pressed:
        pygame.draw.rect(screen, button_pressed_color, restart_button)
    else:
        pygame.draw.rect(screen, button_color, restart_button)

    # Draw the button text on top of the button background
    restart_text = button_font.render("Smile", True, button_text_color)
    screen.blit(restart_text, (screen_width - button_width - 0, 25))

    if event.type == MUSIC_END_EVENT:
            play_random_background_music()  # Play a new random song

    pygame.display.update()

    if restart_cooldown and current_timer >= restart_cooldown_duration:
        restart_cooldown = False

pygame.quit()
sys.exit()
