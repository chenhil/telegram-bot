from plexapi.myplex import MyPlexAccount

class PlexAPI():
    def __init__(self):
        self.movies = []
        self.shows = []
        account = MyPlexAccount('twannie@hellngo.com', 'Password123')
        self.plex = account.resource('PlexDocker').connect()  # returns a PlexServer instance
        self.getRecentlyAdded()

    def getRecentlyAdded(self):
        for item in self.plex.library.section("TV Shows").recentlyAdded()[:5]:
            self.shows.append("• " + item.episodes()[-1].grandparentTitle + " " +item.episodes()[-1].seasonEpisode)

        for item in self.plex.library.section("Movies").recentlyAdded()[:5]:
            self.movies.append("• " + item.title)

    def getMarkdown(self):
        return (str("```") + "\n"
        + "Recently Added Movies\n"
        + '\n'.join([str(elem) for elem in self.movies]) 
        + "\n\nRecently Added TV Shows\n"
        + '\n'.join([str(elem) for elem in self.shows]) 
        + "\n " + str("```"))