import typer
from typing import List
from typing_extensions import Annotated
from sqlmodel import SQLModel, create_engine, Session, select
from rich import print

from datetime import date

from entity.record import WorkRecord, WorkStatus
from utils.util import console, error_console, print_table, check_duplicate_name
from utils.db import engine

app = typer.Typer()

@app.command()
def list(
    count: Annotated[int, typer.Option(help="Display the number of records")] = 10,
):
    print_table(count)

@app.command()
def create(name: str):
    if check_duplicate_name(name):
        error_console.log(f"记录 {name} 已存在")
        return
    today = date.today().strftime("%Y-%m-%d")
    work_record = WorkRecord(name=name, start_time=today, end_time=today)
    with Session(engine) as session:
        session.add(work_record)
        session.commit()
        session.refresh(work_record)
    print_table()


@app.command()
def work(ids: List[str]):
    """更新指定ID的工作记录的结束时间为当前日期

    Args:
        ids: 工作记录的ID列表

    Author: 王强
    Date: 2024-07-29
    Version: 1.0.0
    """
    today = date.today().strftime("%Y-%m-%d")
    with Session(engine) as session:
        for record_id_str in ids:
            try:
                work_record = session.exec(
                    select(WorkRecord).where(WorkRecord.id == int(record_id_str))
                ).one()
                if work_record:
                    work_record.end_time = today
                    session.add(work_record)
                    session.commit()
                    session.refresh(work_record)
                else:
                    error_console.log(f"未找到记录 ID {record_id_str}")
            except ValueError:
                error_console.log(f"无效的记录 ID: {record_id_str}")
    print_table()

@app.command()
def commit(ids: List[str]):
    with Session(engine) as session:
        for record_id_str in ids:
            try:
                work_record = session.exec(
                    select(WorkRecord).where(WorkRecord.id == int(record_id_str))
                ).one()
                if work_record:
                    work_record.status = WorkStatus.COMPLETED
                    session.add(work_record)
                    session.commit()
                    session.refresh(work_record)
                else:
                    error_console.log(f"未找到记录 ID {record_id_str}")
            except ValueError:
                error_console.log(f"无效的记录 ID: {record_id_str}")
    print_table()

@app.command(name="rm")
def delete(ids: List[str]):
    with Session(engine) as session:
        for record_id_str in ids:
            try:
                work_record = session.exec(
                    select(WorkRecord).where(WorkRecord.id == int(record_id_str))
                ).one()
                if work_record:
                    session.delete(work_record)
                    session.commit()
                    console.log("Deleted record:", work_record)
                else:
                    error_console.log(f"未找到记录 ID {record_id_str}")
            except ValueError:
                error_console.log(f"无效的记录 ID: {record_id_str}")
        

if __name__ == "__main__":
    app()
