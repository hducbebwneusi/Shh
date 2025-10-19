"""
Simple health check server for Render.com deployment
This runs alongside the Discord bot to provide health check endpoint
"""
import asyncio
from aiohttp import web
import threading
import logging
import os

logger = logging.getLogger(__name__)

class HealthServer:
    def __init__(self, port=None):
        # Use PORT environment variable from Render.com, fallback to 10000
        self.port = port or int(os.getenv('PORT', 10000))
        self.app = web.Application()
        self.setup_routes()
        
    def setup_routes(self):
        self.app.router.add_get('/health', self.health_check)
        self.app.router.add_get('/', self.health_check)
        
    async def health_check(self, request):
        import time
        return web.json_response({
            'status': 'healthy',
            'service': 'discord-email-bot',
            'message': 'Bot is running',
            'timestamp': int(time.time()),
            'port': self.port,
            'environment': 'render.com'
        })
    
    async def start_server(self):
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', self.port)
        await site.start()
        logger.info(f"Health server started on port {self.port}")
        
    def start_in_thread(self):
        """Start the health server in a separate thread"""
        def run_server():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.start_server())
            loop.run_forever()
            
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        logger.info("Health server thread started")

# Global health server instance
health_server = HealthServer()