from fastapi import UploadFile

from pathlib import Path

from app.core.config import UPLOAD_DIR_NAME

import time
import aiofiles


class Upload:
    def __init__(self, file: UploadFile):
        self.file = file

    async def save(self) -> Path:
        app_path = Path(__file__).parents[1]
        upload_dir_name = UPLOAD_DIR_NAME
        upload_dir_path = app_path.joinpath(upload_dir_name)

        Path.mkdir(upload_dir_path, exist_ok=True)

        extension = self.file.content_type.split("/")[1]

        file_path = f"{upload_dir_name}/{time.time()}-{self.file.filename}.{extension}"
        file_abs_path = app_path.joinpath(file_path)

        async with aiofiles.open(file_abs_path, "wb") as fp:
            await self.file.seek(0)
            while content := await self.file.read(1024):
                await fp.write(content)

        return Path(file_abs_path)
