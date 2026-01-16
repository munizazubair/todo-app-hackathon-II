"""Todo API endpoints - Full CRUD operations with authentication."""

from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select, func, col
from models.todo import Todo, TodoCreate, TodoUpdate, TodoStatusUpdate, TodoStatus
from models.user import User
from core.deps import get_session, get_current_user
from core.messages import (
    MSG_TODO_CREATED,
    MSG_TODO_UPDATED,
    MSG_TODO_DELETED,
    ERR_TITLE_EMPTY,
    ERR_TITLE_TOO_LONG,
    MAX_TITLE_LENGTH,
)

router = APIRouter()


@router.get("/", response_model=dict, summary="Get all todos with filtering and pagination")
async def get_todos(
    status: Optional[TodoStatus] = Query(None, description="Filter by status (pending/completed)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, min_length=1, description="Search in title"),
    limit: int = Query(20, ge=1, le=100, description="Number of items per page"),
    offset: int = Query(0, ge=0, description="Number of items to skip"),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get todos with optional filtering, search, and pagination.

    **Requires authentication.** Returns only the authenticated user's todos.

    Returns:
    - items: List of todos
    - total: Total count of items (after filtering)
    - limit: Items per page
    - offset: Current offset
    """
    # Build base query - filter by current user
    query = select(Todo).where(Todo.user_id == current_user.id)

    # Apply filters
    if status:
        query = query.where(Todo.status == status)
    if category:
        query = query.where(Todo.category == category)
    if search:
        query = query.where(col(Todo.title).ilike(f"%{search}%"))

    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    total = session.exec(count_query).one()

    # Apply ordering (newest first) and pagination
    query = query.order_by(Todo.created_at.desc()).offset(offset).limit(limit)

    # Execute query
    todos = session.exec(query).all()

    return {
        "items": todos,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/stats", response_model=dict, summary="Get todo statistics")
async def get_stats(
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get statistics about todos.

    **Requires authentication.** Returns stats only for the authenticated user's todos.

    Returns:
    - total: Total number of todos
    - pending: Number of pending todos
    - completed: Number of completed todos
    - overdue: Number of overdue todos (pending with past due_date)
    """
    from datetime import date

    # Get counts by status - filtered by current user
    total = session.exec(
        select(func.count(Todo.id)).where(Todo.user_id == current_user.id)
    ).one()
    pending = session.exec(
        select(func.count(Todo.id))
        .where(Todo.user_id == current_user.id)
        .where(Todo.status == TodoStatus.PENDING)
    ).one()
    completed = session.exec(
        select(func.count(Todo.id))
        .where(Todo.user_id == current_user.id)
        .where(Todo.status == TodoStatus.COMPLETED)
    ).one()

    # Get overdue count (pending todos with past due date)
    today = date.today()
    overdue = session.exec(
        select(func.count(Todo.id))
        .where(Todo.user_id == current_user.id)
        .where(Todo.status == TodoStatus.PENDING)
        .where(Todo.due_date < today)
    ).one()

    return {
        "total": total,
        "pending": pending,
        "completed": completed,
        "overdue": overdue,
    }


@router.get("/{todo_id}", response_model=Todo, summary="Get a single todo by ID")
async def get_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Get a specific todo by ID.

    **Requires authentication.** Returns 404 if todo doesn't exist or belongs to another user.
    """
    # Query with user_id filter for security
    statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == current_user.id)
    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )
    return todo


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED, summary="Create a new todo")
async def create_todo(
    todo_data: TodoCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new todo.

    **Requires authentication.** The todo will be associated with the authenticated user.

    Validates:
    - Title is not empty (after stripping whitespace)
    - Title length <= 500 characters
    """
    # Validate and normalize title
    title = todo_data.title.strip()
    if not title:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_TITLE_EMPTY,
        )
    if len(title) > MAX_TITLE_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ERR_TITLE_TOO_LONG,
        )

    # Create todo with normalized title and user_id
    todo = Todo(
        title=title,
        category=todo_data.category,
        due_date=todo_data.due_date,
        user_id=current_user.id,  # Associate with current user
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {
        "message": MSG_TODO_CREATED,
        "todo": todo,
    }


@router.put("/{todo_id}", response_model=dict, summary="Update a todo (full update)")
async def update_todo(
    todo_id: int,
    todo_data: TodoUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update a todo with optimistic locking.

    **Requires authentication.** Can only update own todos.

    Requires version field to prevent concurrent update conflicts.
    Only provided fields will be updated.
    """
    # Get existing todo - verify ownership
    statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == current_user.id)
    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    # Check version for optimistic locking
    if todo.version != todo_data.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Version mismatch. Expected {todo.version}, got {todo_data.version}. The todo was modified by another user.",
        )

    # Update fields if provided
    update_data = todo_data.model_dump(exclude_unset=True, exclude={"version"})

    # Validate title if provided
    if "title" in update_data:
        title = update_data["title"].strip()
        if not title:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_TITLE_EMPTY,
            )
        if len(title) > MAX_TITLE_LENGTH:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ERR_TITLE_TOO_LONG,
            )
        update_data["title"] = title

    # Apply updates
    for key, value in update_data.items():
        setattr(todo, key, value)

    # Update metadata
    todo.updated_at = datetime.utcnow()
    todo.version += 1

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {
        "message": MSG_TODO_UPDATED,
        "todo": todo,
    }


@router.patch("/{todo_id}/status", response_model=dict, summary="Update todo status only")
async def update_todo_status(
    todo_id: int,
    status_data: TodoStatusUpdate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Update only the status of a todo (pending/completed).

    **Requires authentication.** Can only update own todos.

    Uses optimistic locking via version field.
    """
    # Get existing todo - verify ownership
    statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == current_user.id)
    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    # Check version for optimistic locking
    if todo.version != status_data.version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Version mismatch. Expected {todo.version}, got {status_data.version}. The todo was modified by another user.",
        )

    # Update status and metadata
    todo.status = status_data.status
    todo.updated_at = datetime.utcnow()
    todo.version += 1

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return {
        "message": MSG_TODO_UPDATED,
        "todo": todo,
    }


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK, summary="Delete a todo")
async def delete_todo(
    todo_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a todo by ID.

    **Requires authentication.** Can only delete own todos.
    """
    # Get todo - verify ownership
    statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == current_user.id)
    todo = session.exec(statement).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found",
        )

    session.delete(todo)
    session.commit()

    return {
        "message": MSG_TODO_DELETED,
        "id": todo_id,
    }
