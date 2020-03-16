import sqlite3 as lite
import csv
import re
con = lite.connect('cs1656.sqlite')

with con:
	cur = con.cursor() 

	########################################################################		
	### CREATE TABLES ######################################################
	########################################################################		
	# DO NOT MODIFY - START 
	cur.execute('DROP TABLE IF EXISTS Actors')
	cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

	cur.execute('DROP TABLE IF EXISTS Movies')
	cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

	cur.execute('DROP TABLE IF EXISTS Directors')
	cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

	cur.execute('DROP TABLE IF EXISTS Cast')
	cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

	cur.execute('DROP TABLE IF EXISTS Movie_Director')
	cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################		
	### READ DATA FROM FILES ###############################################
	########################################################################		
	# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
	# UPDATE THIS
	
	#create variables for the files
	actors = []
	cast = []
	directors = []
	movie_dir = []
	movies = []

	
	#---Now read from the files---  
	with open('actors.csv') as actor_csv:
		csv_reader = csv.reader(actor_csv)
		for row in csv_reader:
			actors.append(row)

	with open('movies.csv') as movies_csv:
		csv_reader = csv.reader(movies_csv)
		for row in csv_reader:
			movies.append(row)

	with open('directors.csv') as directors_csv:
		csv_reader = csv.reader(directors_csv)
		for row in csv_reader:
			directors.append(row)

	with open('cast.csv') as cast_csv:
		csv_reader = csv.reader(cast_csv)
		for row in csv_reader:
			cast.append(row)

	with open('movie_dir.csv') as movie_dir_csv:
		csv_reader = csv.reader(movie_dir_csv)
		for row in csv_reader:
			movie_dir.append(row)

	########################################################################		
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################		
	# UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
	
	#---replace the single quoation with a double so the data can be entered using INSERT INTO---
	for actor in actors:
		for arg in actor:
			arg.replace("'","''")

	for movie in movies:
		for arg in movie:
			arg.replace("'","''")

	for director in directors:
		for arg in director:
			arg.replace("'","''")

	for cast_ in cast:
		for arg in cast_:
			arg.replace("'","''")

	for movie_dir_ in movie_dir:
		for arg in movie_dir_:
			arg.replace("'","''")


	#---insert the data into the database---
	for actor in actors:
		cur.execute("INSERT INTO Actors VALUES(" + actor[0] + ", '" + actor[1] + "', '" + actor[2] + "', '" + actor[3] + "')")

	for movie in movies:
		cur.execute("INSERT INTO Movies VALUES(" + movie[0] + ", '" + movie[1] + "', '" + movie[2] + "', '" + movie[3] + "')")

	for director in directors:
		cur.execute("INSERT INTO Directors VALUES(" + director[0] + ", '" + director[1] + "', '" + director[2] + "')")

	for cast_ in cast:
		cur.execute("INSERT INTO Cast VALUES(" + cast_[0] + ", '" + cast_[1] + "', '" + cast_[2] + "')")

	for movie_dir_ in movie_dir:
		cur.execute("INSERT INTO Movie_Director VALUES(" + movie_dir_[0] + ", '" + movie_dir_[1] + "')")

	con.commit()
    
	########################################################################		
	### QUERY SECTION ######################################################
	########################################################################		
	queries = {}

	# DO NOT MODIFY - START 	
	# DEBUG: all_movies ########################
	queries['all_movies'] = '''
SELECT * FROM Movies
'''	
	# DEBUG: all_actors ########################
	queries['all_actors'] = '''
SELECT * FROM Actors
'''	
	# DEBUG: all_cast ########################
	queries['all_cast'] = '''
SELECT * FROM Cast
'''	
	# DEBUG: all_directors ########################
	queries['all_directors'] = '''
SELECT * FROM Directors
'''	
	# DEBUG: all_movie_dir ########################
	queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''	
	# DO NOT MODIFY - END

	########################################################################		
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################		
	# NOTE: You are allowed to also include other queries here (e.g., 
	# for creating views), that will be executed in alphabetical order.
	# We will grade your program based on the output files q01.csv, 
	# q02.csv, ..., q12.csv

	# Q01 ########################		
	queries['q01'] = '''
	SELECT fname,lname
	FROM Actors as a, Cast as c
	WHERE a.aid = c.aid
	AND c.mid IN(	SELECT mid
					FROM Movies
					WHERE year BETWEEN 1980 AND 1990)
	AND c.mid IN(	SELECT mid
					FROM Movies
					WHERE year >= 2000)
	ORDER BY lname, fname

'''	
	
	# Q02 ########################	
	queries['q02'] = '''
	SELECT title, year
	FROM Movies as m
	WHERE m.year = (	SELECT year
						FROM Movies
						WHERE title = "Rogue One: A Star Wars Story")
	AND m.rank > (		SELECT rank
						FROM Movies
						WHERE title = "Rogue One: A Star Wars Story")
	ORDER BY title

'''	

	# Q03 ########################		
	queries['q03'] = '''
	SELECT DISTINCT a.fname, a.lname
	FROM Actors as a, Cast as c, Movies as m
	WHERE c.aid = a.aid AND c.mid = m.mid
	AND m.title IN(	SELECT m1.title
					FROM movies as m1
					WHERE m1.title LIKE '%Star Wars%')
	GROUP BY a.aid
	ORDER BY count(m.title) DESC, lname,fname

'''	

	# Q04 ########################		
	queries['q04'] = '''
	SELECT fname,lname
	FROM Actors as a, Cast as c
	WHERE a.aid = c.aid
	AND c.mid IN(		SELECT mid
						FROM Movies
						WHERE year < 1985)
	AND c.mid NOT IN(	SELECT mid
						FROM Movies
						WHERE year >= 1985)
	ORDER BY lname, fname

'''	

	# Q05 ########################		
	queries['q05'] = '''
	SELECT fname,lname, count(*) as mdc
	FROM Directors as d, Movie_Director as md
	WHERE md.did = d.did
	GROUP BY fname,lname
	ORDER BY mdc DESC
	LIMIT 20

'''	

	# Q06 ########################

	cur.execute("DROP VIEW IF EXISTS cast_cnt")

	q06a = '''
	CREATE VIEW cast_cnt AS
		SELECT m.title, count(c.aid) as count
		FROM Movies as m, Cast as c
		WHERE m.mid = c.mid
		GROUP BY m.title
		ORDER BY count DESC
		LIMIT 10

	'''

	cur.execute(q06a)

	queries['q06'] = '''
	SELECT m.title, count(c.aid) as cc
	FROM Movies as m, Cast as c
	WHERE m.mid = c.mid
	GROUP BY title
	HAVING cc >= (SELECT MIN(cc_.count) FROM cast_cnt cc_)
	ORDER BY cc DESC

'''	

	# Q07 ########################
	cur.execute("DROP VIEW IF EXISTS male_actors")
	cur.execute("DROP VIEW IF EXISTS female_actors")


	q07a = '''
	CREATE VIEW male_actors AS
		SELECT m.title, count(*) as mc
		FROM Movies as m, Cast as c
		WHERE m.mid = c.mid
		AND c.aid IN(	SELECT aid 
						FROM Actors
						WHERE gender = "Male" )
		GROUP BY title
		ORDER BY mc DESC

	'''

	q07b = '''
	CREATE VIEW female_actors AS
		SELECT m.title, count(*) as fc
		FROM Movies as m, Cast as c
		WHERE m.mid = c.mid
		AND c.aid IN(	SELECT aid 
						FROM Actors
						WHERE gender = "Female" )
		GROUP BY title
		ORDER BY fc DESC	

	'''

	cur.execute(q07a)
	cur.execute(q07b)

	queries['q07'] = '''
	SELECT DISTINCT male_actors.title,female_actors.fc,male_actors.mc
	FROM male_actors, female_actors
	WHERE male_actors.title = female_actors.title
	AND female_actors.fc > male_actors.mc
	ORDER BY male_actors.title

'''	

	# Q08 ########################		
	queries['q08'] = '''
	SELECT DISTINCT a.fname, a.lname, count(DISTINCT md.did) as dir_cnt
	FROM Actors AS a, Cast as c, Movie_Director as md, Directors as d
	WHERE c.aid = a.aid AND md.mid = c.mid AND d.did = md.did
	AND Not (a.fname = d.fname AND a.lname = d.lname)
	GROUP by a.aid
	HAVING dir_cnt >= 7
	ORDER BY dir_cnt DESC    


'''	

	# Q09 ########################		
	queries['q09'] = '''
	SELECT a.fname, a.lname, count(DISTINCT m.title) as title_cnt
	FROM Actors AS a, Cast as c, Movies as m
	WHERE c.aid = a.aid AND m.mid = c.mid
	AND m.year = (	SELECT MIN(m2.year)
					FROM Movies as m2, Cast AS c2, Actors AS a2
					WHERE c2.mid = m2.mid AND a2.aid = a.aid AND a2.aid = c2.aid
					)
	AND a.fname LIKE 'S%'
	GROUP BY a.aid

'''	

	# Q10 ########################
	queries['q10'] = '''
	SELECT a.lname, m.title
	FROM Actors as a, Cast as c, Movies as m, Movie_Director as md, Directors as d
	WHERE a.aid = c.aid AND c.mid = md.mid AND md.did = d.did AND m.mid = c.mid
	AND d.lname = a.lname
	AND d.fname <> a.fname
	ORDER BY a.lname
'''	

	# Q11 ########################
	cur.execute("DROP VIEW IF EXISTS bacon_movies")
	cur.execute("DROP VIEW IF EXISTS costars")
	cur.execute("DROP VIEW IF EXISTS costar_movies")

	q11a = '''
	CREATE VIEW bacon_movies as
		SELECT DISTINCT m.mid
		FROM Actors as a, Cast as c, Movies as m
		WHERE a.aid = c.aid AND c.mid = m.mid
		AND a.fname = "Kevin"
		AND a.lname = "Bacon"
		GROUP BY m.mid
	'''
	
	q11b = '''
	CREATE VIEW costars as
		SELECT DISTINCT a.aid
		FROM Actors as a, Cast as c, Movies as m, bacon_movies as bm
		WHERE a.aid = c.aid AND c.mid = m.mid AND bm.mid = m.mid
		AND NOT (a.fname = "Kevin" AND a.lname = "Bacon")
		GROUP BY a.aid
	
'''

	q11c ='''
	CREATE VIEW costar_movies as
		SELECT DISTINCT m.mid
		FROM Actors as a, Cast as c, Movies as m, costars as co
		WHERE a.aid = c.aid AND c.mid = m.mid AND co.aid = a.aid
		GROUP BY m.mid

'''

	cur.execute(q11a)
	cur.execute(q11b)	
	cur.execute(q11c)

	queries['q11'] = '''
	SELECT DISTINCT a.fname, a.lname
	FROM Actors as a, Cast as c, Movies as m, costar_movies as como
	WHERE a.aid = c.aid AND c.mid = m.mid AND como.mid = m.mid
	AND a.aid NOT IN (	SELECT *
						FROM costars)
	AND NOT (a.fname = "Kevin" AND a.lname = "Bacon")
	ORDER BY a.fname
'''	

	# Q12 ########################		
	queries['q12'] = '''
	SELECT a.fname, a.lname, count(DISTINCT m.title) as mov_cnt, avg(m.rank) as avg_rank
	FROM Actors as a, Cast as c, Movies as m
	WHERE a.aid = c.aid AND c.mid = m.mid
	GROUP BY a.aid
	ORDER BY avg_rank DESC
	LIMIT 20
'''	


	########################################################################		
	### SAVE RESULTS TO FILES ##############################################
	########################################################################		
	# DO NOT MODIFY - START 	
	for (qkey, qstring) in sorted(queries.items()):
		try:
			cur.execute(qstring)
			all_rows = cur.fetchall()
			
			print ("=========== ",qkey," QUERY ======================")
			print (qstring)
			print ("----------- ",qkey," RESULTS --------------------")
			for row in all_rows:
				print (row)
			print (" ")

			save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
			if (save_to_file):
				with open(qkey+'.csv', 'w') as f:
					writer = csv.writer(f)
					writer.writerows(all_rows)
					f.close()
				print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
		
		except lite.Error as e:
			print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
