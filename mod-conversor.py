import subprocess
import sys

from pathlib import Path


def fatal_error(msg):
    subprocess.run([
        "osascript",
        "-e",
        f'display alert "{msg}"'
    ])
    print("Fatal error: ", msg)
    sys.exit(1)

  
def show_success(output_path):
    script = f'''
    set theFile to POSIX file "{output_path}"
    set theChoice to button returned of (display alert "Conversion Complete" ¬
        message "File saved as:\\n{output_path}" ¬
        buttons {{"OK", "Reveal in Finder"}} ¬
        default button "OK")

    if theChoice is "Reveal in Finder" then
        tell application "Finder"
            activate
            reveal theFile
        end tell
    end if
    '''

    subprocess.run(["osascript", "-e", script])

    
# Check if ffmpeg is installed in the computers
def check_ffmpeg() -> bool:
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        print("ffmpeg is installed and working")
        return True
    except FileNotFoundError:
        print("ffmpeg is not installed")
    except subprocess.CalledProcessError:
        print("ffmpeg exists but failed to run")

    return False


# Validate if the input file is the correct type
def validate_mod_file(path):
    if path.suffix.lower() != ".mod":
        fatal_error("The selected file type is not .MOD")
        

# Get the filepath from finder
def choose_file():
    try:
        script = 'POSIX path of (choose file)'
        result = subprocess.run(
            ["osascript", "-e", script], 
            capture_output=True,
            text=True
        )
        
        # User pressed cancel
        if result.returncode != 0:
            fatal_error("The file selection was cancelled")
            
        # Convert it to Path type
        input_path = Path(result.stdout.strip())
        print(input_path)
        
        # Check if its a correct mod file
        validate_mod_file(input_path)
            
        # Check if selected file exists
        if not input_path.exists():
            fatal_error("The selected file does not exist")
            
        # Create output_path and check if it already exists
        output_path = input_path.with_suffix(".mp4")
        if output_path.exists():
            fatal_error("The file has already been converted or there is another with the same name")
            
        return input_path, output_path
    
    except Exception as e:
        fatal_error(f"File picker failed: {e}")
    
    
# Build the ffmpeg command
def run_ffmpeg(input, output):
    # Never build it as a string just in case the filepath contains spaces
    cmd = [
        "ffmpeg",
        "-i", str(input),
        "-vf", "bwdif",
        "-preset", "slow",
        "-crf", "16",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output)
    ]
    
    try:
        result = subprocess.run(cmd)
        
        if result.returncode != 0:
            fatal_error("ffmpeg failed during conversion.")
        
        print("Return code: ", result.returncode)
        
    except FileNotFoundError:
        fatal_error("ffmpeg executable not found")
        
    except Exception as e:
        fatal_error(f"ffmpeg execution failed {e}")


def main():
    check_ffmpeg()
    
    input_path, output_path = choose_file()
    
    print("Converting: ", input_path.name)
    
    run_ffmpeg(input_path, output_path)
    
    print("Conversion complete: ", output_path)
    
    show_success(output_path)
    
    

# have the output terminal be printed in a new window
# double-clickable .app bundle


if __name__=="__main__":
    main()