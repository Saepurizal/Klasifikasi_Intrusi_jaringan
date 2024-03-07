from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ServiceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get('command', None)
        
        if command == 'start':
            # Lakukan tindakan untuk memulai deteksi intrusi
            # Misalnya, mengirim perintah ke channel layer
            # dan mengirimkan pesan balik ke klien
            await self.send(text_data=json.dumps({'status': 'Deteksi intrusi diaktifkan'}))
        elif command == 'stop':
            # Lakukan tindakan untuk menghentikan deteksi intrusi
            # Misalnya, mengirim perintah ke channel layer
            # dan mengirimkan pesan balik ke klien
            await self.send(text_data=json.dumps({'status': 'Deteksi intrusi dihentikan'}))
