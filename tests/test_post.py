# We'd need to deal with authentication for our post testing
from typing import List
from app import schemas
import pytest



def test_get_all_posts(authorized_client,test_post):
    res = authorized_client.get("/posts/")
    # print(res.json())
    
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate,res.json())
    post_list = list(posts_map)
    print(list(posts_map))
    assert len(res.json()) == len(test_post)
    assert res.status_code == 201 
    # changed this one from 200


def test_unauthorized_user_get_all_posts(client, test_post):
    res = client.get("/posts/")
    assert res.status_code == 401
    
    
def test_unauthorized_user_get_one_posts(client, test_post):
    res = client.get(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
    
def test_get_one_post_not_exist(authorized_client,test_post):
    res = authorized_client.get(f"/posts/88888")
    assert res.status_code == 404
    
# def test_get_one_post(authorized_client,test_post):
#     res = authorized_client.get(f"/posts/{test_post[0].id}")
#     # assert res.status_code == 404
#     post = schemas.PostOut(**res.json())
#     assert post.Post.id == test_post[0].id
#     assert post.Post.content ==  test_post[0].content


@pytest.mark.parametrize("title,content,published",[
    ("awesome new title","awesome new content", True),
    ("pizza","I love pepperoni",False),
    ("building","Burj Kahalifa",True)
])
def test_create_post(authorized_client,create_test_user,test_post,title,content,published):
    res = authorized_client.post("/posts/",json={"title":title,"content":content,"published":published})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    # assert created_post.owner_id ==  create_test_user.id
    assert created_post.owner_id == create_test_user['id']
    
def test_create_post_default_published_true(authorized_client,create_test_user,test_post):
    res = authorized_client.post("/posts/",json={"title":"title","content":"content"})
    
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "title"
    assert created_post.content == "content"
    assert created_post.published == True
    # assert created_post.owner_id ==  create_test_user.id
    assert created_post.owner_id == create_test_user['id']
    
    
def test_unauthorized_user_create_post(client, test_post,  create_test_user):
    res = client.post("/posts/",json={"title":"title","content":"content"})
    assert res.status_code == 401
    
    
def test_unauthorized_user_delete_post(client,test_post,create_test_user):
    res = client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_delete_post_success(authorized_client,test_post,create_test_user):
    res = authorized_client.delete(f"/posts/{test_post[0].id}")
    assert res.status_code == 204
    
def test_delete_post_non_exist(authorized_client,test_post,create_test_user):
    res = authorized_client.delete(f"/posts/900")
    assert res.status_code == 404
    
    
# test when user tries to delete a post that isn't theirs'
def test_delete_other_user_post(authorized_client,test_post,create_test_user):
    res = authorized_client.delete(f"/posts/{test_post[3].id}")
    assert res.status_code == 403
    
    
# def test_update_post(authorized_client,create_test_user,test_post):
#     data = {
#         "title":"updated title",
#         "content":"updated content",
#         "id": test_post[0].id
#     }
    
#     res = authorized_client.put(f"/posts/{test_post[0].id}",json=data)
    
#     updated_post = schemas.Post(**res.json())
#     assert res.status_code == 200
#     assert updated_post.title == data['title']
#     assert updated_post.content == data['content']
    
    
# def test_update_other_user_post(authorized_client,test_post):
#     data = {
#         "title": "updated title",
#         "content": "updated content",
#         "id": test_post[3].id
#     }
    
#     res = authorized_client.put(f"/posts/{test_post[3].id}",json=data)
    
#     assert res.status_code == 403
#     assert res.join().get('detail') == "Not Authorized to perform requested action"


def test_unauthorized_user_update_post(client,test_post,create_test_user):
    res = client.put(f"/posts/{test_post[0].id}")
    assert res.status_code == 401
    
def test_update_post_non_exist(authorized_client,test_post,create_test_user):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_post[3].id
    }
    res = authorized_client.put(f"/posts/900", json=data)
    assert res.status_code == 404