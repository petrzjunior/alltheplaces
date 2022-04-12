# -*- coding: utf-8 -*-
import scrapy
import json
from collections import namedtuple
from locations.items import GeojsonPointItem

class GrimaldisPizzeriaSpider(scrapy.Spider):
    name = 'grimaldis_pizzeria'
    allowed_domains = ['www.grimaldispizzeria.com']
    start_urls = (
        'https://www.grimaldispizzeria.com/locations/',
        'https://local.vons.com/ca.html',
        ...
    )

    def parse(self, response):
        locations = response.css('div.location_block')

        for loc in locations:
            address = self._format_address(loc.css('.store_address::text').getall())

            properties = {
                "ref": loc.css('h3.loc_title::text').get(),
                "name": loc.css('.loc_title::text').get(),
                "addr_full": address.street_address,
                "city": address.city,
                "state": address.state,
                "postcode": address.zip,
                "phone": self._format_phone(loc.css('.phone_number::text')),
                "opening_hours": loc.css('.store_hours::text').getall()
            }

            yield GeojsonPointItem(**properties)



    def _format_address(self, address):
        Address = namedtuple('Address', ['street_address', 'city', 'state', 'zip'])
        street_address = address[0].strip()
        city_state_zip = address[1].split(',')
        city = city_state_zip[0].replace(',', '')
        state, zip = city_state_zip[1].split()

        return Address(
            street_address=street_address,
            city=city,
            state=state,
            zip=zip
        )

    def _format_phone(self, phone):
        # if phone number is found
        if phone.getall():
            return phone.getall()[1].strip()
        else:
            return ''







           # lat = scrapy.Field()
           # lon = scrapy.Field()
           # name = scrapy.Field()
           # addr_full = scrapy.Field()
           # housenumber = scrapy.Field()
           # street = scrapy.Field()
           # city = scrapy.Field()
           # state = scrapy.Field()
           # postcode = scrapy.Field(
           # country = scrapy.Field()
           # phone = scrapy.Field()
           # website = scrapy.Field()
           # opening_hours = scrapy.Field()
           # ref = scrapy.Field()
           # brand = scrapy.Field()
           # brand_wikidata = scrapy.Field()
           # extras = scrapy.Field()


        # properties = {
        #     "name": loc["name"],
        #     "brand": loc["brand"],
        #     "phone": loc["phones"][0]["phone_number"],
        #     "addr_full": loc["address"]["street_addresses"],
        #     "city": loc["address"].get("city"),
        #     "state": loc["address"]["country_subdivision_code"],
        #     "postcode": loc["address"]["postal"],
        #     "country": loc["address"].get("country_code"),
        #     "lat": float(loc["gps"]["latitude"]),
        #     "lon": float(loc["gps"]["longitude"]),
        #     "ref": loc["id"],
        # }

        # print(response.xpath('[@ id = "alabama"]').extract())

        # return GeojsonPointItem
