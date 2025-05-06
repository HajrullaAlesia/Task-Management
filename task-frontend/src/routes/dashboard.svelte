<script>

  import TaskTable from '../components/TaskTable.svelte';
  import TaskForm from '../components/TaskForm.svelte';
  import { onMount } from 'svelte';
  import { tasks, user } from '../stores.js';
  import { useLocation, useNavigate } from 'svelte-navigator';

  export let location  = useLocation();
  export let navigate = useNavigate();



  let showForm = false;
  let editTask = null;
  let filter = 'todo';
  let searchQuery = '';
  let filterName = 'To Do';
  let filterOpen = false;
  const API_URL = 'http://localhost:8000/api/tasks';
  const baseUrl = `${API_URL}/search/`;
  let currentPageUrl = baseUrl;
  let fallbackTried = false;

  let nextPage = null;
  let previousPage = null;

  function openForm(task = null) {
    editTask = task;
    showForm = true;
  }

  function closeForm() {
    editTask = null;
    showForm = false;
  }

  function goToPage(url) {
    currentPageUrl = url;
    searchTasks();
  }

  function resetAndSearch() {
    currentPageUrl = baseUrl;
    searchTasks();
  }

  async function searchTasks() {
    const payload = {};

    if (searchQuery.trim() !== '') {
      payload.search = searchQuery;
    }
    if (filter === 'done') {
      payload.is_done = true;
    } else if (filter === 'todo') {
      payload.is_done = false;
    }

    try {
      const res = await fetch(currentPageUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        if (!fallbackTried && res.status === 404 && currentPageUrl.includes("page=")) {
          fallbackTried = true;
          currentPageUrl = `${API_URL}/search/`;
          return await searchTasks();
        }
        console.error(` HTTP ${res.status} from ${currentPageUrl}`);
        return;
      }

      fallbackTried = false;
      const data = await res.json();
      tasks.set(data.results);
      nextPage = data.next;
      previousPage = data.previous;
    } catch (err) {
      console.error("searchTasks() failed:", err);
    }
  }

  function handleClickOutsideFilter(e) {
    if (!e.target.closest('.filter-dropdown')) {
      filterOpen = false;
    }
  }

  function logout() {
    user.set(null);
    localStorage.removeItem('authToken');
    navigate('/login');
  }

  onMount(() => {
    if (!$user) {
      navigate('/login');
      return;
    }

    searchTasks();
    document.addEventListener('click', handleClickOutsideFilter);
    return () => document.removeEventListener('click', handleClickOutsideFilter);
  });

  $: if (filter || searchQuery) {
    searchTasks();
  }
</script>

<main class="min-h-screen flex flex-col justify-between p-6 max-w-5xl mx-auto">
  <div class="flex justify-between items-center mb-6">
    <h1 class="text-2xl font-bold">Task Management</h1>
    
    <button on:click={logout} class="text-sm px-4 py-2 bg-red-500 text-white rounded">Logout</button>
  </div>

  <div class="flex-grow flex flex-col justify-start min-h-[600px]">
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center gap-4">
        <div class="relative">
          <input
            type="text"
            placeholder="Search"
            bind:value={searchQuery}
            on:input={searchTasks}
            class="border px-3 py-1 rounded pl-8"
          />
          <span class="absolute left-2 top-1.5 text-gray-400">🔍</span>
        </div>

        <div class="relative filter-dropdown">
          <button
            class="bg-black text-white px-7 py-1 rounded flex items-center gap-2 "
            on:click={() => (filterOpen = !filterOpen)}
          >
            {filterName}
          </button>

          {#if filterOpen}
            <div class="absolute mt-2 bg-white border rounded shadow z-10">
              <button on:click={() => { filter = 'all'; filterName = 'All Tasks'; filterOpen = false; resetAndSearch(); }} class="block w-full px-4 py-2 text-left hover:bg-gray-100">All Tasks</button>
              <button on:click={() => { filter = 'todo'; filterName = 'To Do'; filterOpen = false; resetAndSearch(); }} class="block w-full px-4 py-2 text-left hover:bg-gray-100">To Do</button>
              <button on:click={() => { filter = 'done'; filterName = 'Done'; filterOpen = false; resetAndSearch(); }} class="block w-full px-4 py-2 text-left hover:bg-gray-100">Done</button>
            </div>
          {/if}
        </div>
      </div>

   
      <div class="flex items-center gap-2">
        <button on:click={() => openForm()} class="bg-green-600 text-white px-4 py-2 rounded">+ Create Task</button>
      </div>
    </div>

 
    <TaskTable on:edit={(e) => openForm(e.detail)} on:refresh={searchTasks} />

   
    {#if showForm}
      <TaskForm {editTask} on:close={closeForm} on:refresh={searchTasks} />
    {/if}
  </div>

  <div class="flex justify-between items-center gap-4 mt-4">
    <button disabled={!previousPage} on:click={() => goToPage(previousPage)} class="bg-gray-200 px-4 py-1 rounded">
      ← Previous
    </button>

    <button disabled={!nextPage} on:click={() => goToPage(nextPage)} class="bg-gray-200 px-4 py-1 rounded">
      Next →
    </button>
  </div>
</main>
