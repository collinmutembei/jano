from typing import List
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import JournalEntry, JournalEntryCreate, JournalEntryUpdate, User
from src.models import JournalEntry as JournalEntryModel
from src.database import get_db
from src.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=JournalEntry, status_code=201)
def create_journal_entry(
    entry: JournalEntryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    db_entry = JournalEntryModel(**entry.model_dump(), user_id=user.id)
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


@router.get("/", response_model=List[JournalEntry])
def get_journal_entries(
    start: date = None,
    end: date = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    entries = db.query(JournalEntryModel).filter(JournalEntryModel.user_id == user.id)
    if start and end:
        return entries.filter(JournalEntryModel.date.between(start, end))
    return entries.all()


@router.put("/{journal_id}", response_model=JournalEntry)
def update_journal_entry(
    journal_id: int,
    journal_update: JournalEntryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    journal = (
        db.query(JournalEntryModel).filter(JournalEntryModel.id == journal_id).first()
    )
    if journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    if journal.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to update this journal"
        )
    update_data = journal_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(journal, key, value)
    db.commit()
    db.refresh(journal)
    return journal


@router.delete("/{journal_id}", status_code=204)
def delete_journal_entry(
    journal_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    journal = (
        db.query(JournalEntryModel).filter(JournalEntryModel.id == journal_id).first()
    )
    if journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    if journal.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this journal"
        )
    db.delete(journal)
    db.commit()
