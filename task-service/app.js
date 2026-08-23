const express = require('express');
const app = express();
app.use(express.json());
let tasks = [
 { id: 1, title: 'Setup Docker', status: 'completed', priority: 'high' },
 { id: 2, title: 'Learn Kubernetes', status: 'in-progress', priority: 'high' },
 { id: 3, title: 'Deploy to production', status: 'pending', priority: 'high' }
];
let taskId = 4;
app.get('/health', (req, res) =>
 res.json({ status: 'healthy', service: 'task-service', timestamp: new Date().toISOString() })
);
app.get('/tasks', (req, res) =>
 res.json({ count: tasks.length, tasks, timestamp: new Date().toISOString() })
);
app.get('/tasks/:id', (req, res) => {
 const task = tasks.find(t => t.id === parseInt(req.params.id, 10));
 if (!task) return res.status(404).json({ error: 'Task not found' });
 res.json(task);
});
app.post('/tasks', (req, res) => {
 const { title, status, priority } = req.body || {};
 if (!title) return res.status(400).json({ error: 'Title is required' });
 const newTask = {
 id: taskId++,
 title,
 status: status || 'pending',
 priority: priority || 'medium',
 createdAt: new Date().toISOString()
 };
 tasks.push(newTask);
 res.status(201).json(newTask);
});
app.put('/tasks/:id', (req, res) => {
 const task = tasks.find(t => t.id === parseInt(req.params.id, 10));
 if (!task) return res.status(404).json({ error: 'Task not found' });
 Object.assign(task, req.body);
 res.json(task);
});
app.delete('/tasks/:id', (req, res) => {
 const i = tasks.findIndex(t => t.id === parseInt(req.params.id, 10));
 if (i === -1) return res.status(404).json({ error: 'Task not found' });
 res.json({ message: 'Task deleted', deleted: tasks.splice(i, 1)[0] });
});
const server = app.listen(5001, () => console.log('Task Service on 5001'));
process.on('SIGTERM', () => server.close(() => process.exit(0)));
