from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app=FastAPI()

#Models

class Movie(BaseModel):
    title: str
    genre: str
    year: int
    rating: float

class MovieUpdate(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None

class MovieResponse(BaseModel):
    id: int
    title: str
    genre: str
    year: int
    rating: float

#Test_Database

movies = [
    {
        "id": 1,
        "title": "K.G.F",
        "genre": "Crime Action",
        "year": 2026,
        "rating": 8.2
    },
    {
        "id": 2,
        "title": "Kantara",
        "genre": "Mythological",
        "year": 2024,
        "rating": 8.8
    },
    {
        "id": 3,
        "title": "777 Charlie",
        "genre": "Adventure",
        "year": 2022,
        "rating": 8.6
    },
    {
        "id": 4,
        "title": "Mr.India",
        "genre": "Sci-Fi",
        "year": 2020,
        "rating": 8.4
    },
]

# Home_Page

@app.get("/")
def home():
    return {
        "message": "Welcome to Movie Management API",
        "developer": "K Vijeth V Naik"
    }

#GET_Methods
#GET /movies
#GET /movies?genre=Sci-Fi

@app.get("/movies", response_model=List[MovieResponse])
def get_movies(genre: Optional[str] = None):
    if genre:
        return [
            movie for movie in movies
            if movie["genre"].lower() == genre.lower()
        ]
    return movies

#GET /movies/{id}

@app.get("/movies/{movie_id}", response_model=MovieResponse)
def get_movie(movie_id: int):
    for movie in movies:
        if movie["id"] == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Movie not found")

#POST /movies

@app.post("/movies", response_model=MovieResponse)
def create_movie(movie: Movie):
    new_id = max([m["id"] for m in movies], default=0) + 1
    new_movie = {
        "id": new_id,
        **movie.model_dump()
    }
    movies.append(new_movie)
    return new_movie

#PUT /movies/{id}

@app.put("/movies/{movie_id}", response_model=MovieResponse)
def replace_movie(movie_id: int, movie: Movie):
    for index, m in enumerate(movies):
        if m["id"] == movie_id:
            updated_movie = {
                "id": movie_id,
                **movie.model_dump()
            }
            movies[index] = updated_movie
            return updated_movie
    raise HTTPException(status_code=404, detail="Movie not found")

# PATCH /movies/{id}

@app.patch("/movies/{movie_id}", response_model=MovieResponse)
def update_movie(movie_id: int, movie: MovieUpdate):
    for m in movies:
        if m["id"] == movie_id:
            updates = movie.model_dump(exclude_unset=True)
            m.update(updates)
            return m
    raise HTTPException(status_code=404, detail="Movie not found")

# DELETE /movies/{id}

@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            movies.pop(index)
            return {
                "message": "Movie deleted successfully"
            }
    raise HTTPException(status_code=404, detail="Movie not found")