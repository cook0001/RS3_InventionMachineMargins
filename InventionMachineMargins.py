import webview
import os
import sys

def main():
    # Handle PyInstaller one-file bundled path
    if hasattr(sys, '_MEIPASS'):
        base_dir = getattr(sys, '_MEIPASS')
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
    html_path = os.path.join(base_dir, 'alt1', 'index.html')
    
    if not os.path.exists(html_path):
        print(f"Error: Could not find {html_path}")
        sys.exit(1)
        
    webview.create_window(
        title='Invention Machine Margins',
        url=f'file://{html_path}',
        width=1200,
        height=800,
        min_size=(800, 600),
        background_color='#0B0E14'
    )
    webview.start()

if __name__ == '__main__':
    main()
