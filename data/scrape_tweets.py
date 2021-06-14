import twint


def search_for_tweets(terms):
    """
    for each element of the terms list, searches for tweets which include this element and saves all in a csv file
    :param terms: list of terms (strings)
    :return: None
    """
    for item in terms:
        print("item", item)
        # configuration
        config = twint.Config()
        config.Search = str(item)
        config.Custom["tweet"] = [
            "id",
            "conversation_id",
            "created_at",
            "date",
            "time",
            "timezone",
            "user_id",
            "username",
            "name",
            "place",
            "tweet",
            "language",
            "mentions",
            "urls",
            "photos",
            "replies_count",
            "retweets_count",
            "likes_count",
            "hashtags",
            "cashtags",
            "link",
            "retweet",
            "quote_url",
            "video",
            "thumbnail",
            "near",
            "geo",
            "user_rt_id",
            "user_rt",
            "source",
            "retweet_date",
            "translate",
            "trans_src",
            "trans_dest"
        ]
        config.Output = str(item) + ".csv"
        config.Store_csv = True
        config.Since = "2021-05-04"
        config.Until = "2021-05-06"
        config.Lang = "en"
        config.Tabs = True

        # running search
        twint.run.Search(config)


if __name__ == "__main__":
    search_for_tweets(["covid"])
