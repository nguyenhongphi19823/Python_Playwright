import requests


def get_crypto_news(crypto_name, api_key):
    """
    Fetch the latest news for a specific cryptocurrency.

    Args:
        crypto_name (str): The name of the cryptocurrency to search for.
        api_key (str): Your NewsAPI API key.

    Returns:
        list: A list of dictionaries containing news details.
    """
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": crypto_name,
        "sortBy": "publishedAt",
        "language": "en",
        "apiKey": api_key
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return articles
    else:
        print(f"Error: Unable to fetch news (Status Code: {response.status_code})")
        return []


def display_news(articles):
    """
    Display news articles in a readable format.

    Args:
        articles (list): List of dictionaries containing news details.
    """
    if not articles:
        print("No news found.")
        return

    print(f"Found {len(articles)} articles:\n")
    for i, article in enumerate(articles, start=1):
        print(f"Article {i}")
        print(f"Title: {article.get('title')}")
        print(f"Author: {article.get('author')}")
        print(f"Source: {article.get('source', {}).get('name')}")
        print(f"Published At: {article.get('publishedAt')}")
        print(f"Description: {article.get('description')}")
        print(f"URL: {article.get('url')}")
        print("-" * 80)


if __name__ == "__main__":
    # Replace with your NewsAPI key
    API_KEY = "4808e7a58e5c489b947a543103ad86d0"
    crypto_name = input("Enter the cryptocurrency name to search for news: ")

    news_articles = get_crypto_news(crypto_name, API_KEY)
    display_news(news_articles)
