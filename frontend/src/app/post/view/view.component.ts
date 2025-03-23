import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PostService } from '../post.service';
import { Post } from '../post';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './view.component.html',
  styleUrl: './view.component.css'
})
export class ViewComponent {
  id!: string;
  post?: Post;

  constructor(private route: ActivatedRoute, public postService: PostService) {}

  ngOnInit(): void {
    this.id = this.route.snapshot.params['postId'];
    if (this.id) {
      this.postService.find(this.id).subscribe({
        next: data => this.post = data,
        error: err => console.error('Load error:', err)
      });
    }
  }
}
