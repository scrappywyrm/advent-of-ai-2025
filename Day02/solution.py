import subprocess
import sys
import os

def run_simple_solution():
    print("🎄 Day 2: Simple Solution (Direct Prompting)...")
    
    # The Mega-Prompt containing all requirements
    prompt = """
    Build a festive "Choose Your Own Adventure" web app as a SINGLE HTML file (index.html).
    
    Requirements:
    1. Theme: "The Winter Festival's Missing Storyteller".
    2. Styling: Beautiful winter CSS (dark blue background, white text, snowflakes, emojis).
    3. Structure:
       - Start: You arrive at the festival gates.
       - Choice A: Go to the Hot Cocoa Stand.
       - Choice B: Go to the Ice Skating Rink.
       - Choice C: Investigate the suspiciously quiet Storyteller's Tent.
    4. Mechanics:
       - Use JavaScript to handle navigation (hide/show sections).
       - No external assets (use CSS/SVG/Emojis for visuals).
       - At least 3 branching paths and 2 distinct endings.
       - A "Restart Story" button at the end.
    
    Output ONLY the raw HTML code. Start with <!DOCTYPE html>.
    """

    try:
        # Run Goose directly (Bypassing the Operator for Track 1)
        print(">> Asking Goose to build the app...")
        
        # We use 'goose run' which automatically uses the 'developer' extension
        # to fulfill the request if it decides to write a file.
        result = subprocess.run(
            [
                'goose', 'run',
                '--no-session',
                '-t', prompt,
                '-q' # Quiet mode
            ],
            capture_output=True,
            text=True,
            timeout=180 # Give it time to write code
        )

        if result.returncode == 0:
            html_content = result.stdout
            
            # Save to file
            with open("simple_story.html", "w") as f:
                f.write(html_content)
                
            print("✅ Success! Generated 'simple_story.html'")
            print("👉 Open this file in your browser to test.")
        else:
            print(f"❌ Error: {result.stderr}")

    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    run_simple_solution()
