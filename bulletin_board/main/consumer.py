from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from .models import Ad, Car, Thing, Service
from .utils import remove_tags


class AdConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        await self.send_json(content={"type": "message",
                                      "data": {"author": self.scope["user"].username, "color": "green",
                                               "time": datetime.now().isoformat(), "text": remove_tags(text_data)}})
        if text_data[0] == '#':
            search_result = await database_sync_to_async(self.get_ad)(name=text_data[1:])
            await self.send_json(content={"type": "message",
                                          "data": {"author": "Bot", "color": "blue",
                                                   "time": datetime.now().isoformat(), "text": search_result}})

    async def disconnect(self, close_code):
        # Called when the socket closes
        pass

    def get_ad(self, name):
        try:
            # get current child ad model instance
            ad = eval(Ad.objects.get(name=name).ad_type.model.title()).objects.get(name=name)
        except ObjectDoesNotExist:
            return "Ничего не найдено!"
        if ad.is_sold:
            res = "Продано!"
        local_fields = ad._meta.local_fields[1:]  # getting list of local fields in current model
        verbose_names = [x.verbose_name for x in local_fields]
        field_values = [str(ad.__getattribute__(e.name)) + "</div>" for e in
                        local_fields]  # getting local fields values

        return self.render_post(ad.price, verbose_names, field_values)

    def render_post(self, price, verbose_names, field_values):
        output = '<div class="d-flex flex-row"><div class="d-flex flex-column">' \
                 'Цена: </div><div class="d-flex flex-column">' \
                 f'{str(price)}</div></div>'
        for verbose_name, value in zip(verbose_names, field_values):
            output += f'<div class="d-flex flex-row"><div class="d-flex flex-column">{verbose_name}: </div>"' \
                      + f'<div class="d-flex flex-column">{value}</div></div>'
        return output
