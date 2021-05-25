from starlette.datastructures import UploadFile as StarletteUploadFile

from app.core.upload import Upload

from unittest import mock

import pytest


@pytest.mark.asyncio
async def test_upload_save(file: StarletteUploadFile):
    mock_file = mock.MagicMock()
    with mock.patch("aiofiles.threadpool.sync_open", return_value=mock_file):
        upload = Upload(file=file)
        await upload.save()

        mock_file.write.assert_called()
