<script>
  import { login } from '../stores.js'; 
  import { useLocation, useNavigate } from 'svelte-navigator';

  export let location  = useLocation();
  export let navigate = useNavigate();
  
  let name = '', email = '', password = '', confirmPassword = '';
  let error = '', success = '';

  
  async function handleSignup() {
    error = ''; 
    success = ''; 

    
    if (password !== confirmPassword) {
      error = 'Passwords do not match';
      return;
    }

    try {
     
      const res = await fetch('http://localhost:8000/api/signup/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: name, email, password }),
      });

      
      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Signup failed');
      }

      
      const data = await res.json();

      login(data.user);

      success = 'Signup successful!';

      setTimeout(() => {
        navigate('/login');
      }, 2000); 
    } catch (e) {
      error = e.message;
    }
  }
</script>

<main class="mt-40 max-w-md mx-auto p-6 bg-white rounded shadow">
  <h2 class="text-xl font-bold mb-4 text-center">Create an Account</h2>

  <form on:submit|preventDefault={handleSignup} class="space-y-4">
    <!-- Input fields for the signup form -->
    <input
      type="text"
      bind:value={name}
      placeholder="Full Name"
      required
      class="border p-2 w-full rounded"
    />
    <input
      type="email"
      bind:value={email}
      placeholder="Email"
      required
      class="border p-2 w-full rounded"
    />
    <input
      type="password"
      bind:value={password}
      placeholder="Password"
      required
      class="border p-2 w-full rounded"
    />
    <input
      type="password"
      bind:value={confirmPassword}
      placeholder="Confirm Password"
      required
      class="border p-2 w-full rounded"
    />

   
    <button
      type="submit"
      class="bg-green-600 text-white px-4 py-2 rounded w-full"
    >
      Sign Up
    </button>

    
    {#if error}
      <p class="text-red-500 text-sm mt-2">{error}</p>
    {/if}
    {#if success}
      <p class="text-green-500 text-sm mt-2">{success}</p>
    {/if}
  </form>

  
  <p class="mt-4 text-center">
    Already have an account? 
    <button on:click={() => navigate('/login')} class="text-blue-500">Login</button>
  </p>
</main>
