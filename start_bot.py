#!/usr/bin/env python3
"""
Startup script for Discord Email Management Bot
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if all dependencies are installed"""
    try:
        import discord
        import aiofiles
        import requests
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Installing dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def main():
    """Main startup function"""
    print("🚀 Discord Email Management Bot Startup")
    print("=" * 50)
    
    # Configure logging for better debugging on Render
    import logging
    import sys
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Check for environment variables
    bot_token = os.getenv('DISCORD_BOT_TOKEN')
    if not bot_token:
        print("❌ DISCORD_BOT_TOKEN environment variable is required!")
        print("💡 Please set your Discord bot token in the Render.com environment variables")
        print("   1. Go to your Render.com service dashboard")
        print("   2. Navigate to Environment tab")
        print("   3. Add DISCORD_BOT_TOKEN with your bot token")
        print("   4. Redeploy the service")
        return
    
    # Validate token format
    if not bot_token.count('.') == 2:
        print("❌ Invalid Discord bot token format!")
        print("💡 Discord bot tokens should have format: XXXXXX.XXXXXX.XXXXXX")
        return
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Failed to install dependencies")
        return
    
    # Extract client ID from token
    def get_client_id_from_token(token):
        try:
            import base64
            client_id_b64 = token.split('.')[0]
            client_id_b64 += '=' * (4 - len(client_id_b64) % 4)
            client_id = base64.b64decode(client_id_b64).decode('utf-8')
            return client_id
        except Exception:
            return None
    
    client_id = get_client_id_from_token(bot_token)
    
    # Display bot information
    print("\n📧 Bot Configuration:")
    print("   • Bot Token: ✅ Loaded from environment")
    print("   • Permissions: 8 (Administrator)")
    print("   • Prefix: !")
    
    if client_id:
        print("\n🔗 Bot Invite Link:")
        print(f"https://discord.com/api/oauth2/authorize?client_id={client_id}&permissions=8&scope=bot")
    else:
        print("\n⚠️  Could not extract client ID from token")
    
    print("\n📋 Available Commands:")
    print("   • !upload - Upload email:password list")
    print("   • !webhook <url> - Set webhook for email forwarding")
    print("   • !stats - Show account statistics")
    print("   • !stop - Stop validation process")
    print("   • !commands - Show help message")
    
    print("\n🎯 Features:")
    print("   • Mass email validation (up to 50 concurrent)")
    print("   • Real-time progress tracking")
    print("   • Automatic email monitoring")
    print("   • Webhook forwarding")
    print("   • Support for 50+ email providers")
    
    print("\n" + "=" * 50)
    
    # Start health server for Render.com web service
    print("🌐 Starting health server...")
    try:
        # Add current directory to Python path to ensure imports work
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
            
        from health_server import HealthServer
        # Get port from environment (Render sets this)
        port = int(os.getenv('PORT', 10000))
        health_server = HealthServer(port=port)
        health_server.start_in_thread()
        print(f"✅ Health server started on port {port}")
    except Exception as e:
        print(f"⚠️  Health server error: {str(e)}")
        print("Continuing without health server...")
    
    print("🤖 Starting Discord bot...")
    
    # Add current directory to Python path to ensure imports work
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    
    # Import and run the bot
    try:
        print("📦 Importing discord_bot module...")
        import discord_bot
        print("✅ Discord bot module imported successfully")
        print("🚀 Starting bot...")
        discord_bot.bot.run(bot_token)
    except KeyboardInterrupt:
        print("\n⏹️ Bot stopped by user")
    except ImportError as e:
        print(f"\n❌ Import error: {str(e)}")
        print(f"Current directory: {current_dir}")
        print(f"Python path: {sys.path}")
        print("Available files:")
        for file in os.listdir(current_dir):
            print(f"  - {file}")
    except Exception as e:
        print(f"\n❌ Bot error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()