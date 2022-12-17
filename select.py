import datetime
import sys
from rethinkdb import RethinkDB
r = RethinkDB()


# Definitions
uniqueNumber = 0
skip = 0
limit = 0

# Database size provided before
documentsNumber = int(sys.argv[1])

# One of 6 queries to choose
option = sys.argv[2]

# In case of unique data like unique category, we have to pass uniqueNumber option with an unique number
if option == 'uniqueCategoryAndUniqueTag' or option == 'uniqueCategory':
    uniqueNumber = int(sys.argv[3])

# In case of skip data like pagination, we have to pass skip and limit options
if option == 'skip':
    skip = int(sys.argv[3])
    limit = int(sys.argv[4])

# Connecting to the RethinkDB server
r.connect(host='localhost', port=28015).repl()

# Connecting to the proper database and table for the tests
db = r.db("database{}".format(documentsNumber))
posts_table = db.table('posts')

# Queries
uniqueCategory = r.and_(
    r.row['categories'].contains("Category{}".format(uniqueNumber))
)

nonUniqueCategory = r.and_(
    r.row['categories'].contains('Category')
)

uniqueCategoryAndUniqueTag = r.or_(
    r.row['tags'].contains("Tag{}".format(uniqueNumber)),
    r.row['categories'].contains("Category{}".format(uniqueNumber))
)

nonUniqueCategoriesAndTags = r.or_(
    r.row['tags'].contains('Tag'),
    r.row['categories'].contains('Category')
)

favouritePosts = r.and_(
    r.row['likes']['username'].contains('NormalUser')
)

# Start time of a getting data
now = datetime.datetime.now()

# Getting data
if option == 'skip':
    posts = posts_table.skip(skip).limit(limit).run()
else:
    posts = posts_table.filter(globals()[option]).run()

# End time for getting all of the matched documents
end = str(datetime.datetime.now() - now)

# Just for displaying data
for post in posts:
    print(post)

print("Duration of fetching documents:")
print(end)




