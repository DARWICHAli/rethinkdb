from rethinkdb import RethinkDB
r = RethinkDB()
r.connect( "localhost", 28015).repl()


# x = r.now().run()

# print(r.table('tv_shows').count().run())
# print(r.table('tv_shows').filter({'name':'Will'}).run())


# print(r.now().run() -x)


#r.db('test').tableCreate('dc_universe', {primaryKey: 'name'}).run();


# r.db_create("test").run()

r.db('test').table_create('dc_universe', shards=2, replicas=2).run();




