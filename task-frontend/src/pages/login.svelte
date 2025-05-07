<script>
  import { login } from '../stores.js'; 
  import { useLocation, useNavigate } from 'svelte-navigator';

  export let location  = useLocation();
  export let navigate = useNavigate();

  let email = '', password = '', error = ''; 

async function handleLogin() {
  try {
    const res = await fetch('http://localhost:8000/api/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    if (!res.ok) {
      const errData = await res.json();
      throw new Error(errData.detail || 'Login failed');
    }

    const data = await res.json();
    
    login(data.access ); 

    navigate('/dashboard');
  } catch (e) {
    error = e.message;
  }
}

</script>

<main class="mt-40 max-w-sm mx-auto p-4 bg-white rounded shadow-md">
  <h2 class="text-2xl font-semibold mb-4 text-center">Login</h2>
  <form on:submit|preventDefault={handleLogin} class="space-y-4">
    <input 
      type="email" 
      bind:value={email} 
      placeholder="Email" 
      required 
      class="border p-2 w-full"
    />
    <input 
      type="password" 
      bind:value={password} 
      placeholder="Password" 
      required 
      class="border p-2 w-full"
    />
    <button 
      type="submit" 
      class="bg-blue-500 text-white px-4 py-2 rounded w-full"
    >
      Login
    </button>
  </form>
  <p class="mt-4 text-center">
    Don't have an account? <button on:click={() => navigate('/signup')} class="text-blue-500">Sign up</button>
  </p>
</main>
