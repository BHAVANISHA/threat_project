from django.shortcuts import render
import concurrent.futures
from rest_framework.response import Response
import requests
import multiprocessing
from rest_framework import viewsets
import aiohttp
from adrf.views import APIView
import time,threading
import asyncio
import httpx
from django.http import HttpResponse


# thread pool executor
class Thread_pool( APIView ):

    def get(self, request):
        start = time.time()
        api_urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
            'https://jsonplaceholder.typicode.com/posts/4'
        ]

        def fetch_data(url):
            response = requests.get( url )
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list( executor.map( fetch_data, api_urls ) )

        data = [{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response( ans )


def fetch_data(url):
    response = requests.get( url )
    if response.status_code == 200:
        return response.json()
    return {'error': f'Failed to retrieve data from {url}'}


class Multiprocess( APIView ):
    def get(self, request):
        start = time.time()
        api_urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
            'https://jsonplaceholder.typicode.com/posts/4'
        ]

        with multiprocessing.Pool( processes=len( api_urls ) ) as pool:
            results = pool.map( fetch_data, api_urls )

        data = [{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response( ans )


# httpx
class Httpx( viewsets.ViewSet ):

    def fetch_data(self, request):
        start = time.time()

        async def fetch(url):
            async with httpx.AsyncClient() as client:
                response = await client.get( url )
                if response.status_code == 200:
                    return response.json()
                return {'error': f'Failed to retrieve data from {url}'}

        api_urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
            'https://jsonplaceholder.typicode.com/posts/4'
        ]

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop( loop )
        results = loop.run_until_complete( asyncio.gather( *[fetch( url ) for url in api_urls] ) )
        loop.close()

        data = [{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response( ans )

    def list(self, request):
        return self.fetch_data( request )


# aiohttp


class AIO( APIView ):
    async def get(self, request):
        start = time.time()

        async def fetch_data(url):
            async with aiohttp.ClientSession() as session:
                async with session.get( url ) as response:
                    if response.status == 200:
                        return await response.json()
                    return {'error': f'Failed to retrieve data from {url}'}

        api_urls = [
            'https://jsonplaceholder.typicode.com/posts/1',
            'https://jsonplaceholder.typicode.com/posts/2',
            'https://jsonplaceholder.typicode.com/posts/3',
            'https://jsonplaceholder.typicode.com/posts/4'
        ]

        tasks = [fetch_data( url ) for url in api_urls]
        results = await asyncio.gather( *tasks )

        data = [{"data": result} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response( ans )


# async


class Asyncio( APIView ):
    async def get(self, request):
        start = time.time()

        async def fetch_data(url):
            response = await asyncio.to_thread( requests.get, url )
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}
        api_urls = [
            'https://api.publicapis.org/entries',
            'https://catfact.ninja/fact',
            'https://api.coindesk.com/v1/bpi/currentprice.json',
            'https://www.boredapi.com/api/activity'
        ]
        tasks = [fetch_data( url ) for url in api_urls]
        results = await asyncio.gather( *tasks )
        data=[{"data":results} for result in results]
        end = time.time()
        total = end - start
        ans = {"data": data, "total": total}
        return Response( ans )



# app api


class FetchDataView(APIView):
    def get(self, request):
        urls = [
            'https://data.covid19india.org/v4/min/data.min.json',
            'https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_ACTUAL_API_KEY',
            'https://api.coingecko.com/api/v3/coins/bitcoin',
        ]

        def fetch_data(url):
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            return {'error': f'Failed to retrieve data from {url}'}
        start_time = time.time()
        threads = []
        fetched_data = []

        for url in urls:
            thread = threading.Thread(target=self.fetch_and_store_data, args=(url, fetched_data))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()
        end_time = time.time()
        total_time = end_time - start_time

        response_data = {
            'data': fetched_data,
            'total_time_seconds': total_time
        }
        return Response(response_data)

    def fetch_and_store_data(self, url, data_container):
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            data_container.append(data)
        else:
            data_container.append({'error': f'Failed to retrieve data from {url}'})
