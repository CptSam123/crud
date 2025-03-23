import { Component } from '@angular/core';
import { FormGroup, FormControl, Validators, ReactiveFormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-login',
  standalone: true,
  templateUrl: './login.component.html',
  imports: [ReactiveFormsModule, CommonModule]
})
export class LoginComponent {
  form = new FormGroup({
    email: new FormControl('', [Validators.required, Validators.email]),
    password: new FormControl('', Validators.required)
  });

  constructor(private authService: AuthService, private router: Router) {}

  submit() {
    if (this.form.invalid) return;

    const { email, password } = this.form.value;
    this.authService.login(email!, password!).subscribe({
      next: (res) => {
        this.authService.storeToken(res.token);
        this.router.navigate(['/post/index']);
      },
      error: () => alert('Invalid credentials')
    });
  }

  get f() {
    return this.form.controls;
  }
}
