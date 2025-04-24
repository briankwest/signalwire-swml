from signalwire import SignalWireSWML
from signalwire_pom import PromptObjectModel
from jsonschema import validate, ValidationError

def build_moviebot_prompt():
    pom = PromptObjectModel()
    # Overview section
    overview = pom.add_section("Overview", body="You are a movie expert AI assistant capable of providing detailed information about movies, directors, actors, genres, and personalized recommendations.")
    overview.add_bullets([
        "You have access to the following functions to retrieve up-to-date movie data."
    ])

    # Functions section
    functions = pom.add_section("Available Functions")
    functions.add_bullets([
        "**search_movie**: Search for movies by title. Parameters: query, language (default: \"en-US\")",
        "**get_movie_details**: Retrieve detailed information about a movie. Parameters: movie_id, language (default: \"en-US\")",
        "**discover_movies**: Discover movies by different criteria. Parameters: with_genres, primary_release_year, sort_by (default: \"popularity.desc\"), language (default: \"en-US\")",
        "**get_trending_movies**: Retrieve a list of movies that are currently trending. Parameters: time_window (default: \"week\"), language (default: \"en-US\")",
        "**get_movie_recommendations**: Get recommendations based on a specific movie. Parameters: movie_id, language (default: \"en-US\")",
        "**get_movie_credits**: Retrieve cast and crew information for a movie. Parameters: movie_id, language (default: \"en-US\")",
        "**get_person_details**: Retrieve detailed information about a person. Parameters: person_id, language (default: \"en-US\"), append_to_response",
        "**get_genre_list**: Retrieve the list of official genres. Parameters: language (default: \"en-US\")",
        "**get_upcoming_movies**: Retrieve movies that are soon to be released. Parameters: language (default: \"en-US\"), region",
        "**get_now_playing_movies**: Retrieve movies currently playing in theaters. Parameters: language (default: \"en-US\"), region",
        "**get_similar_movies**: Retrieve movies similar to a specified movie. Parameters: movie_id, language (default: \"en-US\")",
        "**multi_search**: Search for movies, TV shows, and people with a single query. Parameters: query, language (default: \"en-US\")"
    ])

    # Guidelines section
    guidelines = pom.add_section("Guidelines")
    guidelines.add_bullets([
        "Always provide accurate and helpful information.",
        "Use the latest data from the functions whenever possible.",
        "Maintain a conversational and friendly tone.",
        "Respect user preferences and provide personalized recommendations.",
        "Adhere to OpenAI's policies and avoid disallowed content."
    ])

    # Example section
    example = pom.add_section("Example")
    example.add_bullets([
        'User: "Can you recommend a good sci-fi movie from last year?"',
        "Assistant:",
        "  1. Use `discover_movies` with `with_genres` set to the genre ID for sci-fi and `primary_release_year` set to last year.",
        "  2. Fetch the list of movies.",
        "  3. Recommend a movie from the list with a brief description."
    ])

    return pom.to_dict()

def build_movie_ai_agent():
    swml = SignalWireSWML(version="1.0.0")

    # Add standard applications
    swml.add_application("main", "answer")
    swml.add_application("main", "record_call", {
        "format": "wav",
        "stereo": True
    })

    # Set up SWAIG defaults and includes
    swml.add_aiswaigdefaults({
        "web_hook_url": "https://botworks/swaig/1/11"
    })
    swml.add_aiinclude({
        "url": "https://moviebot/swaig",
        "functions": [
            "search_movie",
            "get_movie_details",
            "discover_movies",
            "get_trending_movies",
            "get_movie_recommendations",
            "get_genre_list",
            "get_upcoming_movies",
            "get_similar_movies",
            "get_now_playing_movies",
            "multi_search",
            "get_person_detail",
            "get_movie_credits"
        ]
    })

    # Set AI language
    swml.add_ailanguage({
        "code": "en-US",
        "name": "English",
        "voice": "openai.alloy"
    })

    # Set AI params
    swml.add_aiparams({
        "debug_webhook_level": 1,
        "debug_webhook_url": "https://botworks/debugwebhook/1/11"
    })

    # Set AI post prompt
    swml.set_aipost_prompt({
        "temperature": 0.5,
        "text": "Summarize the conversation including all the details that were discussed.",
        "top_p": 0.5
    })

    # Set AI post prompt URL
    swml.set_aipost_prompt_url({
        "post_prompt_url": "https://botworks/postprompt/1/11"
    })

    # Set AI prompt using POM
    swml.set_aiprompt({
        "temperature": 0.5,
        "pom": build_moviebot_prompt(),
        "top_p": 0.5
    })

    # Add the AI application to the main section
    swml.add_aiapplication("main")

    # Output as JSON or YAML
    output_json = swml.render_json(ordered=True)
    print(output_json)
    # print(swml.render_yaml(ordered=True))  # Uncomment for YAML output

    # --- Schema Validation ---
    try:
        import json
        # Load schema from file (adjust path as needed)
        with open('SWMLObject.json') as schema_file:
            schema = json.load(schema_file)
        data = json.loads(output_json)
        validate(instance=data, schema=schema)
        print("\nSchema validation: SUCCESS")
    except FileNotFoundError:
        print("\nSchema file 'schema.json' not found. Skipping validation.")
    except ValidationError as e:
        print("\nSchema validation: FAILED\n", e)

if __name__ == "__main__":
    build_movie_ai_agent()