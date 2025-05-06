<script>
  import { createEventDispatcher, onMount } from 'svelte';
  import { tasks } from '../stores.js';

  const dispatch = createEventDispatcher();
  let openMenuId = null;

  function toggleMenu(id) {
    openMenuId = openMenuId === id ? null : id;
  }

  function handleClickOutside(e) {
    if (!e.target.closest('.dropdown')) openMenuId = null;
  }

  async function deleteTask(id) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    try {
      await fetch(`http://localhost:8000/api/tasks/${id}/`, { method: 'DELETE' });
      dispatch('refresh');
    } catch (err) {
      console.error("Error deleting task:", err);
    }
  }

  onMount(() => {
    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  });
</script>

<table class="w-full bg-white shadow rounded">


  <thead class="bg-gray-100">
    <tr class="text-left border-b">
      <th class="p-3">Title</th>
      <th class="p-3">Status</th>
      <th class="p-3">Deadline</th>
      <th class="p-3 text-right">Actions</th>
    </tr>
  </thead>
  <tbody>
    {#if $tasks.length === 0}
      <tr><td colspan="4" class="p-4 text-center text-gray-400">No tasks found.</td></tr>
    {/if}
    {#each $tasks as task}
      <tr class="border-t hover:bg-gray-50">
        <td class="p-3">{task.title}</td>
        <td class="p-3">{task.is_done ? 'Done' : 'To Do'}</td>
        <td class="p-3">{task.deadline ? new Date(task.deadline).toLocaleDateString() : '—'}</td>
        <td class="p-3 text-right">
          <div class="dropdown relative inline-block">
            <button on:click={() => toggleMenu(task.id)} class="p-2 hover:bg-gray-200 rounded">⋮</button>
            {#if openMenuId === task.id}
              <div class="absolute right-0 mt-2 w-32 bg-white border rounded shadow animate-fade z-10">
                <button on:click={() => { dispatch('edit', task); openMenuId = null; }} class="block w-full px-4 py-2 text-left hover:bg-blue-100">Edit</button>
                <button on:click={() => { deleteTask(task.id); openMenuId = null; }} class="block w-full px-4 py-2 text-left text-red-600 hover:bg-red-100">Delete</button>
              </div>
            {/if}
          </div>
        </td>
      </tr>
    {/each}
  </tbody>
</table>
