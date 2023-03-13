import uasyncio as asyncio

class Foo():
    def __init__(self,ID):
        self.ID=ID
        print(f'constructor: {self.ID}')
        
    async def sender(self):
        while True:
            print(f"send: {self.ID}")
            await asyncio.sleep(1)

    async def receiver(self):
        while True:
            print(f"receive: {self.ID}")
            await asyncio.sleep(1)

    def toto(self):
        print('toto')        

    def run(self):
        asyncio.create_task(self.sender())
        asyncio.create_task(self.receiver())

async def run_forever():
    while True:
        await asyncio.sleep(1)

def set_global_exception():
    def handle_exception(loop, context):
        import sys
        sys.print_exception(context["exception"])
        sys.exit()
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)

async def bar():
    set_global_exception()
    foo1 = Foo(1)  # Foo is an awaitable class
    foo1.run()

    foo2 = Foo(2)  # Foo is an awaitable class
    foo2.run()
    
    await run_forever()

if __name__=="__main__":
    try:
        asyncio.run(bar())
    finally:
        asyncio.new_event_loop()
