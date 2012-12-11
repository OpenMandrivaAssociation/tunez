# Mysql information (should be identical to config.inc.php)
my $mysql_dbhost = "localhost";
my $mysql_dbuser = "tunez";
my $mysql_dbpass = "";
my $mysql_dbname = "tunez";

# Assuming you're using Ices v0.3 the only thing you can play are MP3s
my $allowed_filetypes = {'mp3', 1,
                         'ogg', 0};

# Your government type (should be the same as in config.inc.php)
my $government_type = "democracy";  # or socialism

# Your random query type for determining what to play when no songs
# are in the queue.  The "weighted" selection takes into account more
# popular songs while "unweighted" is completely random.
my $random_query_type = "unweighted";

# End Configuration Information

