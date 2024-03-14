const net = require('net');
const client = new net.Socket();

cmd = {
    // 'fn': 'resolve.get_version_string',
    // 'fn': 'resolve.get_project_manager',
    'fn': 'resolve.get_current_project',
    'args': [],
    'kwargs': {},
}

client.connect(65432, '127.0.0.1', function() {
    console.log('Connected');
    client.write(JSON.stringify(cmd));
});

client.on('data', function(data) {
    console.log('Received: ' + data);
    client.destroy(); // kill client after server's response
});

client.on('close', function() {
    console.log('Connection closed');
});

