<script>
  import { onMount } from 'svelte';
  import { tick } from 'svelte';
  import { user } from './stores.js';
  import { Router, Route, navigate } from 'svelte-navigator'; 

  import Login from './routes/Login.svelte';
  import Signup from './routes/Signup.svelte';
  import Dashboard from './routes/Dashboard.svelte';


</script>

<main>
  <Router>
    <Route path="/" component={Login} />
    <Route path="/login" component={Login} />
    <Route path="/signup" component={Signup} />
    <Route path="/dashboard" component={Dashboard} />
  </Router>
</main>
