

import praw
import csv
from tqdm import tqdm

reddit = praw.Reddit(
    client_id='cg56VO7TfnaKaa8YIlMdWg',
    client_secret='CgNyU2cp-7bblO0g2jmEtHdHlH-PGw',
    user_agent='Designer_Dealer_3310-Deep-Movie-characterization'
)

# List of top movie-related subreddits
subreddits = [
    'movies', 'TrueFilm', 'Letterboxd', 'Film', 'MovieSuggestions', 'BoxOffice', 'MovieDetails', 'ClassicFilms',
    'Documentaries', 'NetflixBestOf', 'Netflix', 'DisneyPlus', 'HorrorMovies', 'ActionMovies', 'ComedyMovies',
    'AnimatedMovies', 'ScienceFiction', 'Marvel', 'DC_Cinematic', 'StarWars', 'StarTrek', 'IndianCinema',
    'AnimeMovies', 'ForeignMovies', 'Shortfilms', 'IndieFilm', 'FilmNoir', 'Westerns', '80sMovies', '90sMovies',
    '2000sMovies', 'ClassicMovieReviews', 'BestOfStreamingVideo', 'MoviesCirclejerk', 'BadMovies', 'UnderratedMovies',
    'ObscureMovies', 'DocumentaryFilms', 'FilmCriticism', 'FilmMakers', 'Screenwriting', 'Directors', 'Actors',
    'Actress', 'FilmMusic', 'FilmPhotography', 'FilmTheory', 'FilmEditing', 'FilmProduction', 'FilmFestival',
    'FilmScores', 'FilmPosters', 'FilmTrivia', 'FilmHistory', 'FilmDiscussion', 'FilmCameras', 'FilmRestoration'
]

# List of villain-related keywords and names
keywords_list = [
    'villain', 'antagonist', 'evil', 'bad guy', 'nemesis', 'antihero', 'dark character', 'mastermind', 'criminal', 'adversary',
    'Joker', 'Darth Vader', 'Thanos', 'Loki', 'Killmonger', 'Magneto', 'Hannibal Lecter', 'Voldemort', 'Sauron', 'Kylo Ren',
    'Green Goblin', 'Norman Bates', 'Scar', 'Agent Smith', 'Bane', 'Palpatine', 'Maleficent', 'Ursula', 'Jigsaw', 'Pennywise',
    'Freddy Krueger', 'Michael Myers', 'Jason Voorhees', 'Gollum', 'T-1000', 'Hans Gruber', 'Commodus', 'Patrick Bateman',
    'Annie Wilkes', 'Lord Farquaad', 'Syndrome', 'Hades', 'Dr. Octopus', 'Red Skull', 'Mystique', 'The Governor',
    'Ramsay Bolton', 'Cersei Lannister', 'Joffrey Baratheon', 'Dolores Umbridge', 'Bellatrix Lestrange', 'The Wicked Witch',
    'Count Dracula', 'The Queen', 'Captain Hook', 'Cruella de Vil', 'The Riddler', 'Two-Face', 'Catwoman', 'Lex Luthor',
    'General Zod', 'Sabretooth'
]


comments = []
total_tasks = len(subreddits) * len(keywords_list)
task_count = 0

for subreddit_name in tqdm(subreddits, desc="Subreddits", position=0):
    print(f"Starting subreddit: {subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    for keyword in tqdm(keywords_list, desc=f"Keywords in {subreddit_name}", leave=False, position=1):
        print(f"  Searching for keyword: '{keyword}' in subreddit: {subreddit_name}")
        task_count += 1
        try:
            for submission in subreddit.search(keyword, limit=50):
                submission.comments.replace_more(limit=0)
                for comment in submission.comments.list():
                    comments.append(comment.body)
            print(f"  Finished keyword: '{keyword}' in subreddit: {subreddit_name}")
        except Exception as e:
            print(f"Error in subreddit {subreddit_name} with keyword '{keyword}': {e}")
        print(f"Progress: {task_count}/{total_tasks} tasks completed. Comments collected: {len(comments)}")
    print(f"Completed subreddit: {subreddit_name}")

# Save all comments to CSV (append mode)
with open('data/joker_comments.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    # Only write header if file is empty
    if f.tell() == 0:
        writer.writerow(['comment'])
    for c in comments:
        writer.writerow([c])

print(f"Saved {len(comments)} comments to villian_comments.csv")