import board, busio, sdcardio, storage, os, time, digitalio
import displayio, pwmio, terminalio, adafruit_st7735r
from adafruit_display_text import label
from audiomp3 import MP3Decoder

# Choose appropriate library for AudioOut object
try:
    from audioio import AudioOut
except ImportError:
    try:
        from audiopwmio import PWMAudioOut as AudioOut
    except ImportError:
        print("This board does not support audio")

# use speaker location to creat an AudioOut object named audio
audio = AudioOut(board.GP15)

# SPI SD_CS pin for SD card on Adalogger Cowbell
SD_CS = board.GP17

#  SPI0 setup for SD card
spi0 = busio.SPI(board.GP18, board.GP19, board.GP16)
sdcard = sdcardio.SDCard(spi0, SD_CS)
vfs = storage.VfsFat(sdcard)
try:
    storage.mount(vfs, "/sd")
    print("😎 sd card mounted")
except ValueError:
    print("❌ no SD card")

    # Setup path & filenames
path = "/sd/robot_sounds/"

# setup the MP#Decoder object first & only once
filename = "0.mp3"
mp3_file = open(path + filename, "rb")  # read in data from file
decoder = MP3Decoder(mp3_file)

def play_mp3(filename):
    decoder.file = open(path + filename, "rb")
    audio.play(decoder)
    while audio.playing:
        pass  # replace with function name if you want concurrent operation

print("🐮 Cowbell Adalogger SD Test")
play_mp3("0.mp3")
play_mp3("1.mp3")
play_mp3("2.mp3")

displayio.release_displays()

# SPI setup (SPI1)
spi1 = busio.SPI(clock=board.GP10, MOSI=board.GP11)

# PWM Backlight
backlight = pwmio.PWMOut(board.GP9, frequency=5000, duty_cycle=65535)

# Display bus using ST7735R wiring
display_bus = displayio.FourWire(
    spi1,
    command=board.GP6,        # DC
    chip_select=board.GP7,    # CS
    reset=board.GP8           # RST
)

# THE CRUCIAL LINE (use ST7735R, native portrait, rotate into landscape)
display = adafruit_st7735r.ST7735R(
    display_bus,
    width=160,
    height=128,
    bgr=True,
    rotation=90,
    colstart=0,
    rowstart=0
)

# Root group
splash = displayio.Group()
display.root_group = splash

# Background fill
bg_bitmap = displayio.Bitmap(160, 128, 1)
bg_palette = displayio.Palette(1)
bg_palette[0] = 0x0033FF  # Blue

bg = displayio.TileGrid(bg_bitmap, pixel_shader=bg_palette)
splash.append(bg)

# Text label
text_group = displayio.Group(scale=2, x=20, y=70)
text = label.Label(terminalio.FONT, text="Make Awesome!!", color=0xFFFF00)
text_group.append(text)
splash.append(text_group)

while True:
    pass
