 ### Jano API Service

 How to run the API
 ```shell
 docker compose up
 ```
 Apply database migrations
 ```
 docker compose exec backend bash
 alembic upgrade head
 ```
 Open http://localhost:8000/docs to view docs
