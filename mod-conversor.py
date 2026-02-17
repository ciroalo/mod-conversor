import subprocess
import sys
import os

from pathlib import Path

# This method is used because the .app bundle doesnt see homebrew folders
def add_common_paths():
    extra = ["/opt/homebrew/bin", "/usr/local/bin"]
    current = os.environ.get("PATH", "")
    os.environ["PATH"] = ":".join(extra + [current])


def show_loading():
    """
    Show a non-blocking Applescript loading dialog.
    Returns the process so we can close it later.
    """
    script = '''
    display dialog "Converting… Please wait." ¬
        with title "MOD → MP4 Converter" ¬
        buttons {} giving up after 99999
    '''
    
    proc = subprocess.Popen(
        ["osascript", "-e", script],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    
    return proc


def hide_loading(proc):
    """
    Close the loading dialog safely
    """
    if proc and proc.poll() is None:
        proc.terminate()
    

def fatal_error(msg):
    subprocess.run([
        "osascript",
        "-e",
        f'display alert "{msg}"'
    ])
    print("Fatal error: ", msg)
    sys.exit(1)

  
def show_success_summary(converted, skipped):
    # converted/skipped are lists of strings
    converted_text = "\\n".join(converted) if converted else "(none)"
    skipped_text = "\\n".join(skipped) if skipped else "(none)"

    script = f'''
    set convertedText to "{converted_text}"
    set skippedText to "{skipped_text}"

    display alert "Batch Conversion Complete" ¬
        message "Converted:\\n" & convertedText & "\\n\\nSkipped:\\n" & skippedText ¬
        buttons {{"OK"}} default button "OK"
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
        fatal_error("ffmpeg is not installed")
    except subprocess.CalledProcessError:
        fatal_error("ffmpeg exists but failed to run")

    return False


# Validate if the input file is the correct type
def validate_mod_file(path) -> bool:
    return path.suffix.lower() == ".mod"
        

# Get the filepath from finder
def choose_files() -> list[Path]:
    """
    Returns a list of Path objects for selected files.
    Cancels safely is a user press Cancel
    """
    try:
        # Return newline-separated POSIX paths
        script = r'''
        set theFiles to choose file with multiple selections allowed
        set outText to ""
        repeat with f in theFiles
            set outText to outText & (POSIX path of f) & linefeed
        end repeat
        return outText
        '''
        
        result = subprocess.run(
            ["osascript", "-e", script], 
            capture_output=True,
            text=True
        )
        
        # User pressed cancel
        if result.returncode != 0:
            fatal_error("The file selection was cancelled")
        
        # Split lines, remove empties
        paths = [Path(p) for p in result.stdout.splitlines() if p.strip()]
        
        # Check if no files were selected
        if not paths:
            fatal_error("No files were selected")
        
        return paths
        
    except Exception as e:
        fatal_error(f"File picker failed: {e}")
    
    
# Build the ffmpeg command
def run_ffmpeg(input: Path, output: Path):
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
        return True, ""
        
    except FileNotFoundError:
        return False, "ffmpeg executable not found"
        
    except Exception as e:
        return False, f"ffmpeg execution failed {e}"


def main():
    add_common_paths()
    
    check_ffmpeg()
    
    input_paths = choose_files()
    
    converted, skipped = [], []
    
    loading_proc = show_loading()
    
    try:
        for input_path in input_paths:
            # Basic existence check
            if not input_path.exists():
                skipped.append(f"{input_path.name} (missing)")
                continue
            
            # Validate extension
            if not validate_mod_file(input_path):
                skipped.append(f"{input_path.name} (not .MOD)")
                continue
            
            output_path = input_path.with_suffix(".mp4")
            
            # Skip if it already exists
            if output_path.exists():
                skipped.append(f"{input_path.name} (output exists)")
                continue
            
            print("Converting: ", input_path.name)
            
            ok, err = run_ffmpeg(input_path, output_path)
            if ok:
                converted.append(output_path.name)
            else:
                skipped.append(f"{input_path.name} ({err})")
    finally:
        hide_loading(loading_proc)
            
    # Show summary pop up at the end
    show_success_summary(converted, skipped)
    
    

# have the output terminal be printed in a new window
# double-clickable .app bundle
# do it for multiple files at the same time


if __name__=="__main__":
    main()