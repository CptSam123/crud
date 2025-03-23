import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { PostService } from '../post.service';
import { Post } from '../post';

@Component({
  selector: 'app-index',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './index.component.html',
  styleUrl: './index.component.css'
})
export class IndexComponent {
  posts: Post[] = [];

  constructor(public postService: PostService) {}

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
}
