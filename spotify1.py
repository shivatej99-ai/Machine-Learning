"""" Name: Beecharaju Shivateja Depaul ID: 2121964 Date: 05/30/2024
I have not given or received any unauthorized assistance on this assignment """
import pandas as pd

def load_data(artists_path, tracks_path):
    # Load the datasets
    artists_df = pd.read_csv(artists_path, sep='\t')
    tracks_df = pd.read_csv(tracks_path, sep='\t')
    tracks_df['id_artists'] = tracks_df['id_artists'].str.split(', ')
    exploded_tracks = tracks_df.explode('id_artists')
    return artists_df, tracks_df, exploded_tracks

def find_max_followers_artist(artists_df):
    max_followers_artist = artists_df.loc[artists_df['followers'].idxmax()]
    print(f"Artist with the maximum number of followers: {max_followers_artist['name']} - Genres: {max_followers_artist['genres']} - Followers: {max_followers_artist['followers']}")

def find_most_productive_artist(exploded_tracks, artists_df):
    track_counts = exploded_tracks['id_artists'].value_counts()
    most_productive_artist_id = track_counts.idxmax()
    most_productive_artist = artists_df[artists_df['id'] == most_productive_artist_id]
    print(f"Most productive artist: {most_productive_artist['name'].values[0]} - Tracks: {track_counts.max()}")

def summarize_artist_performance(name, artists_df, tracks_df, exploded_tracks):
    artist_id = artists_df[artists_df['name'].str.lower() == name.lower()]['id']
    if artist_id.empty:
        print("Artist not found.")
        return
    artist_id = artist_id.values[0]

    artist_tracks = exploded_tracks[exploded_tracks['id_artists'] == artist_id]
    detailed_tracks = tracks_df[tracks_df['id'].isin(artist_tracks['id'])]

    total_tracks = len(detailed_tracks)
    solo_tracks = detailed_tracks[detailed_tracks['id_artists'].apply(lambda x: len(x) == 1 and x[0] == artist_id)]
    collaborative_tracks = detailed_tracks[detailed_tracks['id_artists'].apply(lambda x: len(x) > 1)]

    avg_popularity_total = detailed_tracks['popularity'].mean()
    avg_popularity_solo = solo_tracks['popularity'].mean() if not solo_tracks.empty else 0
    avg_popularity_collab = collaborative_tracks['popularity'].mean() if not collaborative_tracks.empty else 0

    all_collaborators = set(collaborative_tracks['id_artists'].explode()) - {artist_id}
    num_collaborators = len(all_collaborators)

    print(f"Performance summary for {name}:")
    print(f"Total Tracks: {total_tracks}")
    print(f"Solo Tracks: {len(solo_tracks)}")
    print(f"Collaborative Tracks: {len(collaborative_tracks)}")
    print(f"Average Popularity (Total): {avg_popularity_total}")
    print(f"Average Popularity (Solo): {avg_popularity_solo}")
    print(f"Average Popularity (Collab): {avg_popularity_collab}")
    print(f"Number of Collaborators: {num_collaborators}")

def summarize_all_genres(artists_df):
    # Prepare genres list
    artists_df['genres_list'] = artists_df['genres'].str.split(', ')
    exploded_genres = artists_df.explode('genres_list')
    # Aggregate data for all genres
    all_genre_summary = exploded_genres.groupby('genres_list').agg(
        total_N=('id', 'count'),
        Av_followers=('followers', 'mean')
    ).reset_index().rename(columns={'genres_list': 'genre'})
    return all_genre_summary

def summarize_selected_genres(artists_df, genres):
    # Prepare genres list
    artists_df['genres_list'] = artists_df['genres'].str.split(', ')
    exploded_genres = artists_df.explode('genres_list')
    # Filter and aggregate data for selected genres
    selected_genre_summary = exploded_genres[exploded_genres['genres_list'].isin(genres)].groupby('genres_list').agg(
        total_N=('id', 'count'),
        Av_followers=('followers', 'mean')
    ).reset_index().rename(columns={'genres_list': 'genre'})
    return selected_genre_summary

def get_genre_variants(artists_df, genre):
    artists_df['genres_list'] = artists_df['genres'].str.split(', ')
    exploded_genres = artists_df['genres_list'].explode()
    variants = exploded_genres[exploded_genres.str.contains(genre)].unique()
    print(f"Variants of {genre}:")
    print(variants)

def main():
    artists_path = 'C:/Users/shivateja beecharaju/Downloads/artists.tsv'
    tracks_path = 'C:/Users/shivateja beecharaju/Downloads/tracks.tsv'
    artists_df, tracks_df, exploded_tracks = load_data(artists_path, tracks_path)

    find_max_followers_artist(artists_df)
    find_most_productive_artist(exploded_tracks, artists_df)
    artist_name = input("Enter the artist name to summarize performance: ")
    summarize_artist_performance(artist_name, artists_df, tracks_df, exploded_tracks)
    
    # Print summary for all genres
    all_genre_summary = summarize_all_genres(artists_df)
    print("All genres summary:")
    print(all_genre_summary)

    # Print summary for selected genres
    genres = ["pop", "hip hop", "rock", "metal", "jazz", "blues", "country", "folklore"]
    selected_genre_summary = summarize_selected_genres(artists_df, genres)
    print("Selected genres summary:")
    print(selected_genre_summary)
    
    # Display variants for the genre "jazz"
    get_genre_variants(artists_df, 'jazz')

if __name__ == '__main__':
    main()
