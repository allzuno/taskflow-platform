const express = require('express');
const axios = require('axios');
const app = express();
app.use(express.json());

const serviceUrls = {
  tasks: process.env.TASK_SERVICE_URL || 'http://task-service:5001',
  users: process.env.USER_SERVICE_URL || 'http://user-service:5002',
  notifications: process.env.NOTIFICATION_SERVICE_URL || 'http://notification-service:5003'
};

app.get('/health', (req, res) =>
  res.json({ status: 'healthy', service: 'api-gateway', timestamp: new Date().toISOString() })
);

app.get('/tasks', async (req, res) => {
  try {
    const response = await axios.get(`${serviceUrls.tasks}/tasks`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch tasks', message: error.message });
  }
});

app.post('/tasks', async (req, res) => {
  try {
    const response = await axios.post(`${serviceUrls.tasks}/tasks`, req.body);
    res.status(201).json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to create task', message: error.message });
  }
});

app.get('/users', async (req, res) => {
  try {
    const response = await axios.get(`${serviceUrls.users}/users`);
    res.json(response.data);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch users', message: error.message });
  }
});

const server = app.listen(5000, () => console.log('API Gateway on 5000'));
process.on('SIGTERM', () => server.close(() => process.exit(0)));
