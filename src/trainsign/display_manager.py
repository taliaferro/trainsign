import asyncio

from jinja2 import Environment


class DisplayManager:
    def __init__(
        self,
        visit_stream,
        output=sys.stdout,
        init_screens=[],
        loop_screens=[],
    ):
        self.visit_stream = visit_stream
        self.replace_newlines = replace_newlines
        self.env = Environment(extensions=["jinja2_time.TimeExtension"])
        for screen in init_screens:
            await display(screen)

        self.display_loop_task = asyncio.create_task(self.display_loop(loop_screens))

    async def display(self, screen):
        self.output.write(screen)
        asyncio.sleep(screen.seconds())

    async def display_loop(screens):
        while True:
            for screen in screens:
                display(screen)
