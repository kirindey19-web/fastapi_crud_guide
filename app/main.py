from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, models
from app.database import engine, get_db

# Пересоздаем таблицы с новым полем created_at
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Article CRUD API with Dates", version="1.1.0")

@app.post("/articles/", response_model=schemas.Article, status_code=status.HTTP_201_CREATED)
def create_new_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """
    Create a new article with automatic creation date.
    - **title**: Title of the article (required)
    - **content**: Content of the article (required)
    - **created_at**: Automatically set to current datetime
    """
    return crud.create_article(db=db, article=article)

@app.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    """
    Get a single article by its ID including creation date.
    """
    db_article = crud.get_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.get("/articles/", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of articles with creation dates.
    - **skip**: Number of articles to skip (default 0)
    - **limit**: Maximum number of articles to return (default 100)
    """
    articles = crud.get_articles(db=db, skip=skip, limit=limit)
    return articles

@app.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(article_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """
    Update an existing article. Creation date remains unchanged.
    """
    db_article = crud.update_article(db=db, article_id=article_id, article_update=article)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return db_article

@app.delete("/articles/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(article_id: int, db: Session = Depends(get_db)):
    """
    Delete an article by its ID.
    """
    db_article = crud.delete_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return None