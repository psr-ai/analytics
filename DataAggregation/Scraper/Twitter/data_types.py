class LiveStreamUserQuery:

    def __init__(self, query=None, type=None):
        self.query = query
        self.type = type


class TweepyStreamQuery:

    def __init__(self, LiveStreamUserQueries, languages=['en'], API=None):
        self.languages = languages
        self.API = API
        self.track = []
        self.locations = []
        self.follow = []

        for query in LiveStreamUserQueries:
            if query.query is not None and query.type is not None:

                if query.type is 'track':
                    if query.query.replace(' ', ''):
                        self.track.append(query.query)
                    else:
                        raise Exception('Query cannot be an empty string.')

                elif query.type is 'locations':
                    for elem in query.query:
                        self.locations.append(elem)

                elif query.type is 'follow':
                    self.follow.append(str(API.get_user(query.query).id))

                else:
                    raise Exception('Cannot decipher the query type.')

            else:
                raise Exception('Query cannot be None type.')



