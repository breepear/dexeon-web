# Render marketing/logo-story.html to an Instagram Story MP4 (1080x1920, 30 fps).
# Usage: python3 marketing/logo-story.py [--frames-only] [--test]
#   --test renders four sample frames to <out>/test-*.png and stops.
# Frames go to $DEXEON_FRAMES (default: marketing/.frames, gitignored); the MP4 to
# assets/social/stories/dexeon-logo-story.mp4. ffmpeg is looked up on PATH, then
# $FFMPEG.
import os, sys, subprocess, time, shutil, glob

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
FPS, DUR = 30, 7.0
OUT_DIR = os.environ.get('DEXEON_FRAMES', 'marketing/.frames')
MP4 = 'assets/social/stories/dexeon-logo-story.mp4'
POSTER = 'assets/social/stories/dexeon-logo-story-poster.png'
os.makedirs(OUT_DIR, exist_ok=True)

def shot(t, path):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1080,1920', '--virtual-time-budget=6000', f'--screenshot={path}',
                    f'http://localhost:8765/marketing/logo-story.html?t={t:.4f}'],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    if '--test' in sys.argv:
        for t in (0.9, 1.3, 2.3, 6.5):
            shot(t, f'{OUT_DIR}/test-{t:.1f}.png'); print('test frame', t)
        sys.exit(0)
    n = int(FPS * DUR)
    for i in range(n):
        shot(i / FPS, f'{OUT_DIR}/f-{i:04d}.png')
        if i % 30 == 0: print(f'frame {i}/{n}')
    shot(DUR - 0.01, POSTER)
finally:
    srv.terminate()

if '--frames-only' in sys.argv: sys.exit(0)
ffmpeg = shutil.which('ffmpeg') or os.environ.get('FFMPEG')
if not ffmpeg: sys.exit('ffmpeg not found: install it or set $FFMPEG')
subprocess.run([ffmpeg, '-y', '-framerate', str(FPS), '-i', f'{OUT_DIR}/f-%04d.png',
                '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '17', '-preset', 'slow', '-movflags', '+faststart', MP4], check=True,
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print('wrote', MP4)
