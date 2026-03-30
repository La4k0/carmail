from sqlalchemy import create_engine, String, ForeignKey, UniqueConstraint, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import insert
from typing import List
from scraper import get_brands_dict
import os
from dotenv import load_dotenv

load_dotenv()
# 🔗 DATABASE CONNECTION
DATABASE_URL = os.getenv('DB_URL')

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)


# 🧱 BASE CLASS
class Base(DeclarativeBase):
    pass


# 🧱 BRAND TABLE
class Brand(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    models: Mapped[List["Model"]] = relationship(
        back_populates="brand",
        cascade="all, delete"
    )


# 🧱 MODEL TABLE
class Model(Base):
    __tablename__ = "models"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    brand_id: Mapped[int] = mapped_column(
        ForeignKey("brands.id", ondelete="CASCADE")
    )

    brand: Mapped["Brand"] = relationship(back_populates="models")

    __table_args__ = (
        UniqueConstraint("name", "brand_id"),
    )


# 🏗️ CREATE TABLES
Base.metadata.create_all(engine)


# 🚀 GET OR CREATE BRAND
def get_or_create_brand(session, brand_name: str) -> Brand:
    stmt = insert(Brand).values(name=brand_name)
    stmt = stmt.on_conflict_do_nothing(index_elements=["name"])

    session.execute(stmt)

    brand = session.execute(
        select(Brand).where(Brand.name == brand_name)
    ).scalar_one()

    return brand


# 🚀 INSERT MODEL
def insert_model(session, model_name: str, brand_id: int):
    stmt = insert(Model).values(
        name=model_name,
        brand_id=brand_id
    )

    stmt = stmt.on_conflict_do_nothing(
        index_elements=["name", "brand_id"]
    )

    session.execute(stmt)


# 🚀 SAVE DATA
def save_brands_and_models(data: dict):
    session = SessionLocal()

    try:
        for brand_name, models in data.items():
            brand = get_or_create_brand(session, brand_name)

            for model_name in models:
                insert_model(session, model_name, brand.id)

        session.commit()

    except Exception as e:
        session.rollback()
        print("Error:", e)

    finally:
        session.close()

def get_column_values(model, column):
    session = SessionLocal()

    try:
        result = session.query(column).all()
        data_list = list([row[0] for row in result])
        data_list.sort()
        return data_list

    finally:
        session.close()

def get_models_by_brand(brand_name: str):
    with SessionLocal() as session:
        result = session.execute(
            select(Model.name)
            .join(Brand)
            .where(Brand.name == brand_name)
            .order_by(Model.name)
        )
        data_list = list([row[0] for row in result])
        data_list.sort()
        return data_list

# 🧪 TEST DATA (твоя dict)
if __name__ == "__main__":
    # data = get_brands_dict()

    a = get_column_values(Brand, Brand.name)
    print(a)