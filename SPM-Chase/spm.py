import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
from collections import defaultdict, Counter
import os
import sys

class SpotifyPlaylistManager:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, username=None):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.analyzed_path = os.path.join(self.base_path, "Analyzed")
        self.duplicates_path = os.path.join(self.base_path, "Duplicates")
        self.playlist_path = os.path.join(self.base_path, "Playlist")
        self.cache_path = os.path.join(self.base_path, "cache")
        
        for path in [self.analyzed_path, self.duplicates_path, self.playlist_path, self.cache_path]:
            os.makedirs(path, exist_ok=True)
            print(f"📁 Directory ready: {path}")
        
        if client_id and client_secret and username:
            self.initialize_spotify(client_id, client_secret, redirect_uri, username)
    
    def ensure_directories(self):
        """Create output directories if they don't exist"""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.analyzed_path = os.path.join(self.base_path, "Analyzed")
        self.duplicates_path = os.path.join(self.base_path, "Duplicates")
        self.playlist_path = os.path.join(self.base_path, "Playlist")
        self.cache_path = os.path.join(self.base_path, "cache")
        
        for path in [self.analyzed_path, self.duplicates_path, self.playlist_path, self.cache_path]:
            os.makedirs(path, exist_ok=True)
            print(f"📁 Directory ready: {path}")
    
    def get_playlist_from_url(self, playlist_url):
        """Extract playlist ID from Spotify URL"""
        try:
            if "playlist/" in playlist_url:
                playlist_id = playlist_url.split("playlist/")[1].split("?")[0]
                print(f"✅ Extracted playlist ID: {playlist_id}")
                return playlist_id
            print("❌ Invalid playlist URL format")
            return None
        except Exception as e:
            print(f"❌ Error parsing playlist URL: {e}")
            return None

    
    def analyze_playlist(self, playlist_id, output_file="playlist_analysis.txt"):
        """Analyze playlist and create detailed report"""
        try:
            print("🔄 Analyzing playlist...")
            
            playlist_info = self.sp.playlist(playlist_id)
            playlist_name = playlist_info['name']
            print(f"📋 Playlist: {playlist_name}")
            
            tracks = self.get_all_playlist_tracks(playlist_id)
            
            if not tracks:
                print("❌ No tracks found in playlist")
                return False
            
            print(f"📊 Found {len(tracks)} tracks, analyzing...")
            
            artist_songs = defaultdict(list)
            artist_counts = Counter()
            total_tracks = 0
            duplicates = defaultdict(list)
            track_ids = defaultdict(list)
            
            for i, item in enumerate(tracks):
                try:
                    if item['track'] and item['track']['id']:
                        track_id = item['track']['id']
                        track_name = item['track']['name']
                        artist_name = item['track']['artists'][0]['name'] if item['track']['artists'] else 'Unknown'
                        
                        artist_songs[artist_name].append(track_name)
                        artist_counts[artist_name] += 1
                        total_tracks += 1
                        
                        track_key = f"{artist_name} - {track_name}"
                        track_ids[track_id].append({
                            'position': i + 1,
                            'artist': artist_name,
                            'song': track_name
                        })
                        
                        if len(track_ids[track_id]) > 1:
                            duplicates[track_key] = track_ids[track_id]
                except Exception as e:
                    print(f"⚠️ Error processing track {i}: {e}")
                    continue
            
            try:
                if not os.path.isabs(output_file):
                    output_file = os.path.join(self.analyzed_path, output_file)
                
                output_file = self.get_unique_filename(output_file)
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write("="*80 + "\n")
                    f.write(f"SPOTIFY PLAYLIST ANALYSIS REPORT\n")
                    f.write("="*80 + "\n")
                    f.write(f"Playlist: {playlist_name}\n")
                    f.write(f"Total Tracks: {total_tracks}\n")
                    f.write(f"Unique Artists: {len(artist_counts)}\n")
                    f.write(f"Duplicate Tracks: {len(duplicates)}\n")
                    f.write(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("="*80 + "\n\n")
                    
                    f.write("ARTIST BREAKDOWN (sorted by song count)\n")
                    f.write("-"*50 + "\n")
                    for artist, count in artist_counts.most_common():
                        f.write(f"{artist}: {count} songs\n")
                    f.write("\n")
                    
                    f.write("DETAILED SONG LIST BY ARTIST\n")
                    f.write("-"*50 + "\n")
                    for artist in sorted(artist_songs.keys()):
                        f.write(f"\n{artist} ({len(artist_songs[artist])} songs):\n")
                        for i, song in enumerate(sorted(artist_songs[artist]), 1):
                            f.write(f"  {i:2d}. {song}\n")
                    
                    if duplicates:
                        f.write("\n" + "="*80 + "\n")
                        f.write("DUPLICATE TRACKS FOUND\n")
                        f.write("="*80 + "\n")
                        for track, positions in duplicates.items():
                            f.write(f"\n{track}:\n")
                            for pos_info in positions:
                                f.write(f"  Position {pos_info['position']}\n")
                    else:
                        f.write("\n" + "="*80 + "\n")
                        f.write("NO DUPLICATE TRACKS FOUND\n")
                        f.write("="*80 + "\n")
                    
                    f.write("\n" + "="*80 + "\n")
                    f.write("SUMMARY STATISTICS\n")
                    f.write("="*80 + "\n")
                    f.write(f"Total Artists: {len(artist_counts)}\n")
                    f.write(f"Total Songs: {total_tracks}\n")
                    if len(artist_counts) > 0:
                        f.write(f"Average Songs per Artist: {total_tracks/len(artist_counts):.1f}\n")
                        f.write(f"Most Songs by Single Artist: {max(artist_counts.values())}\n")
                        f.write(f"Artist with Most Songs: {artist_counts.most_common(1)[0][0]}\n")
                    f.write(f"Duplicate Tracks: {len(duplicates)}\n")
                    
                    f.write(f"\nTOP 10 ARTISTS BY SONG COUNT:\n")
                    for i, (artist, count) in enumerate(artist_counts.most_common(10), 1):
                        f.write(f"{i:2d}. {artist}: {count} songs\n")
                
                print(f"✅ Analysis complete! Report saved to: {output_file}")
                return True
                
            except Exception as e:
                print(f"❌ Error writing analysis file: {e}")
                return False
            
        except Exception as e:
            print(f"❌ Error analyzing playlist: {e}")
            return False
    
    def search_track(self, artist, song):
        try:
            song_clean = song.split(',')[0].strip() if ',' in song else song.strip()
            artist_clean = artist.strip()
            
            query = f"artist:\"{artist_clean}\" track:\"{song_clean}\""
            results = self.sp.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                return results['tracks']['items'][0]['id']
            
            query = f"artist:{artist_clean} track:{song_clean}"
            results = self.sp.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                return results['tracks']['items'][0]['id']
            
            query = f"{artist_clean} {song_clean}"
            results = self.sp.search(q=query, type='track', limit=1)
            
            if results['tracks']['items']:
                return results['tracks']['items'][0]['id']
                
            return None
            
        except Exception as e:
            print(f"⚠️ Search error for {artist} - {song}: {e}")
            return None
    
    def get_or_create_playlist(self, playlist_name):
        try:
            print(f"🔍 Looking for playlist: '{playlist_name}'")
            
            playlists = []
            results = self.sp.current_user_playlists()  
            playlists.extend(results['items'])
            
            while results['next']:
                results = self.sp.next(results)
                playlists.extend(results['items'])
            
            print(f"📋 Found {len(playlists)} total playlists")
            
            for playlist in playlists:
                if playlist['name'] == playlist_name:
                    print(f"✅ Found existing playlist: '{playlist_name}'")
                    return playlist['id']
            
            print(f"🆕 Creating new playlist: '{playlist_name}'")
            playlist = self.sp.user_playlist_create(
                self.actual_user_id, 
                playlist_name, 
                public=False,
                description="Playlist created by Chase's Spotify Playlist Manager"
            )
            print(f"✅ Created new playlist: '{playlist_name}'")
            return playlist['id']
            
        except Exception as e:
            print(f"❌ Error with playlist: {e}")
            return None
    
    def get_all_playlist_tracks(self, playlist_id):
        try:
            print("🔄 Getting playlist tracks...")
            tracks = []
            results = self.sp.playlist_tracks(playlist_id)
            tracks.extend(results['items'])
            
            while results['next']:
                results = self.sp.next(results)
                tracks.extend(results['items'])
            
            print(f"✅ Retrieved {len(tracks)} tracks")
            return tracks
        except Exception as e:
            print(f"❌ Error getting playlist tracks: {e}")
            return []
    
    def add_tracks_to_playlist(self, playlist_id, track_ids):
        try:
            print(f"🔄 Adding {len(track_ids)} tracks to playlist...")
            added_count = 0
            batch_size = 100
            
            for i in range(0, len(track_ids), batch_size):
                batch = track_ids[i:i + batch_size]
                self.sp.playlist_add_items(playlist_id, batch)
                added_count += len(batch)
                print(f"✅ Added batch of {len(batch)} tracks (Total: {added_count}/{len(track_ids)})")
                time.sleep(0.1)
            
            return added_count
        except Exception as e:
            print(f"❌ Error adding tracks: {e}")
            return 0
    
    def remove_duplicates_from_playlist(self, playlist_id, create_report=True):
        try:
            print("🔄 Scanning playlist for duplicates...")
            tracks = self.get_all_playlist_tracks(playlist_id)
            
            if not tracks:
                print("❌ No tracks found in playlist")
                return 0
            
            playlist_info = self.sp.playlist(playlist_id)
            playlist_name = playlist_info['name']
            
            track_occurrences = defaultdict(list)
            
            for i, item in enumerate(tracks):
                try:
                    if item['track'] and item['track']['id']:
                        track_id = item['track']['id']
                        track_name = item['track']['name']
                        artist_name = item['track']['artists'][0]['name'] if item['track']['artists'] else 'Unknown'
                        
                        track_occurrences[track_id].append({
                            'position': i,
                            'name': track_name,
                            'artist': artist_name
                        })
                except Exception as e:
                    print(f"⚠️ Error processing track {i}: {e}")
                    continue
            
            duplicates_to_remove = []
            duplicate_report = []
            
            for track_id, occurrences in track_occurrences.items():
                if len(occurrences) > 1:
                    print(f"🔍 Found {len(occurrences)} copies of: {occurrences[0]['artist']} - {occurrences[0]['name']}")
                    duplicate_report.append({
                        'artist': occurrences[0]['artist'],
                        'song': occurrences[0]['name'],
                        'count': len(occurrences),
                        'positions': [occ['position'] + 1 for occ in occurrences]
                    })
                    
                    for occurrence in occurrences[1:]:
                        duplicates_to_remove.append({
                            'uri': f"spotify:track:{track_id}",
                            'positions': [occurrence['position']]
                        })
            
            if create_report and duplicate_report:
                try:
                    report_file = f"duplicates_removed_{playlist_name.replace(' ', '_').replace('/', '_')}.txt"
                    report_file = os.path.join(self.duplicates_path, report_file)
                    report_file = self.get_unique_filename(report_file)
                    with open(report_file, 'w', encoding='utf-8') as f:
                        f.write("="*80 + "\n")
                        f.write(f"DUPLICATE TRACKS REMOVAL REPORT\n")
                        f.write("="*80 + "\n")
                        f.write(f"Playlist: {playlist_name}\n")
                        f.write(f"Total Duplicates Found: {len(duplicate_report)}\n")
                        f.write(f"Total Duplicate Tracks Removed: {len(duplicates_to_remove)}\n")
                        f.write(f"Removal Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                        f.write("="*80 + "\n\n")
                        
                        for dup in duplicate_report:
                            f.write(f"{dup['artist']} - {dup['song']}\n")
                            f.write(f"  Found {dup['count']} copies at positions: {', '.join(map(str, dup['positions']))}\n")
                            f.write(f"  Kept: Position {dup['positions'][0]}\n")
                            f.write(f"  Removed: Positions {', '.join(map(str, dup['positions'][1:]))}\n\n")
                    
                    print(f"📄 Duplicate report saved to: {report_file}")
                except Exception as e:
                    print(f"⚠️ Error saving duplicate report: {e}")
            
            if not duplicates_to_remove:
                print("✅ No duplicates found!")
                return 0
            
            print(f"🗑️ Removing {len(duplicates_to_remove)} duplicate tracks...")
            
            duplicates_to_remove.sort(key=lambda x: x['positions'][0], reverse=True)
            
            removed_count = 0
            for duplicate in duplicates_to_remove:
                try:
                    self.sp.playlist_remove_specific_occurrences_of_items(playlist_id, [duplicate])
                    removed_count += 1
                    
                    if removed_count % 10 == 0:
                        print(f"🗑️ Removed {removed_count}/{len(duplicates_to_remove)} duplicates...")
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"⚠️ Error removing duplicate: {e}")
            
            print(f"✅ Successfully removed {removed_count} duplicate tracks!")
            return removed_count
            
        except Exception as e:
            print(f"❌ Error removing duplicates: {e}")
            return 0
    
    def process_csv_file(self, csv_file_path, playlist_name):
        try:
            print(f"📁 Checking CSV file: {csv_file_path}")
            if not os.path.exists(csv_file_path):
                print(f"❌ CSV file not found: {csv_file_path}")
                return False
            
            print(f"📊 Reading CSV file...")
            
            try:
                with open(csv_file_path, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            
                filtered_lines = []
                comment_count = 0
                for line in lines:
                    stripped_line = line.strip()
                    if stripped_line.startswith('#') or stripped_line == '':
                        comment_count += 1
                        continue  
                    filtered_lines.append(line)
            
                print(f"📝 Filtered out {comment_count} comment/empty lines")
            
                from io import StringIO
                csv_content = ''.join(filtered_lines)
                df = pd.read_csv(StringIO(csv_content))
            
            except Exception as e:
                print(f"⚠️ CSV parsing error: {e}")
                print("⚠️ Trying alternative method...")
                df = pd.read_csv(csv_file_path, on_bad_lines='skip')
                if 'Artist' in df.columns:
                    original_count = len(df)
                    df = df[~df['Artist'].astype(str).str.strip().str.startswith('#')]
                    df = df[df['Artist'].astype(str).str.strip() != '']
                    df = df[df['Song'].astype(str).str.strip() != '']
                    filtered_count = original_count - len(df)
                    print(f"📝 Filtered out {filtered_count} comment/empty rows from dataframe")
            
            print(f"📋 CSV Info:")
            print(f"  Rows: {len(df)}")
            print(f"  Columns: {list(df.columns)}")
            
            if 'Artist' not in df.columns or 'Song' not in df.columns:
                print("❌ Error: CSV must have 'Artist' and 'Song' columns")
                return False
            
            playlist_id = self.get_or_create_playlist(playlist_name)
            if not playlist_id:
                print("❌ Failed to create/get playlist")
                return False
            
            print(f"\n🔍 Searching for {len(df)} tracks on Spotify...")
            track_ids = []
            not_found = []
            
            for index, row in df.iterrows():
                try:
                    artist = str(row['Artist']).strip()
                    song = str(row['Song']).strip()
                    
                    if artist.startswith('#') or song.startswith('#'):
                        continue
                    
                    if not artist or not song or artist == 'nan' or song == 'nan':
                        continue
                    
                    track_id = self.search_track(artist, song)
                    if track_id:
                        track_ids.append(track_id)
                        if len(track_ids) % 10 == 0:
                            print(f"✅ Found {len(track_ids)} tracks so far...")
                    else:
                        not_found.append(f"{artist} - {song}")
                    
                    time.sleep(0.1)
                    
                except Exception as e:
                    print(f"⚠️ Error processing row {index}: {e}")
                    continue
            
            print(f"\n📊 Search Results:")
            print(f"  ✅ Found: {len(track_ids)} tracks")
            print(f"  ❌ Not found: {len(not_found)} tracks")
            
            if not_found:
                try:
                    not_found_file = f"not_found_tracks_{playlist_name.replace(' ', '_').replace('/', '_')}.txt"
                    not_found_file = os.path.join(self.playlist_path, not_found_file)
                    not_found_file = self.get_unique_filename(not_found_file)
                    with open(not_found_file, 'w', encoding='utf-8') as f:
                        f.write("TRACKS NOT FOUND ON SPOTIFY\n")
                        f.write("="*50 + "\n")
                        f.write(f"Playlist: {playlist_name}\n")
                        f.write(f"Total not found: {len(not_found)}\n")
                        f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                        
                        for track in not_found:
                            f.write(f"{track}\n")
                    
                    print(f"📄 Not found tracks saved to: {not_found_file}")
                except Exception as e:
                    print(f"⚠️ Error saving not found tracks: {e}")
            
            if track_ids:
                added_count = self.add_tracks_to_playlist(playlist_id, track_ids)
                
                print("\n🧹 Removing duplicates...")
                removed_count = self.remove_duplicates_from_playlist(playlist_id, create_report=True)
                
                print("\n📊 Creating playlist analysis...")
                analysis_file = f"playlist_analysis_{playlist_name.replace(' ', '_').replace('/', '_')}.txt"
                analysis_file = os.path.join(self.analyzed_path, analysis_file)
                analysis_file = self.get_unique_filename(analysis_file)
                self.analyze_playlist(playlist_id, analysis_file)
                
                print(f"\n🎉 Process complete!")
                print(f"   ✅ Added: {added_count} tracks")
                print(f"   🗑️ Removed duplicates: {removed_count}")
                print(f"   ❌ Not found: {len(not_found)}")
                
                return True
            else:
                print("❌ No tracks found to add!")
                return False
                
        except Exception as e:
            print(f"❌ Error processing CSV: {e}")
            return False

    def save_credentials(self, client_id, client_secret, username):
        """Save credentials to cache file"""
        try:
            credentials = {
                'client_id': client_id,
                'client_secret': client_secret,
                'username': username,
                'saved_date': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            cred_file = os.path.join(self.cache_path, 'spotify_credentials.json')
            with open(cred_file, 'w') as f:
                import json
                json.dump(credentials, f, indent=2)
            print(f"💾 Credentials saved to cache")
            return True
        except Exception as e:
            print(f"⚠️ Could not save credentials: {e}")
            return False

    def load_credentials(self):
        """Load credentials from cache file"""
        try:
            cred_file = os.path.join(self.cache_path, 'spotify_credentials.json')
            if os.path.exists(cred_file):
                with open(cred_file, 'r') as f:
                    import json
                    credentials = json.load(f)
                print(f"📋 Found cached credentials from {credentials.get('saved_date', 'unknown date')}")
                return credentials
            return None
        except Exception as e:
            print(f"⚠️ Could not load cached credentials: {e}")
            return None

    def get_unique_filename(self, filepath):
        """Generate unique filename if file already exists"""
        if not os.path.exists(filepath):
            return filepath
        
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)
        
        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_filepath = os.path.join(directory, new_filename)
            if not os.path.exists(new_filepath):
                print(f"📝 File exists, using: {new_filename}")
                return new_filepath
            counter += 1

    def initialize_spotify(self, client_id, client_secret, redirect_uri, username):
        """Initialize Spotify connection with credentials"""
        try:
            print("🔄 Initializing Spotify connection...")
            self.username = username
            self.scope = "playlist-modify-public playlist-modify-private playlist-read-private"
            
            cache_file = os.path.join(self.cache_path, f".cache-{username}")
            
            self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope=self.scope,
                username=username,
                cache_path=cache_file
            ))
            
            user = self.sp.current_user()
            self.actual_user_id = user['id']
            display_name = user.get('display_name', 'N/A')
            
            print(f"✅ Connected as: {display_name} ({self.actual_user_id})")
            
            self.save_credentials(client_id, client_secret, username)
            return True
            
        except Exception as e:
            print(f"❌ Failed to connect to Spotify: {e}")
            return False

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import spotipy
        import pandas
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install spotipy pandas")
        return False

