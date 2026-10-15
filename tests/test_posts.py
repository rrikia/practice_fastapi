import pytest
from app import schemas


# Create our own tokens 
# import the OAuth2 method to create a token
# so we don't have to request the API a token 


# We have to add test posts in the test database 
# relies on the two fixtures authorized_client and test_posts
def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # We can print out the posts in PostOut Pydantic form 
    # (so the form will do validation for us)
    def validate(post):
        return schemas.PostOut.model_validate(post)
    posts_map = map(validate, res.json())
    posts_list = list(posts_map)

    print(posts_list)
    assert len(posts_list) == len(test_posts)
    assert res.status_code == 200
    # Access the first post: posts_list[0].Post.id 

def test_unauthorized_user_get_all_posts(client, test_posts):
    # Use the regular client that's unauthorized to get all posts, should return 401
    # test_posts relies on test_user fixture, so we don't have to include 
    # test_user as a parameter here, because test_posts will automatically create a test user for us
    res = client.get("/posts/")
    assert res.status_code == 401

# Test individual posts by id 
# Unauthorized user
def test_unauthorized_user_get_one_posts(client, test_posts):
    # test_posts is a SQL Alchemy model 
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    # test_posts is a SQL Alchemy model 
    res = authorized_client.get(f"/posts/999999")
    assert res.status_code == 404

# Test getting a post that exists
def test_get_one_post(authorized_client, test_posts):
    # test_posts is a SQL Alchemy model 
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut.model_validate(res.json())
    # post.Post because in schemas.py, PostOut has a nested Post model,
    # so we have to access the Post model inside the PostOut model
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200


@pytest.mark.parametrize("title, content, published", [
    ("new title", "new content", True),
    ("favorite sushi", "i love pictures", False),
    ("favorite ice cream", "i love vanilla", True),
])

# Test creating a post
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    # test_user is a SQL Alchemy model 
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    
    created_post = schemas.Post.model_validate(res.json())
    assert res.status_code == 201

    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user['id']

def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    created_post = schemas.Post.model_validate(res.json())
    assert res.status_code == 201
    assert created_post.title == "arbitrary title"
    assert created_post.content == "arbitrary content"
    assert created_post.published == True
    assert created_post.owner_id == test_user['id']

def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "arbitrary content"})
    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_authorized_user_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204



def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/999999")
    assert res.status_code == 404


# A User deletes another user's post 
# So we need to have 1 more authorized_client in the database
# authorized_client is always the test_user and not test_user2  
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    # Delete the fourth post, so post with id = 3
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']
    assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_user, test_posts):
    res = client.put(f"/posts/{test_posts[4].id}")
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(f"/posts/999999", json=data)
    assert res.status_code == 404
