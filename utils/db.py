from sqlmodel import SQLModel, create_engine

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///D:/data/record-book/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=False)  # echo=True 显示SQL语句

# 创建表
SQLModel.metadata.create_all(engine)
