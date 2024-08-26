<template>
  <main>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Email</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div>
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
        <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      </form>
    </div>
  </main>
    
  </template>
  
  <script>
  export default {
    name:"LoginPage",
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      async handleLogin() {
        fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      username: this.username,
      password: this.password
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      // Store the token in localStorage or Vuex (if using Vuex)
      localStorage.setItem('token', data.access_token);
      // Redirect to the dashboard
      console.log()
      this.$router.push('/dashboard');
    } else {
      // Handle login error
      alert('Login failed');
    }
  })
  .catch(error => {
    console.error('Error:', error);
  });
      },
    },
  };
  </script>
  
  <style scoped>
  main{
    justify-content: center;


  }
  .login {
    max-width: 400px;
    margin: auto;
    padding: 1em;
  }
  
  .error {
    color: red;
  }
  </style>
  