#!/usr/bin/env python
# coding: utf-8

# In[2]:


import sys
from rethinkdb import RethinkDB
r = RethinkDB()
import time
import matplotlib.pyplot as plt
from multiprocessing import Process, Queue
import psutil
import statistics



def check_ressources(q, msg, initial_cpu=0, initial_ram=0):
    print("Running Process...")
    i = 0
    cpu_usage = []
    mem_usage = []
    while (i == 0 or q.empty()):
        # Obtaining all the essential details
        cpu_usage.append(max(psutil.cpu_percent() - initial_cpu, 0))
        mem_usage.append(max(psutil.virtual_memory().percent - initial_ram, 0))
        i += 1
    print(msg)
    print(f"Mean CPU Usage : {statistics.mean(cpu_usage):0.2f}%")
    print(f"Mean Memory Usage : {statistics.mean(mem_usage):0.2f}%")



# In[9]:





if __name__ == '__main__':

	insert = False 
	select = True
	documentsNumber =  [10, 100, 1000, 10000, 100000]

	if insert: 

		# Connecting to the RethinkDB server
		r.connect(host='localhost', port=28015).repl()


		for docnum in documentsNumber:
			r.db_create("database{}".format(docnum)).run()
			db = r.db("database{}".format(docnum))
			db.table_create('posts').run()
			posts_table = db.table('posts')

			# Start time of all insertions
			start = time.time()
			q = Queue()
			p = Process(target=check_ressources, args=(q, f"Evaluation pour une base de données de taille {docnum}", psutil.cpu_percent(), psutil.virtual_memory().percent))
			p.start()
			for i in range(0, docnum):
				# Start time of a single insertion
				now = time.time()

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


			# End time for inserting all of the documents
			end = time.time()

			print(f"La durée pour toutes les insertions pour une base de donnée de taille {docnum}: {end - start:.2f} secondes\n")
			q.put('Done')
			p.join()

	if select :

		r.connect(host='localhost', port=28015).repl()



		# pour supprimer les index 

		r.db("database10").table("posts").index_drop("content").run()
		r.db("database100").table("posts").index_drop("content").run()
		r.db("database1000").table("posts").index_drop("content").run()
		r.db("database10000").table("posts").index_drop("content").run()
		r.db("database100000").table("posts").index_drop("content").run()


		for docnum in documentsNumber:


			# Connecting to the proper database and table for the tests
			db = r.db("database{}".format(docnum))
			db.table('posts').index_create("content").run() # création des index
			posts_table = db.table('posts')

			# Wait for the index to be ready to use
			db.table("posts").index_wait("content").run()



			con = "Content{}".format(int(docnum-1))
			uniqueCategory = db.table("posts").get_all(con, index="content")




			# Start time of a getting data
			now = time.time()
			q = Queue()
			p = Process(target=check_ressources, args=(q, f"Evaluation pour une base de données de taille {docnum}", psutil.cpu_percent(), psutil.virtual_memory().percent))
			p.start()
			
			for i in range(docnum*6):	

				uniqueCategory.run()


			# End time for getting all of the matched documents
			end = time.time()

			print(f"La durée pour toutes les selections pour une base de donnée de taille {docnum}: {end-now:.5f} secondes\n")
			q.put('Done')
			p.join()



	



