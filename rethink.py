from rethinkdb import RethinkDB
r = RethinkDB()
r.connect( "localhost", 28015).repl()


x = r.now().run()

print(r.table('tv_shows').count().run())
print(r.table('tv_shows').filter({'name':'Will'}).run())


print(r.now().run() -x)