def main():
    print("🎵 SPOTIFY PLAYLIST MANAGER")
    print("="*60)
    
    if not check_dependencies():
        return
    
    print("\nWhat would you like to do?")
    print("1. Create playlist from CSV file")
    print("2. Analyze existing playlist from URL")
    print("3. Remove duplicates from existing playlist")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice not in ['1', '2', '3']:
            print("❌ Invalid choice! Please enter 1, 2, or 3")
            return
        
        manager = SpotifyPlaylistManager()
        
        cached_creds = manager.load_credentials()
        
        if cached_creds:
            print(f"🔄 Trying cached credentials for user: {cached_creds['username']}")
            try:
                redirect_uri = "http://127.0.0.1:8080/callback"
                success = manager.initialize_spotify(
                    cached_creds['client_id'],
                    cached_creds['client_secret'],
                    redirect_uri,
                    cached_creds['username']
                )
                
                if not success:
                    raise Exception("Cached credentials failed")
                    
            except Exception as e:
                print(f"⚠️ Cached credentials failed: {e}")
                print("🔄 Please enter credentials manually...")
                cached_creds = None
        
        if not cached_creds:
            print("\n" + "="*60)
            print("SPOTIFY API SETUP")
            print("="*60)
            print("You need Spotify API credentials:")
            print("1. Go to https://developer.spotify.com/dashboard")
            print("2. Create a new app")
            print("3. Add 'http://127.0.0.1:8080/callback' as redirect URI")
            print("4. Copy your Client ID and Client Secret")
            
            client_id = input("\nSpotify Client ID: ").strip()
            if not client_id:
                print("❌ Client ID is required!")
                return
                
            client_secret = input("Spotify Client Secret: ").strip()
            if not client_secret:
                print("❌ Client Secret is required!")
                return
                
            username = input("Spotify Username: ").strip()
            if not username:
                print("❌ Username is required!")
                return
            
            redirect_uri = "http://127.0.0.1:8080/callback"
            
            print(f"\n🔄 Connecting to Spotify...")
            success = manager.initialize_spotify(client_id, client_secret, redirect_uri, username)
            
            if not success:
                print("❌ Failed to connect with provided credentials!")
                return
        
        if choice == '1':
            csv_file_path = input("\nEnter CSV file path (or press Enter for 'csv/example.csv'): ").strip()
            if not csv_file_path:
                csv_file_path = os.path.join("csv", "example.csv")
            
            playlist_name = input("Enter playlist name (or press Enter for 'My Playlist'): ").strip()
            if not playlist_name:
                playlist_name = "My Playlist"
            
            success = manager.process_csv_file(csv_file_path, playlist_name)
            
        elif choice == '2':
            playlist_url = input("\nEnter Spotify playlist URL: ").strip()
            if not playlist_url:
                print("❌ Playlist URL is required!")
                return
            
            playlist_id = manager.get_playlist_from_url(playlist_url)
            if not playlist_id:
                print("❌ Invalid playlist URL!")
                return
            
            output_file = input("Enter output file name (or press Enter for 'playlist_analysis.txt'): ").strip()
            if not output_file:
                output_file = "playlist_analysis.txt"
            
            success = manager.analyze_playlist(playlist_id, output_file)
            
        elif choice == '3':
            playlist_url = input("\nEnter Spotify playlist URL: ").strip()
            if not playlist_url:
                print("❌ Playlist URL is required!")
                return
            
            playlist_id = manager.get_playlist_from_url(playlist_url)
            if not playlist_id:
                print("❌ Invalid playlist URL!")
                return
            
            print("\n🔄 Analyzing and removing duplicates...")
            removed_count = manager.remove_duplicates_from_playlist(playlist_id, create_report=True)
            
            print("\n📊 Creating analysis report...")
            analysis_file = "playlist_analysis_after_cleanup.txt"
            manager.analyze_playlist(playlist_id, analysis_file)
            
            success = True
            print(f"\n✅ Removed {removed_count} duplicate tracks!")
        
        if success:
            print(f"\n🎉 Operation completed successfully!")
        else:
            print(f"\n❌ Operation failed!")
            
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please check your internet connection and API credentials.")

if __name__ == "__main__":
    main()