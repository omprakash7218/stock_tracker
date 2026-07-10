from fastapi import APIRouter
from pydantic import BaseModel
from fastapi.params import Body

router = APIRouter(tags=["posts"],prefix="/posts")
class Post(BaseModel):
	title: str
	content: str
	published: bool = True

@router.get("/posts")
def show_posts():
	return {"message":f"Here are all the posts"}

@router.post("/posts")
def create_post(post:Post):
	print(f"Title:{post.title} Content:{post.content}  published: {post.published}")
	return {"message": f"Title:{post.title} Content: {post.content}  published: {post.published}"}
@router.post("/posts2")
def create_post(posts:dict=Body(...)):
	print(posts)
	return {"new_post": f"Here is your post {posts}"}
