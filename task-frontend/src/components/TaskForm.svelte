<script>
  import { createEventDispatcher, beforeUpdate } from 'svelte';
  export let editTask = null;
  const dispatch = createEventDispatcher();
  const API_URL = 'http://localhost:8000/api/tasks';

  let title = '';
  let is_done = false;
  let deadline = '';

  
  let previousTaskId = null;



  beforeUpdate(() => {
    if (editTask && editTask.id !== previousTaskId) {
      title = editTask.title;
      is_done = editTask.is_done;
      deadline = editTask.deadline ;
      previousTaskId = editTask.id;
    }
    if (!editTask && previousTaskId !== null) {
      title = '';
      is_done = false;
      deadline = '';
      previousTaskId = null;
    }
  });

  async function saveTask() {

    const payload = { title, is_done, deadline };
    const method = editTask ? 'PUT' : 'POST';
    const url = editTask ? `${API_URL}/${editTask.id}/` : `${API_URL}/`;
    try {
      const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) throw new Error('Failed to save task');

      await res.json(); 

      dispatch('refresh'); 
      dispatch('close');
    } catch (e) {
      console.warn('Error saving task:', e);
    }
  }
</script>

<div class="fixed inset-0 bg-black bg-opacity-50 flex justify-center items-center">
  <form class="bg-white p-6 rounded shadow w-full max-w-md" on:submit|preventDefault={saveTask}>
    <h2 class="text-xl font-bold mb-4">{editTask ? 'Edit Task' : 'Create Task'}</h2>

    <label class="block mb-2">Title</label>
    <input class="border rounded w-full px-3 py-2 mb-4" type="text" bind:value={title} required />

    <label class="inline-flex items-center mb-4">
      <input type="checkbox" bind:checked={is_done} class="mr-2" />
      Done
    </label>

    <label class="block mb-2">Deadline</label>
<input type="date" class="border rounded w-full px-3 py-2 mb-4" bind:value={deadline} />



    <div class="flex justify-end gap-2">
      <button type="button" on:click={
        () => dispatch('close')} 
        class="px-4 py-2 border rounded">Cancel</button>
      <button type="submit" class="px-4 py-2 bg-green-600 text-white rounded">
        {editTask ? 'Save' : 'Create'}
      </button>
    </div>
  </form>
</div>

