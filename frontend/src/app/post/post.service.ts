// src/app/post/post.service.ts
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { Post } from './post';

@Injectable({ providedIn: 'root' })
export class PostService {
  private apiURL = 'http://localhost:3000/api/posts';

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<Post[]> {
    return this.httpClient.get<Post[]>(this.apiURL).pipe(
      catchError(this.errorHandler)
    );
  }

  create(post: Post): Observable<any> {
    return this.httpClient.post(this.apiURL, post).pipe(
      catchError(this.errorHandler)
    );
  }

  find(id: string): Observable<Post> {
    return this.httpClient.get<Post>(`${this.apiURL}/${id}`).pipe(
      catchError(this.errorHandler)
    );
  }

  update(id: string, post: Post): Observable<any> {
    return this.httpClient.put(`${this.apiURL}/${id}`, post).pipe(
      catchError(this.errorHandler)
    );
  }

  delete(id: string): Observable<any> {
    return this.httpClient.delete(`${this.apiURL}/${id}`).pipe(
      catchError(this.errorHandler)
    );
  }

  errorHandler(error: any) {
    const errorMessage = error.error?.message || `Error Code: ${error.status}\nMessage: ${error.message}`;
    return throwError(() => errorMessage);
  }
}
