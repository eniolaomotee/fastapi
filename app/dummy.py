# @app.get("/posts")
# def get_posts():
    
  
#     # Getting all posts with SQL
#     cursor.execute(""" SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     print(posts)
#     return {"data":posts}

# # Using pydantic(Base Model) for our data validation from the user.
# # Create Post- retrieve the post and add to the post array,also use to pydantic to validate the post
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post): 
#     # creating Posts with SQL
#     cursor.execute(""" INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title,post.content,post.published)) 
    
#     new_post = cursor.fetchone()
    
#     conn.commit()
       
       
#     # normal Create Post without SQL
#     # post_dict = post.dict()
#     # post_dict['id'] = randrange(0,100000)
#     # my_posts.append(post_dict)
    
#     return {"data": new_post}



# # Retrieving one single post (Performing validation as well)
# # Getting response codes as well as status codes when a resource is been created or gotten from a database.
# @app.get("/posts/{id}")
# def get_post(id:int, response: Response):
#     # Get posts via SQL Queries
#     cursor.execute(""" SELECT * FROM posts WHERE id= %s""",(str(id),))
#     post = cursor.fetchone()
    
#     # Get post by Id Normal way
#     # for post in my_posts:
#     #     if post['id'] == id:
#     #         return {"post_detail":post}
    
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with {id} was not found")

#     return {"post_detail": post}

# # Delete a post
# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_posts(id:int):
#     # Deleting a post via SQL QUERIES
#     cursor.execute("""DELETE FROM posts WHERE id= %s RETURNING *""",(str(id),))
#     deleted_post = cursor.fetchone()
    
#     conn.commit()
    
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
#     # Deleting a post the normal way via the index
#     # for index,post in enumerate(my_posts):
#     #     if post['id'] == id:
#     #         my_posts.pop(index)
#     # return Response(status_code=status.HTTP_204_NO_CONTENT)

# # Update a Post
# @app.put("/posts/{id}")
# def update_post(id:int,post:Post):
#     # Updating post with SQL QUERIES
#     cursor.execute(""" UPDATE posts SET title =%s,content=%s, published=%s WHERE id=%s RETURNING *""",(post.title,post.content,post.published, str(id)))
    
#     updated_post = cursor.fetchone()
    
#     conn.commit()
    
    
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id:{id} does not exist")
    
    
#     # Updating Our Post with Normal code with the id 
#     # for index,posts in enumerate(my_posts):
#     #     if posts['id'] == id:
#     #         post_dict = post.dict()
#     #         post_dict['id'] = id
#     #         my_posts[index]= post_dict 
            
#     #         return {"messge":"Post updated successfully", "post":post_dict}
#     return  {"data":updated_post}



# # Using an ORM 
# # Prevents SQL injection, b. perform db operations without SQL queries with normal python code c. Sits between the database and us



