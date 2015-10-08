#
# Database access functions for the web forum.
# 

import time
import psycopg2

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")

    c = DB.cursor()
    query = "select time, content from posts order by time desc"
    c.execute(query)
    rows = c.fetchall()
    
    posts = [{'content': str(row[1]), 'time': str(row[0])} for row in rows]
    DB.close()

    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    ## Database connection
    DB = psycopg2.connect("dbname=forum")

    c = DB.cursor()
    c.execute("insert into posts (content) values (%s)", (content,))
    DB.commit()
    DB.close()