// src/app/post/index/index.component.ts
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import { PostService } from '../post.service';
import { Post } from '../post';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-index',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './index.component.html',
  styleUrl: './index.component.css'
})
export class IndexComponent {
  posts: Post[] = [];

  constructor(
    public postService: PostService,
    public authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.postService.getAll().subscribe((data: Post[]) => {
      this.posts = data;
    });
  }

  deletePost(id: string | undefined) {
    if (!id) return;
    this.postService.delete(id).subscribe(() => {
      this.posts = this.posts.filter(post => post._id !== id);
    });
  }

  logout() {
    this.authService.logout();
    this.router.navigate(['/login']);
  }
}
