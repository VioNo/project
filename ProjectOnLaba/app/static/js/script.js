async function updateTask(taskId, taskData) {
    const url = `/tasks/${taskId}`;

    try {
        const response = await fetch(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(taskData),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const updatedTask = await response.json();
        console.log('Task updated successfully:', updatedTask);
        return updatedTask;
    } catch (error) {
        console.error('Failed to update task:', error);
    }
}

