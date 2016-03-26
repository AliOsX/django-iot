from django.db import models
import tweepy
import os


class TwitterVote(models.Model):
    # created time
    created_at = models.DateTimeField(auto_now=True)

    # winning choice
    VOTE_CHOICE_LIST = [
        'red', 'orange', 'yellow', 'cyan',
        'green', 'blue', 'purple', 'pink'
    ]
    VOTE_CHOICE_TUPLES = [(x, x) for x in VOTE_CHOICE_LIST]
    winner = models.CharField(max_length=20, choices=VOTE_CHOICE_TUPLES,
                              null=True, blank=True)

    # hashtag for voting
    hashtag = models.CharField(max_length=50, blank=True, null=True)

    # number of total and winning votes
    n_votes_winner = models.IntegerField(default=0)
    n_votes_total = models.IntegerField(default=0)

    # vote tally
    tally = models.CommaSeparatedIntegerField(max_length=50)

    # vote logs
    log = models.TextField(default='')

    # line separator
    LOG_LINE_SEP = '{{{{LINESEP}}}}'

    def collect_votes(self):
        # set up twitter
        auth = tweepy.OAuthHandler(
            os.environ.get('TWITTER_CONSUMER_KEY'),
            os.environ.get('TWITTER_CONSUMER_SECRET'))
        auth.set_access_token(
            os.environ.get('TWITTER_ACCESS_TOKEN'),
            os.environ.get('TWITTER_ACCESS_SECRET'),
        )
        api = tweepy.API(auth)

        # search for hashtag
        results = api.search(q=self.hashtag, rpp=100)

        # collect votes
        vote_counts = {choice: 0 for choice in self.VOTE_CHOICE_LIST}
        log_entries = []
        for tweet in results:
            for choice in self.VOTE_CHOICE_LIST:
                if choice in tweet.text:
                    # increment vote
                    vote_counts[choice] += 1

                    # store log
                    log_entry = 'at %s @%s voted for %s\n%s' % (
                        tweet.created_at, tweet.user.screen_name,
                        choice, tweet.text
                    )
                    log_entries.append(log_entry)

        # store winner and tallies
        self.winner, self.n_votes_winner = max(vote_counts.iteritems(), key=lambda x: x[1])
        self.n_votes_total = sum(vote_counts.values())
        self.tally = ','.join([str(vote_counts[choice]) for choice in self.VOTE_CHOICE_LIST])
        self.log = self.LOG_LINE_SEP.join(log_entries)

        # save
        self.save()

        # return winner and winning fraction
        try:
            return self.winner, self.n_votes_winner / float(self.n_votes_total)
        except ZeroDivisionError:
            return None, None
