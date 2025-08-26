from sqlalchemy.orm import Session
from app import models, schemas

def create_article(db: Session, article: schemas.ArticleCreate):
    db_article = models.Article(**article.model_dump())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article

def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()

def get_articles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Article).order_by(models.Article.created_at.desc()).offset(skip).limit(limit).all()

def update_article(db: Session, article_id: int, article_update: schemas.ArticleCreate):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article is None:
        return None

    update_data = article_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_article, field, value)

    db.commit()
    db.refresh(db_article)
    return db_article

def delete_article(db: Session, article_id: int):
    db_article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if db_article is None:
        return None

    db.delete(db_article)
    db.commit()
    return db_article