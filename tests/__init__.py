



# cursor.execute(""" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)RETURNING * """, (post.title,post.content,post.published))
    
#     new_post = cursor.fetchone()
    
#     conn.commit()  
    
#     return {"data": new_post}


# Most times you would never store your password in the db in a raw format you'd need to hash it and store the hashed value in the DB


# 10:30:27