from typing import List

from sqlmodel import Session, select, func, asc, desc
from rich.console import Console
from rich.table import Table

from .db import engine
from entity import WorkRecord

console = Console()
error_console = Console(stderr=True, style="bold red")

def print_table(count: int = 10):
    with Session(engine) as session:
        # 先获取总记录数
        total = session.exec(select(func.count()).select_from(WorkRecord)).one()
        work_records = session.exec(
            select(WorkRecord)
            .order_by(asc(WorkRecord.status), asc(WorkRecord.end_time))
            .offset(max(0, total - count))
            .limit(count)
        ).all()
        if not work_records:
            error_console.log("No records found.")
            return
        name_width = max(len(work_record.name) for work_record in work_records) + 20
        table = Table(title="Work Records " + str(len(work_records)), expand=True)
        table.add_column("ID", justify="center", style="cyan")
        table.add_column("任务", justify="center", style="magenta")
        table.add_column("开始时间", justify="center", style="green")
        table.add_column("结束时间", justify="center", style="green")
        table.add_column("状态", justify="center", style="green")
        for work_record in work_records:
            table.add_row(
                str(work_record.id),
                work_record.name,
                work_record.start_time,
                work_record.end_time,
                work_record.status.value,
            )
        console.print(table)

def check_duplicate_name(name: str):
    with Session(engine) as session:
        work_record = session.exec(
            select(WorkRecord).where(WorkRecord.name == name)
        ).first()
        return work_record is not None
