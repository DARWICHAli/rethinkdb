import sys
import pymysql.cursors
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
if __name__ == '__main__':
    # Database's size
    documentsNumber = [10, 100, 1000, 10000, 100000]
    connection = pymysql.connect(host='localhost', port=3306, user='root', password='')

    cursor = connection.cursor()

    # Create 1-N tables
    createPosts = "CREATE TABLE posts (id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, title VARCHAR(250) NOT NULL, content VARCHAR(250) NOT NULL, created VARCHAR(250))"
    createTags = 'CREATE TABLE tags (id_tag INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL)'
    createCategories = 'CREATE TABLE categories (id_category INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL)'
    createUsers = 'CREATE TABLE users (id_user INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, name VARCHAR(250) NOT NULL, password VARCHAR(250) NOT NULL)'

    # Create M-N tables
    createPostsCategories = 'CREATE TABLE postsCategories (id_post_category INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(10), category_id INT(10))'
    createPostsTags = 'CREATE TABLE postsTags (id_post_tag INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(11), tag_id INT(10))'
    createLikes = 'CREATE TABLE likes (id_like INT(10) UNSIGNED AUTO_INCREMENT PRIMARY KEY, post_id INT(11), user_id INT(10))'
    
    for docnum in documentsNumber:
        # We create suitable databases for running various tests
        try:    
            cursor.execute(f"CREATE DATABASE database{docnum}")
        except Exception as e:
            print(f"Exception : {e}\n NB :If Database Exists we DROP then we create ONE")
            cursor.execute(f"DROP DATABASE database{docnum}")
            cursor.execute(f"CREATE DATABASE database{docnum}")
            
        cursor.execute(f"USE database{docnum}")
        
        # Table Creations
        cursor.execute(createPosts)
        cursor.execute(createTags)
        cursor.execute(createCategories)
        cursor.execute(createUsers)
        cursor.execute(createPostsCategories)
        cursor.execute(createPostsTags)
        cursor.execute(createLikes)

        
        start = time.time()
        q = Queue()
        p = Process(target=check_ressources, args=(q, f"Evaluation pour une base de données de taille {docnum}", psutil.cpu_percent(), psutil.virtual_memory().percent))
        p.start()
        # Insertions to Tables
        for i in range(docnum):
            now = time.time()
            cursor.execute("INSERT INTO `posts` (`title`, `content`, `created`) VALUES (%s, %s, %s)", (f"Title{i}", f"Content{i}", now))
            connection.commit()
            
            cursor.execute("INSERT INTO `tags` (`name`) VALUES (%s)", f"Tag{i}")
            connection.commit()
            
            cursor.execute("INSERT INTO `categories` (`name`) VALUES (%s)", f"Category{i}")
            connection.commit()
            
            cursor.execute("INSERT INTO `postsTags` (`post_id`, `tag_id`) VALUES (%s, %s)", (i+1, 1))
            connection.commit()

            cursor.execute("INSERT INTO `postsTags` (`post_id`, `tag_id`) VALUES (%s, %s)", (i+1, i+2))
            connection.commit()

            cursor.execute("INSERT INTO `users` (`name`, `password`) VALUES (%s, %s)", (f'user{i}', f'pass{i}{i+1}'))
            connection.commit()
            
            cursor.execute("INSERT INTO `postsCategories` (`post_id`, `category_id`) VALUES (%s, %s)", (i+1, 1))
            connection.commit()

            cursor.execute("INSERT INTO `postsCategories` (`post_id`, `category_id`) VALUES (%s, %s)", (i+1, i+2))
            connection.commit()
            
            cursor.execute("INSERT INTO `likes` (`post_id`, `user_id`) VALUES (%s, %s)", (i+1, 1))
            connection.commit()
        # End time for inserting all of the documents
        end = time.time()
        print(f"La durée pour toutes les insertions pour une base de donnée de taille {docnum}: {end - start:.2f} secondes\n")
        q.put('Done')
        p.join()
    connection.close()
        
