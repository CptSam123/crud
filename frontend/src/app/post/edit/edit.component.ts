import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PostService } from '../post.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Post } from '../post';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-edit',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './edit.component.html',
  styleUrl: './edit.component.css'
})
export class EditComponent implements OnInit {

  id!: string;
  post!: Post;
  form!: FormGroup;

  constructor(
    public postService: PostService,
    private route: ActivatedRoute,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.id = this.route.snapshot.paramMap.get('postId') || '';

    this.postService.find(this.id).subscribe((data: Post) => {
      this.post = data;

      this.form = new FormGroup({
        title: new FormControl(this.post.title, [Validators.required]),
        body: new FormControl(this.post.body, Validators.required)
      });
    });
  }

  get f() {
    return this.form.controls;
  }

  submit() {
    this.postService.update(this.id, this.form.value).subscribe(() => {
      this.router.navigateByUrl('post/index');
    });
  }
}
