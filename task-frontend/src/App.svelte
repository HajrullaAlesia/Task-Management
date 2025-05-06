<script>
  import { onMount } from 'svelte';
  import { tick } from 'svelte';
  import { user } from './stores.js';
  import { Router, Route, navigate } from 'svelte-navigator'; 

  import Login from './pages/Login.svelte';
  import Signup from './pages/Signup.svelte';
  import Dashboard from './pages/Dashboard.svelte';


 onMount(() => {
    if (!$user && location.pathname === '/dashboard') {
      navigate('/login');
    }

    if ($user && location.pathname === '/login') {
      navigate('/dashboard');
    }
  });

</script>

<main>
  <Router>

    <Route path="/" component={Login} />
    <Route path="/login" component={Login} />
    <Route path="/signup" component={Signup} />
    <Route path="/dashboard">
      {#if $user}
        <Dashboard />
      {:else}
        {navigate('/login')}
      {/if}
    </Route>
  </Router>
</main>
