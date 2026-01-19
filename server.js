/*
systemd setup (/etc/systemd/system/circles-proxy.service):

[Unit]
Description=Circles Magazine Proxy Server
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/path/to/circles-magazine
ExecStart=/usr/bin/node server.js
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target

Commands:
  sudo systemctl daemon-reload
  sudo systemctl enable circles-proxy
  sudo systemctl start circles-proxy
  sudo systemctl status circles-proxy
  journalctl -u circles-proxy -f
*/

const http = require('http');
const https = require('https');

const PORT = 3000;
const TARGET_URL = 'https://hasura.bi.status.im/api/rest/circle/events';

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  if (req.url === '/events' && req.method === 'GET') {
    https.get(TARGET_URL, (proxyRes) => {
      let data = '';

      proxyRes.on('data', (chunk) => {
        data += chunk;
      });

      proxyRes.on('end', () => {
        res.setHeader('Content-Type', 'application/json');
        res.writeHead(proxyRes.statusCode);
        res.end(data);
      });
    }).on('error', (err) => {
      res.writeHead(500);
      res.end(JSON.stringify({ error: err.message }));
    });
  } else {
    res.writeHead(404);
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

server.listen(PORT, () => {
  console.log(`Proxy server running at http://localhost:${PORT}`);
  console.log(`Fetch events at http://localhost:${PORT}/events`);
});
