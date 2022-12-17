from rethinkdb import RethinkDB
r = RethinkDB()
import sys
import datetime

# To achieve reliable test results I encourage you to run tests for different database's size, like 10, 100, 1000 etc.
documentsNumber = int(sys.argv[1])

# Connecting to the RethinkDB server
r.connect(host='localhost', port=28015).repl()

# We create a suitable database and table for running various tests
# Create the "test" database if it does not exist
#try
r.db_create("database{}".format(documentsNumber)).run()
db = r.db("database{}".format(documentsNumber))


db.table_create('posts').run()
posts_table = db.table('posts')

# Start time of all insertions
start = datetime.datetime.now()

for i in range(0, documentsNumber):
    # Start time of a single insertion
    now = datetime.datetime.now()

    post = {
        "title": "Title{}".format(i),
        "content": "Content{}".format(i),
        "tags": ["Tag", "Tag{}".format(i)],
        "created": r.now(),
        "categories": ["Category", "Category{}".format(i)],
        "likes": [
            {
                "username": "NormalUser"
            }
        ],
        "comments": [
            {
                "username": "NormalUser",
                "text": "Text{}".format(i)
            }
        ]
    }
    posts_table.insert(post).run()

    # Duration of a single insertion
    print(str(datetime.datetime.now() - now))

# End time for inserting all of the documents
end = datetime.datetime.now()

print("Duration of all insertions:")
print(str(end - start))
