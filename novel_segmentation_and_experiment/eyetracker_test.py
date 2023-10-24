import asyncio
import logging
import os

from g3pylib import connect_to_glasses

logging.basicConfig(level=logging.INFO)


async def access_recordings():
    async with connect_to_glasses.with_hostname(os.environ["G3_HOSTNAME"]) as g3:  # "G3_HOSTNAME" is the serial number of the eyetracker
        async with g3.recordings.keep_updated_in_context():
            logging.info(
                f"Recordings before: {list(map(lambda r: r.uuid, g3.recordings.children))}"
            )
            await g3.recorder.start()
            logging.info("Creating new recording")
            await asyncio.sleep(3)
            await g3.recorder.stop()
            logging.info(
                f"Recordings after: {list(map(lambda r: r.uuid, g3.recordings.children))}"
            )
            creation_time = await g3.recordings[0].get_created()
            logging.info(f"Creation time of last recording in UTC: {creation_time}")


def main():
    asyncio.run(access_recordings())


if __name__ == "__main__":
    main()