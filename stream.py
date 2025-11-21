import os
import argparse

def create_m3u(directory, output_file):
    # Define movie file extensions to look for.
    movie_extensions = {'.mp4', '.mkv', '.avi', '.mov', '.flv'}
    
    # Open the output file and write the M3U header.
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('#EXTM3U\n')
            
            # Walk through the directory recursively.
            for root, dirs, files in os.walk(directory):
                for file in files:
                    ext = os.path.splitext(file)[1].lower()
                    if ext in movie_extensions:
                        file_path = os.path.join(root, file)
                        # Write the EXTINF metadata and the file path to the playlist.
                        f.write(f'#EXTINF:-1,{os.path.splitext(file)[0]}\n')
                        f.write(file_path + '\n')
    except OSError as e:
        print(f"Error: Could not write to output file '{output_file}': {e}")
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate an .m3u playlist for movies in a directory.')
    parser.add_argument('directory', help='Path to the movie directory on your home server')
    parser.add_argument('--output', default='movies.m3u', help='Name of the output .m3u file (default: movies.m3u)')
    
    args = parser.parse_args()
    create_m3u(args.directory, args.output)
    print(f"Playlist created successfully: {args.output}")
